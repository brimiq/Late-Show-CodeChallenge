"""
Database Seeding Script

This script populates the database with sample data for development
and testing purposes. It creates sample episodes, guests, and appearances.

Usage:
    python seed.py

Note: If you have a CSV file (guest_data.csv), this script will attempt
to read it and use it for guest data. Otherwise, it uses sample data.
"""

import csv
import os
from app import app
from models import db, Episode, Guest, Appearance


def seed_database():
    """
    Main function to seed the database with sample data
    
    This function:
    1. Clears existing data (optional - comment out if you want to preserve)
    2. Creates sample episodes
    3. Creates sample guests (from CSV if available, otherwise sample data)
    4. Creates sample appearances
    """
    
    with app.app_context():
        # Optional: Clear existing data
        # Uncomment the following lines to start fresh
        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()
        
        print("Creating sample episodes...")
        
        # Create sample episodes
        episodes = [
            Episode(date="1/11/99", number=1),
            Episode(date="1/12/99", number=2),
            Episode(date="1/13/99", number=3),
            Episode(date="1/14/99", number=4),
            Episode(date="1/15/99", number=5),
            Episode(date="1/18/99", number=6),
            Episode(date="1/19/99", number=7),
            Episode(date="1/20/99", number=8),
            Episode(date="1/21/99", number=9),
            Episode(date="1/22/99", number=10),
        ]
        
        # Add all episodes to the session
        for episode in episodes:
            db.session.add(episode)
        
        # Commit to get episode IDs
        db.session.commit()
        
        print(f"Created {len(episodes)} episodes")
        
        # Check for CSV file and load guest data if available
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'guest_data.csv')
        
        guests = []
        
        if os.path.exists(csv_path):
            print(f"Loading guest data from CSV file: {csv_path}")
            try:
                with open(csv_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        guest = Guest(
                            name=row.get('name', '').strip(),
                            occupation=row.get('occupation', '').strip()
                        )
                        guests.append(guest)
                        db.session.add(guest)
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                print("Using sample guest data instead...")
                guests = create_sample_guests()
        else:
            print("No CSV file found. Using sample guest data...")
            guests = create_sample_guests()
        
        # Commit guests to get their IDs
        db.session.commit()
        
        print(f"Created {len(guests)} guests")
        
        # Create sample appearances
        print("Creating sample appearances...")
        
        appearances = [
            # Episode 1 appearances
            Appearance(rating=4, guest_id=1, episode_id=1),
            Appearance(rating=5, guest_id=2, episode_id=1),
            Appearance(rating=3, guest_id=3, episode_id=1),
            
            # Episode 2 appearances
            Appearance(rating=5, guest_id=3, episode_id=2),
            Appearance(rating=4, guest_id=4, episode_id=2),
            Appearance(rating=5, guest_id=5, episode_id=2),
            
            # Episode 3 appearances
            Appearance(rating=4, guest_id=1, episode_id=3),
            Appearance(rating=3, guest_id=6, episode_id=3),
            Appearance(rating=5, guest_id=7, episode_id=3),
            
            # Episode 4 appearances
            Appearance(rating=4, guest_id=2, episode_id=4),
            Appearance(rating=5, guest_id=8, episode_id=4),
            
            # Episode 5 appearances
            Appearance(rating=3, guest_id=4, episode_id=5),
            Appearance(rating=4, guest_id=5, episode_id=5),
            Appearance(rating=5, guest_id=6, episode_id=5),
            
            # Episode 6 appearances
            Appearance(rating=5, guest_id=1, episode_id=6),
            Appearance(rating=4, guest_id=3, episode_id=6),
            
            # Episode 7 appearances
            Appearance(rating=3, guest_id=7, episode_id=7),
            Appearance(rating=5, guest_id=8, episode_id=7),
            Appearance(rating=4, guest_id=2, episode_id=7),
            
            # Episode 8 appearances
            Appearance(rating=4, guest_id=5, episode_id=8),
            Appearance(rating=5, guest_id=6, episode_id=8),
            
            # Episode 9 appearances
            Appearance(rating=3, guest_id=1, episode_id=9),
            Appearance(rating=4, guest_id=4, episode_id=9),
            Appearance(rating=5, guest_id=7, episode_id=9),
            
            # Episode 10 appearances
            Appearance(rating=5, guest_id=3, episode_id=10),
            Appearance(rating=4, guest_id=8, episode_id=10),
        ]
        
        # Add all appearances to the session
        for appearance in appearances:
            db.session.add(appearance)
        
        # Commit all changes
        db.session.commit()
        
        print(f"Created {len(appearances)} appearances")
        
        print("\n✅ Database seeding completed successfully!")
        print(f"   - {len(episodes)} episodes")
        print(f"   - {len(guests)} guests")
        print(f"   - {len(appearances)} appearances")


def create_sample_guests():
    """
    Create sample guest data if CSV file is not available
    
    Returns:
        list: List of Guest objects
    """
    sample_guests = [
        Guest(name="Michael J. Fox", occupation="actor"),
        Guest(name="Sandra Bernhard", occupation="Comedian"),
        Guest(name="Tracey Ullman", occupation="television actress"),
        Guest(name="Bradley Whitford", occupation="actor"),
        Guest(name="Janeane Garofalo", occupation="comedian"),
        Guest(name="William Baldwin", occupation="actor"),
        Guest(name="John Turturro", occupation="actor"),
        Guest(name="Minnie Driver", occupation="actress"),
    ]
    
    for guest in sample_guests:
        db.session.add(guest)
    
    return sample_guests


if __name__ == '__main__':
    seed_database()

