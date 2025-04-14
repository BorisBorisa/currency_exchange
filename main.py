import uvicorn
from fastapi import FastAPI

from app.api.endpoints import auth


app = FastAPI()
app.include_router(auth.auth_route)



@app.get("/")
async def main_page():
    return {"message": "Welcome user"}


if __name__ == '__main__':
    uvicorn.run(app)

