# I: movie_ratings.csv — movie_title, genre, release_year, reviewer_id,
#    rating: 1-5, times_watched, would_recommend, platform
# P: load CSV, clean data, validate, analyze with groupby, visualize
# O: groupby summaries, avg_rating_by_genre

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_data():
    df = pd.read_csv("/Users/kylechristensen/Documents/IS303-A06/movie_ratings.csv")
    return df


def clean_data(df):
    # drop rows with missing rating
    df = df.dropna(subset=["rating_1_5"])
    # normalize genre casing (e.g. 'action' -> 'Action', 'SCI-FI' -> 'Sci-Fi')
    df["genre"] = df["genre"].str.title()
    # convert release_year to numeric, drop bad rows (e.g. 'two thousand twelve')
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df = df.dropna(subset=["release_year"])
    return df


def analyze_data(df):
    print("Average rating by genre:")
    print(df.groupby("genre")["rating_1_5"].mean().round(2))
    print()
    print("Most-reviewed movie:")
    print(df.groupby("movie_title")["reviewer_id"].count().idxmax())
    print()
    print("Recommendation rate by movie (%):")
    rec_rate = df.groupby("movie_title")["would_recommend"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).round(1)
    print(rec_rate)


def visualize_data(df):
    avg_rating = df.groupby("genre")["rating_1_5"].mean().round(2)
    avg_rating.plot(kind="bar", color="steelblue", edgecolor="white")
    plt.title("Average Rating by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Average Rating (1–5)")
    plt.tight_layout()
    plt.savefig("avg_rating_by_genre.png")
    plt.close()


df = load_data()
df = clean_data(df)

assert df["rating_1_5"].isna().sum() == 0, "Missing ratings remain"
assert (df["rating_1_5"].between(1, 5)).all(), "Rating out of 1–5 range"

analyze_data(df)
visualize_data(df)