from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
app= FastAPI()
# @app.get("/")
# def root():
#     return {"message":"HEllo!"}
#Pydantic Models help in data orgstructuring and documentation
items=[]
class Item(BaseModel):
    text: str=None
    is_done: bool=False

@app.post("/items")
def greet_user(item: Item):
    items.append(item)
    return items

@app.get("/items_cart/{item_id}")
def get_item(item_id:int)-> Item:
    item=items[item_id]
    if item_id > len(items):
        return item
    else:
        raise HTTPException(status_code=404,detail=f"Invalid Item Not Found!")
