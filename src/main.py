from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.responses import UJSONResponse
from .routes.media import mediaRouter


app: FastAPI = FastAPI(
    name="Movie Star",
    description="media stuff",
    version="0.0.1",
    default_response_class=UJSONResponse
)

app.include_router(mediaRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def read_root():
    routes = []
    for r in app.routes:
        if type(r) == APIRoute:
            routes.append(r.path)
    return {
        "paths": routes,
        "Hello": "World"
    }
