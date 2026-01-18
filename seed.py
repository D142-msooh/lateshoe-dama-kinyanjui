#!/usr/bin/env python3

from app import app
from models import db, Episode, Guest, Appearance
import csv

if __name__ == '__main__':
    with app.app_context():
        print("Clearing database...")
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()

        print("Seeding episodes...")
        episodes_data = []
        try:
            with open('episodes.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    episode = Episode(
                        id=int(row['id']),
                        date=row['date'],
                        number=int(row['number'])
                    )
                    episodes_data.append(episode)
            db.session.add_all(episodes_data)
        except FileNotFoundError:
            # fallback data if CSV not found
            episodes_data = [
                Episode(id=1, date="1/11/99", number=1),
                Episode(id=2, date="1/12/99", number=2),
                Episode(id=3, date="1/13/99", number=3),
            ]
            db.session.add_all(episodes_data)

        print("Seeding guests...")
        guests_data = [
            Guest(id=1, name="Michael J. Fox", occupation="actor"),
            Guest(id=2, name="Sandra Bernhard", occupation="Comedian"),
            Guest(id=3, name="Tracey Ullman", occupation="television actress"),
        ]
        db.session.add_all(guests_data)

        print("Seeding appearances...")
        appearances_data = [
            Appearance(id=1, rating=4, episode_id=1, guest_id=1),
            Appearance(id=2, rating=5, episode_id=2, guest_id=3),
        ]
        db.session.add_all(appearances_data)

        db.session.commit()
        print("Database seeded successfully!")
