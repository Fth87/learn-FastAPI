from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Item(BaseModel):
    name: str = None
    is_done: bool = False

app = FastAPI()
items = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items")
async def create_item(item: Item):
    items.append(item)
    return items
  
@app.get("/items", response_model=list[Item])
async def list_items(limit: int = 10):
    return items[:limit]
  

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int)->Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
      
      
@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id < len(items):
        del items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
      
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < len(items):
        items[item_id] = item
        return item
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")