from fastapi import FastAPI

from app.database import Base, engine
from app.routers.feedback import router as feedback_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Technician Feedback API", version="0.1.0")
app.include_router(feedback_router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
