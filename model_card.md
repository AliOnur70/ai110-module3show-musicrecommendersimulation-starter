# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a simple, content-based music recommender.

## 2. Intended Use and Non-Intended Use

This is a classroom simulation for someone learning how recommendations work. It suggests five songs from a small catalog using a listener's favorite genre, mood, and preferred energy. The optional class-based profile also asks whether the listener likes acoustic music. The program assumes those preferences describe what the person wants to hear right now.

This is **not** intended to predict real people's taste, replace a streaming service, make judgments about listeners, or support decisions outside music discovery. It does not collect personal information or track listening history.

## 3. How the Model Works / Algorithm Summary

The model reads the songs from a CSV file. Each song gets **2 points** if the genre matches the listener's favorite genre and **1 point** if the mood matches. Then it adds up to **1 more point** when the song's energy is close to the listener's target. A very close energy match earns more than a distant one. Class-based profiles can also earn up to **0.5 points** for acousticness. The program sorts all the songs by total score and shows the top five with explanations.

The basic CLI profiles use just genre, mood, and energy, so their maximum score is 4.00. The scoring is hand-written math, not a trained AI model. The starter project had empty scoring and ranking functions; I filled those in and connected the class-based and dictionary-based versions to the same rule.

## 4. Data Used

The catalog has **20 fictional songs**: the original 10 starter tracks plus 10 new examples. It covers 17 distinct genre labels, such as pop, lofi, rock, jazz, EDM, latin, folk, blues, classical, hip-hop, metal, and acoustic. Every track includes its title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

Only a few of these features affect the score right now. The numbers are examples for a simulation, not official measurements, and no real likes, skips, playlists, or listener behavior are included. A few genres have multiple songs, while many have just one.

## 5. Strengths / Observed Behavior

The recommender is fast, simple to understand, and easy to test. It makes sense for a listener with clear preferences. **Sunrise City** ranked first for high-energy happy pop (3.98), **Library Rain** ranked first for chill lofi (4.00), and **Storm Runner** ranked first for intense rock (3.99). Those results feel reasonable because they match the requested genres, moods, and energy levels.

The explanations also help. Instead of only showing a number, the program tells the listener which matches added points.

## 6. Limitations and Bias

The biggest issue is that genre can count too much. The test listener who wanted **sad, low-energy rock** still received **Storm Runner** first. It got 2 points for rock even though its mood is intense and its energy is 0.91, far from the requested 0.15. That is a clear example of the math being correct while the suggestion still feels wrong. The system also treats `pop` and `indie pop` as different genres, even though they overlap. Since most genres have only one song, a listener may keep seeing the same songs and miss good choices from other genres. This could create a small **filter bubble**.

Another limitation is that the model cannot tell whether someone actually likes a recommendation. It does not learn from skips or repeat listens, and it ignores lyrics, language, and artists when scoring. These limitations affect who gets useful recommendations and how varied those suggestions are.

## 7. Evaluation Process

I ran `python -m src.main` with four different taste profiles and read the top five for each:

- **High-Energy Pop** (`pop`, `happy`, `0.80`): Sunrise City (3.98) was first. Gym Hero (2.87) came second because genre was weighted heavily.
- **Chill Lofi** (`lofi`, `chill`, `0.35`): Library Rain (4.00) and Midnight Coding (3.93) came first, followed by another lofi track.
- **Intense Rock** (`rock`, `intense`, `0.92`): Storm Runner (3.99) was first. Gym Hero (1.99) and Neon Sprint (1.96) also appeared because their mood and energy were similar.
- **Conflicting Preferences** (`rock`, `sad`, `0.15`): Storm Runner (2.24) still came first, ahead of the sad blues song Blue Window (1.87). This was the most surprising result.

### Comparing the profiles

- **Pop vs. Lofi:** Pop favored upbeat songs, while lofi favored calmer tracks like Library Rain and Midnight Coding.
- **Pop vs. Rock:** Both featured Gym Hero, but rock put Storm Runner first because it matched rock and intense.
- **Pop vs. Conflicting:** Pop put happy Sunrise City first, while the conflicting profile still preferred Storm Runner because of the genre bonus.
- **Lofi vs. Rock:** Lofi's top picks were low-energy, while rock's top picks were much more intense.
- **Lofi vs. Conflicting:** Both requested low energy, but the conflicting profile's top song was much louder because its genre preference overpowered energy.
- **Rock vs. Conflicting:** They share the same favorite genre, so Storm Runner won both tests even though the second listener wanted sad, quiet music.

### Small scoring experiment

I tested one change: **genre 2.0 → 1.0** and **energy 1.0 → 2.0**, with mood unchanged. The `python -m src.evaluate` script prints both rankings for the pop/happy profile.

| Rank | Original scoring | Energy-focused scoring |
| --- | --- | --- |
| 1 | Sunrise City (3.98) | Sunrise City (3.96) |
| 2 | Gym Hero (2.87) | Golden Hour Salsa (2.98) |
| 3 | Golden Hour Salsa (1.99) | Rooftop Lights (2.92) |
| 4 | Rooftop Lights (1.96) | Silver Steps (2.86) |
| 5 | Silver Steps (1.93) | Gym Hero (2.74) |

**Result:** the energy-focused version brought more happy, similar-energy songs closer to the top. It might better fit this particular listener, but it also weakened the importance of their favorite genre. I would want feedback from actual listeners before choosing one set of weights permanently.

I also ran automated tests with `python -m pytest -q`. They check CSV number conversion, scoring explanations, sorting, the value of `k`, acoustic preference, and the experiment. The original two class-based starter tests passed as well.

## 8. Future Work / Ideas for Improvement

1. **Learn from feedback:** let someone like, skip, or save songs so preferences can change over time.
2. **Support more flexible genre matches:** recognize related genres, and give some bonus for artist, tempo, or danceability when they matter.
3. **Add diversity:** reserve at least one top-five spot for a nearby but different genre, instead of recommending only familiar kinds of songs.

## 9. Personal Reflection

The biggest thing I learned is how much the weights affect recommendations. I expected matching genre to be helpful, but I did not expect an intense rock track to show up first for someone who requested sad and quiet music. It showed me that even when a program works correctly, the result can still be a poor recommendation.

AI tools were useful for brainstorming the scoring rule, building the first version, and thinking of a tricky profile to test. The important part was checking the actual scores, comparing rankings, and making sure the output matched the rules. If I extended this project, I would let listeners give feedback and see whether their recommendations improved over time. It made real-world apps feel less mysterious, while also showing why their recommendation systems need more than just a few features.
