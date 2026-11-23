"""Run the music recommendation examples from the command line."""

from .recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.80},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    "Conflicting Preferences": {"genre": "rock", "mood": "sad", "energy": 0.15},
}


def main() -> None:
    """Load songs and print five explained recommendations for each profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for label, preferences in PROFILES.items():
        print(f"\n=== {label} ===")
        print(
            f"Profile: genre={preferences['genre']}, "
            f"mood={preferences['mood']}, energy={preferences['energy']:.2f}"
        )
        for place, (song, score, explanation) in enumerate(
            recommend_songs(preferences, songs, k=5), start=1
        ):
            print(f"{place}. {song['title']} - {song['artist']} | Score: {score:.2f}")
            print(f"   Why: {explanation}")


if __name__ == "__main__":
    main()
