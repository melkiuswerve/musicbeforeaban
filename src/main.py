
#uvicorn src.main:app --reload

from fastapi import FastAPI
from src.api import user, auth
app = FastAPI()

app.include_router(user.router)

app.include_router(auth.router)


