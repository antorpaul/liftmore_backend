from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import user_router, category_router, exercise_router
from api.v1.routine_template_router import routine_template_router

app = FastAPI(
    title="LiftMoreAPI", 
    description="API specification for the LiftMore app.")

origins = [
    "http://localhost:3000",
    "http://10.8.62.184"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(exercise_router, prefix="/api/v1")
app.include_router(routine_template_router, prefix="/api/v1")

@app.get("/healthCheck")
async def root():
    return "Healthy"