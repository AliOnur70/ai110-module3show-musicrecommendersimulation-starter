"""Simple, explainable music recommendations based on song features."""

import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple

DEFAULT_WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5}


@dataclass
class Song:
    """Store a song and the features available in our catalog."""
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
    """Store a listener's favorite genre, mood, and sound preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Offer a class-based interface using the same scoring rule as the CLI."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the highest-scoring songs without changing the original list."""
        prefs = self._prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(prefs, asdict(song))[0],
            reverse=True,
        )
        return ranked[:max(0, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain which parts of a song fit the user's preferences."""
        _, reasons = score_song(self._prefs(user), asdict(song))
        return "; ".join(reasons) or "No preferences were provided"

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        """Convert the class profile to the dictionary used by scoring."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }


def load_songs(csv_path: str) -> List[Dict]:
    """Read the catalog as dictionaries with numbers converted from CSV text."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for feature in ("energy", "valence", "danceability", "acousticness"):
                row[feature] = float(row[feature])
            songs.append(row)
    return songs


def score_song(
    user_prefs: Dict, song: Dict, weights: Optional[Dict[str, float]] = None
) -> Tuple[float, List[str]]:
    """Give one song a weighted relevance score and readable reasons."""
    points = dict(DEFAULT_WEIGHTS)
    if weights is not None:
        points.update(weights)
    score = 0.0
    reasons = []
    genre = user_prefs.get("genre", user_prefs.get("favorite_genre"))
    mood = user_prefs.get("mood", user_prefs.get("favorite_mood"))
    energy = user_prefs.get("energy", user_prefs.get("target_energy"))

    if genre and genre.strip().lower() == song["genre"].strip().lower():
        score += points["genre"]
        reasons.append(f"genre match (+{points['genre']:.2f})")
    if mood and mood.strip().lower() == song["mood"].strip().lower():
        score += points["mood"]
        reasons.append(f"mood match (+{points['mood']:.2f})")
    if energy is not None:
        # The closer the two energies are, the closer this value gets to 1.
        similarity = max(0.0, 1.0 - abs(float(energy) - float(song["energy"])))
        bonus = points["energy"] * similarity
        score += bonus
        reasons.append(f"energy similarity (+{bonus:.2f})")
    if "likes_acoustic" in user_prefs:
        acousticness = float(song["acousticness"])
        fit = acousticness if user_prefs["likes_acoustic"] else 1.0 - acousticness
        bonus = points["acoustic"] * fit
        score += bonus
        reasons.append(f"acoustic preference (+{bonus:.2f})")
    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score, and return the top k explanations."""
    ranked = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        ranked.append((song, score, "; ".join(reasons)))
    # sorted() returns a new list, so the original catalog stays unchanged.
    ranked = sorted(ranked, key=lambda result: result[1], reverse=True)
    return ranked[:max(0, k)]
