from fastapi import FastAPI
from app.db.db_async import lifespan
from app.routes import user_routes #, reservation_routes

app = FastAPI(
    title="Restaurant Reservation API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_routes.router)
#app.include_router(reservation_routes.router)

@app.get("/")
async def root():
    return {"message": "FastAPI + Async PyMongo API is running 🚀"}
