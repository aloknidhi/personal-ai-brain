from fastapi import FastAPI
from app.api import auth, sources, conversations, analysis, knowledge, planner, activities, imports
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal AI Brain", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(sources.router, prefix="/api/v1/sources", tags=["Data Sources"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["Conversations"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["Knowledge"])
app.include_router(planner.router, prefix="/api/v1/plans", tags=["Study Planner"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["Activities"])
app.include_router(imports.router, prefix="/api/v1/imports", tags=["Import"])


@app.get("/")
def root():
    return {"message": "Personal AI Brain API v1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
