from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.api.v1.routers import router
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_pinecone import PineconeVectorStore

from sqlalchemy import create_engine
from app.schemas.application.api_db_schema import DbUser, chatThreads, chatLists
engine = create_engine("postgresql://postgres:vishal@localhost:5432/UserDatabase")

@asynccontextmanager
async def lifespan(app: FastAPI):
    DbUser.metadata.create_all(bind=engine)
    chatThreads.metadata.create_all(bind=engine)
    chatLists.metadata.create_all(bind=engine)
    embedding = SentenceTransformer("all-MiniLM-L6-v2")
    app.state.embedding_model = embedding
    pc = Pinecone(api_key="YOUR_API_KEY")
    db = PineconeVectorStore(
        embedding=embedding,
        index=pc.Index("communitiesvectordb")
    )
    app.state.vdatabase = db
    yield

def load_app()->FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name, version="1.0", lifespan=lifespan ,docs_url="/docs" )
    application.add_middleware(CORSMiddleware, 
        allow_origins=["*"],
        allow_methods=["*"], 
        allow_headers=["*"],
    )
    application.include_router(router)
    return application

app = load_app()

if __name__ == "__main__":
    uvicorn.run("backend-app.app.main:app", host="0.0.0.0",port=8000, reload=True ) 