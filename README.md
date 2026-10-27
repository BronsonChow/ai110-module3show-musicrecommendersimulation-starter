# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube combine two main approaches. **Collaborative filtering** recommends what similar listeners liked ("people who played X also played Y"). **Content-based filtering** recommends songs whose attributes match what you already enjoy. Those systems learn from huge amounts of behavior data, such as plays, skips, saves and replays, and they balance relevance with freshness and variety. My version is a small content-based recommender: it has no other users' data, so it compares each song's attributes to a single user's taste profile. It prioritizes **genre** as the strongest signal, then **mood**, then how close a song's **energy** is to the user's target level. It rewards closeness to the target rather than simply higher or lower values. Each matching feature adds points to a song's score, the highest-scoring songs are returned, and every recommendation comes with a plain-language reason so the ranking is easy to explain.

**`Song` features**

- `genre`: the musical style, such as pop, lofi or rock. This is the main feature for matching.
- `mood`: the feel of the track, such as happy, chill or intense. This is a secondary match.
- `energy` (0–1): how calm or intense the song is. It's compared to the user's target energy.
- `acousticness` (0–1): how acoustic the song sounds versus electronic or produced. It's used for the acoustic preference.
- `title`, `artist`, `id`: used to identify and display the song, not for scoring.
- `tempo_bpm`, `valence`, `danceability`: loaded from the CSV but not scored, because they mostly overlap with energy and mood.

**`UserProfile` features**

- `favorite_genre`: the genre the user wants most. A match earns the most points.
- `favorite_mood`: the vibe the user wants right now. A match earns extra points.
- `target_energy` (0–1): the user's ideal energy level. Songs score higher the closer they are to it.
- `likes_acoustic` (True/False): whether to reward songs with high acousticness.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python src/main.py
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



