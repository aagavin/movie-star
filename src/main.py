from typing import Optional
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from .routes.media import mediaRouter


app: FastAPI = FastAPI(default_response_class=UJSONResponse)

app.include_router(mediaRouter)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
