# Music Recommender Simulation

## Project Summary

This project is a small music recommendation system I made in Python. It compares a listener's taste with a catalog of songs and recommends the best matches. It does not use machine learning or real listening histories. Instead, each song gets a simple score, and the program explains where that score came from.

## How The System Works

Real apps like Spotify and YouTube can use **collaborative filtering** (patterns from listeners with similar habits) and **content-based filtering** (things about the music itself). Likes, skips, repeat plays, and playlists provide clues about what someone enjoys. My simulation uses content-based filtering because the starter CSV has song descriptions but no real user activity.

- **Song data:** ID, title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness. Energy, valence, danceability, and acousticness are values from 0 to 1. Tempo is measured in beats per minute.
- **User preferences:** favorite genre, favorite mood, and target energy from 0 to 1. The `UserProfile` class also stores whether the listener likes acoustic music.
- **Features used for the score:** genre, mood, energy, and optionally acousticness. The other features are saved for possible improvements later.

### My algorithm recipe

| Feature | Rule |
| --- | --- |
| Genre | Add **2.0** points for an exact genre match. |
| Mood | Add **1.0** point for an exact mood match. |
| Energy | Add `1.0 - abs(song_energy - target_energy)` points, with a minimum of 0. |
| Acousticness | For class-based profiles, optionally add up to **0.5** points based on the user's acoustic preference. |

For example, **Sunrise City** is pop/happy with energy 0.82. A pop/happy listener who wants energy 0.80 gives it `2 + 1 + (1 - |0.82 - 0.80|) = 3.98` points.

A **scoring rule** judges one song. A **ranking rule** scores every song, sorts the songs from highest to lowest, and returns the top `k`. I used `sorted()` rather than changing the original catalog with `.sort()`. Ties keep their original CSV order.

```text
Input: songs.csv + listener's preferences
                 |
                 v
        Read song dictionaries
                 |
                 v
     Score each song + save reasons
                 |
                 v
      Sort by score (high to low)
                 |
                 v
     Output: Top 5 songs with reasons
```

A possible weakness is that the 2-point genre bonus can be stronger than the actual vibe. For example, somebody asking for sad, low-energy rock may still receive a loud rock track first.

## Getting Started

Run commands from the project root directory. The recommender uses Python's built-in CSV library, so there are no extra packages needed just to run it.

```bash
python -m src.main
```

This prints five recommendations for each of four listener profiles. To run the scoring experiment:

```bash
python -m src.evaluate
```

To run all the tests, install `pytest` if it is not already installed, then run:

```bash
python -m pip install pytest
python -m pytest -q
```

The starter repository also includes `requirements.txt` for its broader environment; installing those packages is optional for this CLI project.

## Sample Recommendation Output

This is the actual terminal output from `python -m src.main`, including the scores and reasons. All four profiles use the normal weights.

```text
Loaded songs: 20

=== High-Energy Pop ===
Profile: genre=pop, mood=happy, energy=0.80
1. Sunrise City - Neon Echo | Score: 3.98
   Why: genre match (+2.00); mood match (+1.00); energy similarity (+0.98)
2. Gym Hero - Max Pulse | Score: 2.87
   Why: genre match (+2.00); energy similarity (+0.87)
3. Golden Hour Salsa - Cielo Rosa | Score: 1.99
   Why: mood match (+1.00); energy similarity (+0.99)
4. Rooftop Lights - Indigo Parade | Score: 1.96
   Why: mood match (+1.00); energy similarity (+0.96)
5. Silver Steps - Funk Harbor | Score: 1.93
   Why: mood match (+1.00); energy similarity (+0.93)

=== Chill Lofi ===
Profile: genre=lofi, mood=chill, energy=0.35
1. Library Rain - Paper Lanterns | Score: 4.00
   Why: genre match (+2.00); mood match (+1.00); energy similarity (+1.00)
2. Midnight Coding - LoRoom | Score: 3.93
   Why: genre match (+2.00); mood match (+1.00); energy similarity (+0.93)
3. Focus Flow - LoRoom | Score: 2.95
   Why: genre match (+2.00); energy similarity (+0.95)
4. Late Afternoon - Juniper Fields | Score: 1.98
   Why: mood match (+1.00); energy similarity (+0.98)
5. Spacewalk Thoughts - Orbit Bloom | Score: 1.93
   Why: mood match (+1.00); energy similarity (+0.93)

=== Intense Rock ===
Profile: genre=rock, mood=intense, energy=0.92
1. Storm Runner - Voltline | Score: 3.99
   Why: genre match (+2.00); mood match (+1.00); energy similarity (+0.99)
2. Gym Hero - Max Pulse | Score: 1.99
   Why: mood match (+1.00); energy similarity (+0.99)
3. Neon Sprint - Pulse Avenue | Score: 1.96
   Why: mood match (+1.00); energy similarity (+0.96)
4. Heavy Sky - Static Harbor | Score: 1.94
   Why: mood match (+1.00); energy similarity (+0.94)
5. Sunrise City - Neon Echo | Score: 0.90
   Why: energy similarity (+0.90)

=== Conflicting Preferences ===
Profile: genre=rock, mood=sad, energy=0.15
1. Storm Runner - Voltline | Score: 2.24
   Why: genre match (+2.00); energy similarity (+0.24)
2. Blue Window - Hearth Notes | Score: 1.87
   Why: mood match (+1.00); energy similarity (+0.87)
3. Quiet Strings - Orchard Quartet | Score: 0.97
   Why: energy similarity (+0.97)
4. Spacewalk Thoughts - Orbit Bloom | Score: 0.87
   Why: energy similarity (+0.87)
5. Paper Planes - Meadow Folk | Score: 0.85
   Why: energy similarity (+0.85)
```

## Experiments I Tried

I tested the normal weights with four different profiles:

1. **High-Energy Pop** (`pop`, `happy`, `0.80`) should find upbeat pop. Sunrise City won with 3.98 points.
2. **Chill Lofi** (`lofi`, `chill`, `0.35`) should find calmer music. Library Rain won with 4.00 points, and the other two lofi tracks were also near the top.
3. **Intense Rock** (`rock`, `intense`, `0.92`) should find energetic tracks. Storm Runner won with 3.99 points, but Gym Hero (pop) also ranked highly because it matched the mood and energy.
4. **Conflicting Preferences** (`rock`, `sad`, `0.15`) is an edge case. Storm Runner still won, even though it is intense and has energy 0.91. That did not feel like the best recommendation for someone asking for sad and quiet music.

### Weight shift: does energy matter enough?

I halved the genre weight from **2.0 to 1.0** and doubled the energy weight from **1.0 to 2.0**, leaving mood at 1.0. I added a separate script so this comparison is easy to repeat without changing the default version.

Run `python -m src.evaluate` to reproduce these results:

```text

Baseline:
1. Sunrise City (3.98)
2. Gym Hero (2.87)
3. Golden Hour Salsa (1.99)
4. Rooftop Lights (1.96)
5. Silver Steps (1.93)

Energy-focused experiment:
1. Sunrise City (3.96)
2. Golden Hour Salsa (2.98)
3. Rooftop Lights (2.92)
4. Silver Steps (2.86)
5. Gym Hero (2.74)
```

**What changed?** Sunrise City stayed first because it fit all three features. But Gym Hero dropped from second to fifth, while Golden Hour Salsa, Rooftop Lights, and Silver Steps moved up. This makes sense: those songs are happy and closer to the listener's target energy, even though their genre is different. I think the experimental ranking is more varied, but it is not automatically better for everybody. The weights depend on what listeners care about most.

## Limitations and Risks

The catalog contains only 20 made-up songs, not a real streaming library. Some genres have just one track, and genre matching is exact, so `pop` and `indie pop` are treated as separate genres. Because it relies on a few hand-picked attributes, it can make a **filter bubble** by repeatedly promoting the same types of music. It also cannot learn from skips, listening history, lyrics, or a person's changing taste. A score is a basic similarity measurement, not proof that someone will like a song.

For more detail about tests, use cases, and future changes, see the [Model Card](model_card.md).

## Reflection

The biggest thing I learned was that a recommendation is not just a guess. Even a very small system needs a way to represent music as data, compare it to somebody's preferences, and rank the results. I also realized that two reasonable scoring rules can produce different song lists without either one being completely right.

AI tools helped with the scoring approach and checking the code, but the outputs were still worth testing instead of assuming the first result made sense. The conflicting rock profile was the clearest example: the math worked exactly as written, but the recommendation did not really match the mood. If I kept building this, I would add feedback from listeners and make the top five a little more diverse.
