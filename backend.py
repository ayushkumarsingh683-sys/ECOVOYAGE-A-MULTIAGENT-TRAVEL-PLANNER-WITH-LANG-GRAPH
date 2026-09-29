import os
import certifi
import operator
import uuid
import requests
from typing import TypedDict, Annotated

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

# =========================
# Database Setup (Neon PostgreSQL)
# =========================
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from environment variables.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TripRecord(Base):
    __tablename__ = "saved_trips"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, unique=True, index=True)
    user_query = Column(Text)
    itinerary_output = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)

# Automatically create tables on startup
init_db()

# =========================
# Secure API Key Loading (From .env)
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from environment variables.")


# ===================================================
# Stable Model Selector
# ===================================================
def get_active_groq_model():
    return "openai/gpt-oss-20b"

ACTIVE_MODEL = get_active_groq_model()
print(f"🤖 Connected to Groq using model: {ACTIVE_MODEL}")

# =========================
# LLM Initialization
# =========================
llm = ChatGroq(
    model=ACTIVE_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0.3
)

# =========================
# State Schema
# =========================
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    eco_results: str
    itinerary: str
    llm_calls: int

# =========================
# Agent Nodes
# =========================
def flight_agent(state: TravelState):
    query = state["user_query"]
    try:
        flight_data = search_flights(query)
    except Exception as e:
        flight_data = f"Flight search unavailable: {str(e)}"

    return {
        "flight_results": str(flight_data),
        "messages": [AIMessage(content="Flight options fetched.")],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def hotel_agent(state: TravelState):
    query = f"Best eco-friendly hotels and stays for {state['user_query']}"
    try:
        hotel_results = tavily_search(query)
    except Exception as e:
        hotel_results = f"Hotel search unavailable: {str(e)}"

    return {
        "hotel_results": str(hotel_results),
        "messages": [AIMessage(content="Hotel and eco-stay information fetched.")],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def eco_agent(state: TravelState):
    eco_prompt = f"""
Analyze the environmental impact and carbon footprint for this trip:
User Request: {state['user_query']}
Flights: {state['flight_results']}
Hotels: {state['hotel_results']}

Provide:
1. Estimated Carbon Footprint (kg CO2e benchmark).
2. 3 actionable Low-Carbon / Eco-Friendly Recommendations.
"""
    response = llm.invoke([
        SystemMessage(content="You are an environmental sustainability and green tourism expert."),
        HumanMessage(content=eco_prompt)
    ])

    return {
        "eco_results": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def itinerary_agent(state: TravelState):
    prompt = f"""
Create a complete travel itinerary.

User Query:
{state['user_query']}

Flight Results:
{state['flight_results']}

Hotel Results:
{state['hotel_results']}

Eco Assessment:
{state.get('eco_results', 'N/A')}

Make the itinerary practical, budget-aware, eco-conscious, and easy to follow.
"""
    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner specializing in sustainable tourism."),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def final_agent(state: TravelState):
    final_prompt = f"""
Generate the final EcoVoyage travel plan for the user in clean, readable text and structured markdown format without breaking layout syntax.

User Request: {state['user_query']}
Flights: {state['flight_results']}
Hotels: {state['hotel_results']}
Eco Assessment: {state.get('eco_results', 'N/A')}
Itinerary: {state['itinerary']}

CRITICAL FORMATTING INSTRUCTIONS:
- Ensure clean column formatting. Avoid broken layout syntaxes.
- Keep table cells concise, straight to the point, and clear.

Sections Required:
1. 🌍 Trip Summary (A clean 2-column format mapping Origin, Destination, Duration, Primary Transport, Accommodation, and Carbon Footprint)
2. 🚆 Flight & Transit Options (Structured comparison table)
3. 🏨 Eco-Friendly Hotel Suggestions (Structured hotel table)
4. 📅 Day-by-Day Itinerary (A clean chronological table with columns: [Day, City / Activity, Transport, Accommodation, Highlights])
5. 🌱 Carbon Footprint & Eco-Score
6. Estimated Budget
7. Final Recommendations
"""
    response = llm.invoke([
        SystemMessage(content="You are EcoVoyage, a professional AI sustainable travel booking assistant that outputs clean and structured markdown data."),
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# =========================
# Build StateGraph
# =========================
graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("eco_agent", eco_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "eco_agent")
graph.add_edge("eco_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)

# In-Memory Checkpointer Setup
checkpointer = MemorySaver()
travel_graph = graph.compile(checkpointer=checkpointer)

# =========================
# Execution Entrypoint (With Neon DB Integration)
# =========================
def run_travel_agent(user_input: str, thread_id: str | None = None):
    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {"configurable": {"thread_id": thread_id}}

    result = travel_graph.invoke(
        {
            "messages": [HumanMessage(content=user_input)],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "eco_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    final_output = result["messages"][-1].content

    # Save generated trip into Neon PostgreSQL Database
    try:
        db = SessionLocal()
        existing_trip = db.query(TripRecord).filter(TripRecord.thread_id == thread_id).first()
        if existing_trip:
            existing_trip.user_query = user_input
            existing_trip.itinerary_output = final_output
        else:
            db_trip = TripRecord(thread_id=thread_id, user_query=user_input, itinerary_output=final_output)
            db.add(db_trip)
        db.commit()
        db.close()
        print("💾 Trip successfully saved to Neon PostgreSQL database!")
    except Exception as e:
        print(f"⚠️ Database save error: {str(e)}")

    return {
        "thread_id": thread_id,
        "answer": final_output,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "eco_results": result.get("eco_results", ""),
        "itinerary": result.get("itinerary", ""),
        "llm_calls": result.get("llm_calls", 0),
    }