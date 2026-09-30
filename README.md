🌍 EcoVoyage: Multi-Agent AI Sustainable Travel Planner
EcoVoyage is an intelligent, multi-agent travel planning assistant designed to curate sustainable, budget-friendly, and eco-conscious itineraries. Powered by LangGraph and Groq AI, it automates flight searches, eco-friendly hotel curation, carbon footprint analysis, and structured itinerary generation while ensuring persistent data storage using Neon PostgreSQL.

🚀 Key Features
Multi-Agent Architecture: Collaborative specialized agents handling flight lookup, eco-stays, carbon emission analysis, and itinerary compilation.

Real-Time Web Search: Integrated with Tavily Search to fetch live, up-to-date eco-friendly hotel recommendations and travel insights.

Carbon Footprint Assessment: Evaluates environmental impact and provides actionable low-carbon recommendations.

Cloud Database Persistence: Automatically saves generated travel plans and user threads securely into Neon Cloud PostgreSQL.

Dockerized Deployment: Ready-to-deploy containerized structure for seamless running across environments.

Clean Markdown & UI: Outputs structured, readable itineraries preventing layout breaks.

🛠️ Tech Stack & Dependencies
Category	Technology / Library	Description
Backend Framework	FastAPI, Python	High-performance async web framework for API endpoints.
Orchestration	LangGraph (StateGraph, MemorySaver)	Multi-agent state machine and conversation memory management.
LLM Provider	Groq API (ChatGroq)	Ultra-fast LLM inference using optimized open models.
Database	Neon PostgreSQL, SQLAlchemy	Serverless cloud relational database with ORM mapping.
Search & Tools	Tavily API, Custom Flight Tools	External web search and flight transit data retrieval.
Containerization	Docker	Packaging the application for reliable deployment.
Frontend UI	HTML5, CSS3, JavaScript	Clean, responsive user interface for interaction.
🤖 Multi-Agent Workflow
Flight Agent (flight_agent): Fetches available flights and transit options matching user criteria.

Hotel Agent (hotel_agent): Searches for sustainable and eco-friendly accommodations via Tavily.

Eco Agent (eco_agent): Computes estimated carbon footprints and provides green recommendations.

Itinerary Agent (itinerary_agent): Builds a comprehensive, practical, and budget-aware schedule.

Final Agent (final_agent): Formulates the clean, structured final markdown layout displayed to the user.

⚙️ Getting Started & Installation
Option A: Running Locally (Virtual Environment)
1. Clone the Repository
Bash
git clone https://github.com/ayushkumarsingh683-sys/ECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH.git
cd ECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH
2. Create and Activate Virtual Environment
Bash
python -m venv travel
# On Windows:
.\travel\Scripts\Activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add your credentials:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://your_neon_postgres_connection_string
TAVILY_API_KEY=your_tavily_api_key_here
5. Run the Application
Start the FastAPI backend server using Uvicorn:

Bash
uvicorn app:app --reload
Open your browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Option B: Running with Docker 🐳
If you prefer to run the application inside a Docker container:

1. Build the Docker Image
Bash
docker build -t ecovoyage-app .
2. Run the Docker Container
Make sure to pass your .env file variables while running the container:

Bash
docker run -d -p 8000:8000 --env-file .env ecovoyage-app
Open your browser and access the application at: http://localhost:8000

📂 Project Structure
Plaintext
ECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH/
│
├── backend.py            # LangGraph multi-agent logic & Neon DB integration
├── app.py                # FastAPI application entrypoint
├── Dockerfile            # Container configuration file
├── .dockerignore         # Files to ignore during docker build
├── requirements.txt      # Project dependencies
├── tools/                # Custom tool modules (Flight & Tavily search)
├── templates/            # HTML frontend templates (index.html)
└── static/               # CSS styles and JavaScript files
🛡️ License
This project is developed as an advanced AI engineering solution for sustainable tourism and tech competitions. Feel free to use and adapt!
