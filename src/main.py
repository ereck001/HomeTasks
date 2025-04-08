import uvicorn
from fastapi import FastAPI

from controllers import account_controller, product_controller, task_controller

app = FastAPI()
app.include_router(product_controller.router)
app.include_router(task_controller.router)
app.include_router(account_controller.router)


@app.get("/")
def health_check():
    return {"health": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
