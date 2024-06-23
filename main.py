from fastapi import FastAPI
from api.v1 import user_router, category_router, exercise_router

app = FastAPI(
    title="LiftMoreAPI", 
    description="API specification for the LiftMore app.")

app.include_router(user_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(exercise_router, prefix="/api/v1")


@app.get("/healthCheck")
async def root():
    return "Healthy"