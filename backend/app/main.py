from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.core.database import init_models

app = FastAPI(title="TinyURL Python")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_models()
    print("Database models initialized")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(router)
