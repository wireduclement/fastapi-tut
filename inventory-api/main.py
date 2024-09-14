from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn


app = FastAPI()

class Item(BaseModel):
   name: str
   brand: str
   qty: Optional[int] = None


class UpdateItem(BaseModel):
   name: Optional[str] = None
   brand: Optional[str] = None
   qty: Optional[int] = None


inventory = {}


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
   if item_id in inventory:
      return {"Error": "Item ID already exist"}
   
   inventory[item_id] = item
   return inventory[item_id]


@app.get("/get-by-id/{item_id}")
def get_item(item_id: int):
   if item_id not in inventory:
      return {"Error": "No item which such item ID"}
   
   return inventory[item_id]


@app.get("/get-by-name")
def get_item(name: str):
   for item_id in inventory:
      if inventory[item_id].name == name:
         return inventory[item_id]
      
   return {"Error": "No item which such item name"}
   

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
   if item_id not in inventory:
      return {"Error": "ID not found"}
   
   if item.name != None:
      inventory[item_id].name = item.name

   if item.brand != None:
      inventory[item_id].brand = item.brand

   if item.qty != None:
      inventory[item_id].qty = item.qty

   return inventory[item_id]


@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int):
   if item_id not in inventory:
      return {"Error": "No data found with such ID"}
   
   del inventory[item_id]


if __name__ == "__main__":
   uvicorn.run("main:app", reload=True)