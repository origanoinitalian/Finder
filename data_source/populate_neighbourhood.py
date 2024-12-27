# populate_neighbourhood.py

import csv
import os
from tqdm import tqdm
from app.db import SessionLocal
from models.neighborhood import Neighborhood

def populate_neighbourhoods(csv_file_path: str):
    """
    Populate the neighbourhood table with data from a CSV file.

    :param csv_file_path: Path to the CSV file containing neighbourhood data.
    """
    # Create a new database session
    db = SessionLocal()
    try:
        # First, count the total number of rows for the progress bar
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            total_rows = sum(1 for row in csvfile) - 1  # Subtract 1 for header
            csvfile.seek(0)  # Reset file pointer to the beginning

            reader = csv.DictReader(csvfile)
            entries_added = 0
            entries_skipped = 0

            # Initialize tqdm progress bar
            with tqdm(total=total_rows, desc="Populating Neighbourhoods", unit="row") as pbar:
                for row in reader:
                    try:
                        neigh_num = int(row['neigh_num'])
                        neigh_name = row['neighbourhood'].strip()
                        rank = int(row['rank'])

                        # Check if the neighbourhood already exists
                        existing = db.query(Neighborhood).filter(Neighborhood.neigh_num == neigh_num).first()
                        if existing:
                            print(f"Neighbourhood with neigh_num {neigh_num} already exists. Skipping.")
                            entries_skipped += 1
                            pbar.update(1)
                            continue

                        # Create a new Neighbourhood instance
                        neighbourhood = Neighborhood(
                            neigh_num=neigh_num,
                            neigh_name=neigh_name,
                            rank=rank
                        )

                        # Add to the session
                        db.add(neighbourhood)
                        entries_added += 1

                    except (ValueError, KeyError) as e:
                        print(f"Error processing row {row}: {e}")
                        entries_skipped += 1
                        continue

                    pbar.update(1)  # Update the progress bar for each processed row

        # Commit the session to persist data
        db.commit()
        print(f"\nPopulation complete: {entries_added} entries added, {entries_skipped} entries skipped.")

    except FileNotFoundError:
        print(f"CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Define the path to the CSV file
    csv_file_path ='neighranked.csv'

    # Check if the file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found at {csv_file_path}")
    else:
        populate_neighbourhoods(csv_file_path)