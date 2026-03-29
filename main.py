from fastapi import FastAPI
from routes.assistant_routes import router
from db.database import engine
from db.models import Base

app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)






