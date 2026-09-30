🌍 EcoVoyage: Multi-Agent AI Sustainable Travel PlannerIntelligent, multi-agent assistant curating low-carbon, budget-conscious, and eco-friendly itineraries.📖 OverviewEcoVoyage is an advanced multi-agent travel planning system designed to promote sustainable tourism. Powered by LangGraph orchestrating specialized AI agents via Groq AI, it automates flight lookups, green hotel selections, carbon footprint calculations, and structured itinerary generation while persisting threads securely in Neon Cloud PostgreSQL.🌟 Key FeaturesMulti-Agent Collaboration: Specialized sub-agents working together to handle flights, eco-stays, emission tracking, and final itinerary compiling.Real-Time Web Intelligence: Integrated with Tavily Search for fetching live, verified eco-friendly lodging options.Carbon Footprint Assessment: Evaluates environmental impact metrics to suggest low-carbon alternatives.Cloud Persistence: Stores user sessions and trip configurations reliably using Neon PostgreSQL.Dockerized & Production-Ready: Packaged cleanly for consistent deployment across local machines and cloud servers.🏛️ Multi-Agent ArchitecturePlaintextUser Request ──► [Flight Agent] ──► [Hotel Agent] ──► [Eco Agent] ──► [Itinerary Agent] ──► [Final Response]
Flight Agent: Gathers transit and flight options matching user parameters.Hotel Agent: Searches for sustainable accommodations via Tavily.Eco Agent: Computes and evaluates carbon footprint outputs.Itinerary Agent: Organizes a balanced, budget-aware schedule.Final Agent: Renders a clean markdown layout for the frontend UI.🛠️ Tech StackComponentTechnologyBackend & APIFastAPI, PythonAI OrchestrationLangGraph (StateGraph, MemorySaver)LLM ProviderGroq API (ChatGroq)DatabaseNeon Cloud PostgreSQL, SQLAlchemyTools & SearchTavily Search API, Custom Flight ToolsContainerizationDocker, Docker ComposeFrontend UIHTML5, CSS3, JavaScript⚙️ Installation & SetupPrerequisitesPython 3.10+Docker Desktop (Optional, for containerized execution)1. Clone the RepositoryBashgit clone https://github.com/ayushkumarsingh683-sys/ECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH.git
cd ECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH
2. Configure Environment VariablesCreate a .env file in the root directory and add your keys:Code snippetGROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://your_neon_postgres_connection_string
TAVILY_API_KEY=your_tavily_api_key_here
Method A: Local Development SetupCreate and activate virtual environment:Bashpython -m venv travel
# Windows:
.\travel\Scripts\Activate
Install dependencies:Bashpip install -r requirements.txt
Run the application:Bashuvicorn app:app --reload
Access the app at: [http://127.0.0.1:8000](http://127.0.0.1:8000)Method B: Docker Deployment 🐳Build the Docker image:Bashdocker build -t ecovoyage-app .
Run the container:Bashdocker run -d -p 8000:8000 --env-file .env ecovoyage-app
Access the app at: http://localhost:8000📂 Project StructurePlaintextECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH/
│
├── backend.py            # LangGraph multi-agent logic & database handlers
├── app.py                # FastAPI application entrypoint & routes
├── Dockerfile            # Container build instructions
├── .dockerignore         # Excluded files for docker context
├── requirements.txt      # Python dependencies list
├── tools/                # Custom operational modules (Flight & Tavily)
├── templates/            # HTML frontend views (index.html)
└── static/               # Client-side styles (CSS) and scripts (JS)
🛡️ License & AcknowledgementsDeveloped as an advanced AI engineering solution for modern sustainable tech frameworks and competitive development.
