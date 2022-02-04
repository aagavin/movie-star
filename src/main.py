from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from .routes.media import mediaRouter


app: FastAPI = FastAPI(default_response_class=UJSONResponse)

app.include_router(mediaRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
