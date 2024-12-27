from fastapi import FastAPI
from fastapi import FastAPI
from app.routers import suggestions

app = FastAPI(
    title="Room Finder API",
    description="""
    # Room Finder API

    This API allows users to find and reserve rooms based on their preferences. Users can input their budget, desired check-in and check-out dates, preferred neighborhood, and the importance of each preference. The API will then suggest rooms sorted based on how well they match the user's preferences.

    ## Endpoints

    - **POST /suggestions/**: Get room suggestions based on user preferences.
    - **POST /suggestions/reserve/{listing_id}**: Reserve a room by listing ID.
    """,
    version="1.0.0",
    contact={
        "name": "ali",
        "email": "khavanin.a2015@gmail.com",
    },
)

# Include the suggestions router
app.include_router(suggestions.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
