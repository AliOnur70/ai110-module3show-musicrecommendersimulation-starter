"""Extra checks for the CSV reader, ranking, and weighting experiment."""

import csv

import pytest

from src.recommender import load_songs, recommend_songs, score_song


def test_load_songs_converts_csv_numbers(tmp_path):
    path = tmp_path / "songs.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "title", "artist", "genre", "mood", "energy", "tempo_bpm", "valence", "danceability", "acousticness"])
        writer.writerow([1, "Example", "Someone", "pop", "happy", 0.8, 120, 0.9, 0.7, 0.2])
    song = load_songs(str(path))[0]
    assert song["id"] == 1 and isinstance(song["id"], int)
    assert song["tempo_bpm"] == 120.0
    assert isinstance(song["energy"], float)


def test_scoring_returns_reasons_and_rewards_closeness():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song(prefs, songs[0])
    assert score == pytest.approx(3.98)
    assert len(reasons) == 3
    assert "genre match" in reasons[0]
    assert score_song(prefs, songs[0])[0] > score_song(prefs, songs[4])[0]


def test_ranking_does_not_modify_catalog_and_respects_k():
    songs = load_songs("data/songs.csv")
    original_titles = [song["title"] for song in songs]
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35}
    results = recommend_songs(prefs, songs, k=3)
    assert [song["title"] for song, _, _ in results[:2]] == ["Library Rain", "Midnight Coding"]
    assert len(results) == 3
    assert all(results[i][1] >= results[i + 1][1] for i in range(2))
    assert [song["title"] for song in songs] == original_titles
    assert recommend_songs(prefs, songs, k=0) == []


def test_weight_experiment_changes_pop_ranking():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    old_titles = [s["title"] for s, _, _ in recommend_songs(prefs, songs, k=5)]
    new_titles = [s["title"] for s, _, _ in recommend_songs(prefs, songs, k=5, weights={"genre": 1.0, "energy": 2.0})]
    assert old_titles != new_titles
    assert old_titles[0] == new_titles[0] == "Sunrise City"


def test_acoustic_preference_affects_score():
    songs = load_songs("data/songs.csv")
    song = next(s for s in songs if s["title"] == "Late Afternoon")
    base = {"genre": "acoustic", "mood": "chill", "energy": 0.33}
    acoustic = score_song({**base, "likes_acoustic": True}, song)[0]
    not_acoustic = score_song({**base, "likes_acoustic": False}, song)[0]
    assert acoustic > not_acoustic
