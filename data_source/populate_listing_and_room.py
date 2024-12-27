import csv
import os
from sqlalchemy.exc import SQLAlchemyError

# Adjust these imports based on your actual project structure:
from app.db import SessionLocal
from models.listing import Listing
from models.room import Room

def populate_listings_and_rooms(csv_file_path: str):
    """
    Populate the 'listings' and 'room' tables from the CSV file.

    Mapping (according to your specification):
    - 'listings' table:
        listing_id -> airbnb_id
        name -> airbnb_name
        price -> price
        host_id -> host_id
        neighbourhood -> neigh_num (foreign key to neighbourhood)
    - 'room' table:
        listing_id -> airbnb_id (foreign key to listings)
        host_id -> host_id
        room_type -> room_type
    """

    db = SessionLocal()
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows_processed = 0
            new_listings = 0
            new_rooms = 0

            for row in reader:
                rows_processed += 1

                # Extract required fields from each row:
                try:
                    airbnb_id = int(row["listing_id"])
                    airbnb_name = row["name"].strip()
                    price = int(row["price"])
                    host_id = int(row["host_id"])
                    neigh_num = int(row["neighbourhood"])  # Foreign key to 'neighbourhood'
                    room_type = row["room_type"].strip()

                except (ValueError, KeyError) as e:
                    print(f"Skipping row {rows_processed}: Unable to parse required fields ({e})")
                    continue

                # 1) Create or Skip Listing
                existing_listing = db.query(Listing).filter_by(airbnb_id=airbnb_id).first()
                if not existing_listing:
                    listing = Listing(
                        airbnb_id=airbnb_id,
                        airbnb_name=airbnb_name,
                        price=price,
                        host_id=host_id,
                        neigh_num=neigh_num
                    )
                    db.add(listing)
                    new_listings += 1

                # 2) Create or Skip Room
                existing_room = db.query(Room).filter_by(airbnb_id=airbnb_id).first()
                if not existing_room:
                    room = Room(
                        airbnb_id=airbnb_id,
                        host_id=host_id,
                        room_type=room_type
                    )
                    db.add(room)
                    new_rooms += 1

            # Commit all changes after processing the CSV
            db.commit()
            print(f"Processed {rows_processed} rows.")
            print(f"New listings added: {new_listings}")
            print(f"New rooms added: {new_rooms}")

    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":

    csv_file_path = "finallisting.csv"

    if not os.path.isfile(csv_file_path):
        print(f"CSV file does not exist: {csv_file_path}")
    else:
        populate_listings_and_rooms(csv_file_path)