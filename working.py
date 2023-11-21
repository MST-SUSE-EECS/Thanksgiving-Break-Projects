from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):  
    name: str
    price: float
    brand: Optional[str] = None

inventory = {
    1: {
        "name": "Milk",
        "price": 3.99,
        "brand": "Regular",
    }
}

@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    return inventory[item_id]

@app.get("/get-by-name")
def get_item_by_name(name: str = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item Id already exists")
    inventory[item_id] = item.dict()  
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory[item_id] = item.dict()
    return inventory[item_id]

@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    del inventory[item_id]
    return {"detail": "Item deleted"}
