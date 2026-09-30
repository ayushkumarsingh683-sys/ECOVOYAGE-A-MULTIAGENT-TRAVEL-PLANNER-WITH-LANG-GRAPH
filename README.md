🌍 EcoVoyage: Multi-Agent AI Sustainable Travel PlannerEcoVoyage is an intelligent, multi-agent travel planning assistant designed to curate sustainable, budget-friendly, and eco-conscious itineraries. Powered by LangGraph and Groq AI, it automates flight searches, eco-friendly hotel curation, carbon footprint analysis, and structured itinerary generation while ensuring persistent data storage using Neon PostgreSQL.🚀 Key FeaturesMulti-Agent Architecture: Collaborative specialized agents handling flight lookup, eco-stays, carbon emission analysis, and itinerary compilation.Real-Time Web Search: Integrated with Tavily Search to fetch live, up-to-date eco-friendly hotel recommendations and travel insights.Carbon Footprint Assessment: Evaluates environmental impact and provides actionable low-carbon recommendations.Cloud Database Persistence: Automatically saves generated travel plans and user threads securely into Neon Cloud PostgreSQL.Dockerized Deployment: Ready-to-deploy containerized structure for seamless running across environments.Clean Markdown & UI: Outputs structured, readable itineraries preventing layout breaks.🛠️ Tech Stack & DependenciesCategoryTechnology / LibraryDescriptionBackend FrameworkFastAPI, PythonHigh-performance async web framework for API endpoints.OrchestrationLangGraph (StateGraph, MemorySaver)Multi-agent state machine and conversation memory management.LLM ProviderGroq API (ChatGroq)Ultra-fast LLM inference using optimized open models.DatabaseNeon PostgreSQL, SQLAlchemyServerless cloud relational database with ORM mapping.Search & ToolsTavily API, Custom Flight ToolsExternal web search and flight transit data retrieval.ContainerizationDockerPackaging the application for reliable deployment.Frontend UIHTML5, CSS3, JavaScriptClean, responsive user interface for interaction.🤖 Multi-Agent WorkflowFlight Agent (flight_agent): Fetches available flights and transit options matching user criteria.Hotel Agent (hotel_agent): Searches for sustainable and eco-friendly accommodations via Tavily.Eco Agent (eco_agent): Computes estimated carbon footprints and provides green recommendations.Itinerary Agent (itinerary_agent): Builds a comprehensive, practical, and budget-aware schedule.Final Agent (final_agent): Formulates the clean, structured final markdown layout displayed to the user.⚙️ Getting Started & InstallationOption A: Running Locally (Virtual Environment)1. Clone the RepositoryBashgit clone https://github.com/ayushkumarsingh683-sys/ECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH.git
cd ECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH
2. Create and Activate Virtual EnvironmentBashpython -m venv travel
# On Windows:
.\travel\Scripts\Activate
3. Install DependenciesBashpip install -r requirements.txt
4. Configure Environment VariablesCreate a .env file in the root directory and add your credentials:Code snippetGROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://your_neon_postgres_connection_string
TAVILY_API_KEY=your_tavily_api_key_here
5. Run the ApplicationStart the FastAPI backend server using Uvicorn:Bashuvicorn app:app --reload
Open your browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)Option B: Running with Docker 🐳If you prefer to run the application inside a Docker container:1. Build the Docker ImageBashdocker build -t ecovoyage-app .
2. Run the Docker ContainerMake sure to pass your .env file variables while running the container:Bashdocker run -d -p 8000:8000 --env-file .env ecovoyage-app
Open your browser and access the application at: http://localhost:8000📂 Project StructurePlaintextECOVOYAGE-A-MULTIAGENT-TRAVEL-PLANNER-WITH-LANG-GRAPH/
│
├── backend.py            # LangGraph multi-agent logic & Neon DB integration
├── app.py                # FastAPI application entrypoint
├── Dockerfile            # Container configuration file
├── .dockerignore         # Files to ignore during docker build
├── requirements.txt      # Project dependencies
├── tools/                # Custom tool modules (Flight & Tavily search)
├── templates/            # HTML frontend templates (index.html)
└── static/               # CSS styles and JavaScript files
🛡️ LicenseThis project is developed as an advanced AI engineering solution for sustainable tourism and tech competitions. Feel free to use and adapt!
