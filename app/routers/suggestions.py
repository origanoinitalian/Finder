from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app import schemas
from app.db import get_db
from models.listing import Listing
from models.neighborhood import Neighborhood
from models.room import Room

router = APIRouter(
    prefix="/suggestions",
    tags=["Suggestions"],
    responses={404: {"description": "Not found"}},
)

# explanation of db: Session = Depends(get_db) -> this is a dependency method meaning that it will wait until the get_db
# method is called and your endpoint has access to the database

# explanation response_model=schemas.SuggestionResponse : this is a response model meaning its a template for your response
# you can go to app/schemas/suggestions to see it

@router.post("/", response_model=schemas.SuggestionResponse, status_code=status.HTTP_200_OK)
def get_room_suggestions(preferences: schemas.PreferenceInput, db: Session = Depends(get_db)):
    """
    ## Get Room Suggestions Based on User Preferences

    This endpoint receives user preferences along with the importance coefficients for each preference.
    It returns a list of room suggestions sorted based on how well they match the user's preferences.

    **Request Body Example:**

    ```json
    {
        "budget": [250, 8],
        "check_in": ["2024-05-01", 7],
        "check_out": ["2024-05-10", 7],
        "neigh_name": ["Downtown", 10]
    }
    ```

    ### **Parameters:**

    - **budget**: A tuple where the first element is the maximum budget and the second is its importance coefficient (1-10).
    - **check_in**: A tuple where the first element is the desired check-in date and the second is its importance coefficient (1-10).
    - **check_out**: A tuple where the first element is the desired check-out date and the second is its importance coefficient (1-10).
    - **neigh_name**: A tuple where the first element is the preferred neighborhood name and the second is its importance coefficient (1-10).

    ### **Response:**

    - **suggestions**: A list of room suggestions sorted based on the calculated scores.

    ### **Implementation Notes:**

    - The ranking method queries the listings and rooms based on user preferences.
    - It calculates the difference between the ideal and available options for all attributes.
    - Rooms are sorted and returned to the user based on how well they match the preferences.

    ### **Bonus Features:**

    - The scores for each attribute are provided to give users insight into how each room was ranked.
    """
    # Extract preferences and their importance coefficients
    # todo : use this data to retrive the most relevant listings from your data base
    user_budget, budget_importance = preferences.budget
    user_check_in, check_in_importance = preferences.check_in
    user_check_out, check_out_importance = preferences.check_out
    user_neigh_name, neigh_importance = preferences.neigh_name

    # Validate dates (already handled by Pydantic)
    # Here, ensure that check_out is after check_in
    if user_check_out < user_check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date cannot be before check-in date."
        )

    # Fetch listings that are available (assuming 'availability' is a Boolean)
    available_listings = db.query(Listing).join(Neighborhood).filter(Room.airbnb_id == Listing.airbnb_id).all()

    suggestions = []

    for listing in available_listings:
        room = db.query(Room).filter(Room.airbnb_id == listing.airbnb_id).first()
        if not room:
            continue  # Skip if no corresponding room

        # Calculate scores based on preferences
        score = 0
        attribute_scores = {}

        # Budget Score
        price_diff = abs(user_budget - listing.price)
        budget_score = (1 / (1 + price_diff)) * budget_importance
        score += budget_score
        attribute_scores['budget'] = round(budget_score, 2)

        # Neighborhood Score


        # Check-in Score
        # Since availability dates are not stored, we'll assume all rooms are available
        # Alternatively, you can implement availability checks if you have the data
        check_in_score = check_in_importance * 10  # Placeholder
        score += check_in_score
        attribute_scores['check_in'] = round(check_in_score, 2)

        # Check-out Score
        check_out_score = check_out_importance * 10  # Placeholder
        score += check_out_score
        attribute_scores['check_out'] = round(check_out_score, 2)

        # Create RoomSuggestion object




    # Sort suggestions based on score in descending order


    # return schemas.SuggestionResponse(suggestions=sorted_suggestions)
    return {'suggestions': "a list of suggestions"}

@router.post("/reserve/{listing_id}", status_code=status.HTTP_200_OK)
def reserve_room(listing_id: int, db: Session = Depends(get_db)):
    """
    ## Reserve a Room

    This endpoint allows users to reserve a room by providing the `listing_id`.

    ### **Parameters:**

    - **listing_id**: The unique identifier of the listing to reserve.

    ### **Response:**

    - **message**: Confirmation message indicating the reservation status.

    ### **Implementation Notes:**

    - This is a placeholder implementation. You should integrate it with your reservation system.
    - Ensure that the room is available before confirming the reservation.
    """
    # Fetch the listing
    listing = db.query(Listing).filter(Listing.airbnb_id == listing_id).first()
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found."
        )

    # Fetch the room
    room = db.query(Room).filter(Room.airbnb_id == listing_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found."
        )

    # Placeholder for reservation logic
    # For example, updating availability, creating a reservation record, etc.
    # Here, we'll just return a success message

    return {"message": f"Room with listing_id {listing_id} has been successfully reserved."}