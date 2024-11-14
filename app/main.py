from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    def __init__(self, name: str, price: float, description: str = None):
        self.name = name
        self.price = price
        self.description = description

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/")
def create_item(item: Item):
    print(f'received item: {item}')
    return {"item_received": item}