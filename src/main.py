from typing import Union

import uvicorn
from fastapi import FastAPI

from controllers import product_controller, task_controller
from repositories import get_conn
from repositories.products import get_prods_to_buy
from repositories.tasks import get_tasks

app = FastAPI()
app.include_router(product_controller.router)
app.include_router(task_controller.router)


@app.get("/")
def health_check():
    return {"health": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
