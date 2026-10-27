import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Point weights, ordered to match "How The System Works": genre > mood > energy
GENRE_WEIGHT = 3.0
MOOD_WEIGHT = 2.0
ENERGY_WEIGHT = 1.0      # scaled by closeness, so 0.0 to 1.0 points
ACOUSTIC_WEIGHT = 0.5    # small bonus for acoustic fans
ACOUSTIC_THRESHOLD = 0.6

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = _profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return "; ".join(reasons) if reasons else "No strong match with your preferences"

def _profile_to_prefs(user: UserProfile) -> Dict:
    """Converts a UserProfile into the dict format used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, newline="", encoding="utf-8") as f:
        songs = []
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_WEIGHT
        reasons.append(f"matches your favorite genre: {song['genre']} (+{GENRE_WEIGHT:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_WEIGHT
        reasons.append(f"matches your mood: {song['mood']} (+{MOOD_WEIGHT:.1f})")

    if "energy" in user_prefs:
        # Reward closeness to the target, not higher or lower energy
        closeness = 1 - abs(song["energy"] - user_prefs["energy"])
        points = ENERGY_WEIGHT * closeness
        score += points
        reasons.append(f"energy {song['energy']:.2f} is close to your target {user_prefs['energy']:.2f} (+{points:.2f})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] >= ACOUSTIC_THRESHOLD:
        score += ACOUSTIC_WEIGHT
        reasons.append(f"acoustic sound you like (+{ACOUSTIC_WEIGHT:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
