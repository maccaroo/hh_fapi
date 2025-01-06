from fastapi import FastAPI
from app.routes import items, root
from app.db import database

app = FastAPI()


# Routers
app.include_router(root.router)
app.include_router(items.router)


# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
