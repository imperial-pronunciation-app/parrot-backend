from typing import Dict

from fastapi import FastAPI

from app.routers import routers


app = FastAPI()


@app.get("/")
def read_home() -> Dict[str, str]:  # would be a Pydantic return type normally
    return {"Hello": "James"}


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    pass
