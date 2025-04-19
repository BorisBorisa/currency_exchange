import uvicorn
from fastapi import FastAPI


from app.api.endpoints import registration, auth

from db.db_connecion import lifespan, get_database_connection


app = FastAPI(lifespan=lifespan)
app.include_router(registration.reg_route)
app.include_router(auth.auth)



@app.get("/")
async def main_page():
    return {"message": "Welcome user"}


if __name__ == '__main__':
    uvicorn.run(app)

