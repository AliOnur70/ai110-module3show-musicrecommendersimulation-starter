"""Compare original and experimental scoring weights for one listener."""

from .recommender import load_songs, recommend_songs

POP_PROFILE = {"genre": "pop", "mood": "happy", "energy": 0.80}
EXPERIMENT_WEIGHTS = {"genre": 1.0, "energy": 2.0}


def main() -> None:
    """Print the baseline and weight-shifted rankings side by side."""
    songs = load_songs("data/songs.csv")
    for label, weights in (("Baseline", None), ("Energy-focused experiment", EXPERIMENT_WEIGHTS)):
        print(f"\n{label}:")
        for place, (song, score, _) in enumerate(
            recommend_songs(POP_PROFILE, songs, k=5, weights=weights), start=1
        ):
            print(f"{place}. {song['title']} ({score:.2f})")


if __name__ == "__main__":
    main()
