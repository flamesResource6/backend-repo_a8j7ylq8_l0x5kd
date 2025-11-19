from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents, db
from schemas import ContactMessage

app = FastAPI(title="Elev8 API", description="Backend for Elev8 AI upskilling platform", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health
@app.get("/")
def root():
    return {"status": "ok", "service": "elev8-api"}

# Test DB connection helper
@app.get("/test")
def test_db():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    try:
        # simple ping by counting collections
        _ = db.list_collection_names()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# In-memory course list for demo display (no writes). Real persistence can be added later if needed.
COURSES = [
    {
        "id": "genai-pro",
        "title": "Generative AI for Professionals",
        "level": "Intermediate",
        "duration": "6 weeks",
        "color": "purple",
        "tag": "Popular",
        "modules": 8
    },
    {
        "id": "mlops-essentials",
        "title": "MLOps Essentials",
        "level": "Advanced",
        "duration": "4 weeks",
        "color": "orange",
        "tag": "New",
        "modules": 6
    },
    {
        "id": "prompt-engineering",
        "title": "Prompt Engineering Mastery",
        "level": "Beginner",
        "duration": "3 weeks",
        "color": "pink",
        "tag": "Trending",
        "modules": 5
    },
    {
        "id": "ai-product-mgmt",
        "title": "AI Product Management",
        "level": "Intermediate",
        "duration": "5 weeks",
        "color": "blue",
        "tag": "Team Favorite",
        "modules": 7
    }
]

@app.get("/courses")
def list_courses():
    return {"courses": COURSES}

# Blog list sample (read-only for now)
BLOGS = [
    {
        "id": "industry-ai-trends-2025",
        "title": "Industry AI Trends 2025",
        "excerpt": "From copilots to autonomous workflows, here’s what’s next.",
        "tag": "Insights"
    },
    {
        "id": "roi-of-ai-upskilling",
        "title": "The ROI of AI Upskilling",
        "excerpt": "How teams accelerate delivery and reduce costs with the right skills.",
        "tag": "Research"
    },
    {
        "id": "governance-guardrails",
        "title": "Governance & Guardrails for Enterprise GenAI",
        "excerpt": "Balancing innovation with risk and compliance.",
        "tag": "Enterprise"
    }
]

@app.get("/blogs")
def list_blogs():
    return {"posts": BLOGS}

# Contact form endpoint - persists to DB
@app.post("/contact")
def submit_contact(msg: ContactMessage):
    try:
        doc_id = create_document("contactmessage", msg)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
