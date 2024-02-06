from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None

@app.get("/print")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_description": item.description}

@app.post("/dendrite/")
async def post_dendrite(synapse: dict):
    print('dendrite synapse', synapse)
    return { "synapse": synapse}
