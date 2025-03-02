# from typing import Optional, Annotated
# import fastapi
# from typing import List
# from fastapi import Query
# from pydantic import BaseModel
# import uvicorn

# app = fastapi.FastAPI()


# class Item(BaseModel):
#     name: Annotated[str, "lowercase"]
#     description: Optional[str] = None
#     price: float
#     status: Optional[float] = 0


# application: List[Item] = []


# @app.get("/")
# def read_root() -> dict:
#     return {}


# @app.get("/items/")
# def read_items(limit: int = 10, skip: int = 0, q: Annotated[str | None, Query(alias="query")] = None) -> dict:
#     return {
#         'application_request': q,
#         'total': len(application),
#         'limit': limit,
#         'skip': skip,
#         'items': application[skip: skip+limit]
#     }


# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}


# @app.post("/items/")
# def create_item(item: Item):
#     application.append(item)
#     item.__setattr__("status", "created")
#     return item

# # if __name__ == "main":
# #     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
\
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results