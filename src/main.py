"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import csv
import random

from recommender import load_songs, recommend_songs


def make_random_profile(csv_path: str) -> dict:
    """Builds a realistic user profile by basing it on a randomly chosen song from the catalog."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    seed = random.choice(rows)

    # Nudge energy slightly so the seed song isn't always a perfect match
    energy = float(seed["energy"]) + random.uniform(-0.1, 0.1)

    return {
        "genre": seed["genre"],
        "mood": seed["mood"],
        "energy": round(min(max(energy, 0.0), 1.0), 2),
        "likes_acoustic": float(seed["acousticness"]) > 0.5,
    }


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Random profile drawn from the genres and moods in songs.csv
    user_prefs = make_random_profile("data/songs.csv")
    print(f"User profile: {user_prefs}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
