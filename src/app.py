from fastapi import FastAPI

from src.routers import goal_routers

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


app.include_router(goal_routers.router)
