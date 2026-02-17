import kagglehub
import pandas as pd
import numpy as np
import shutil
import os

# %% #Importing Data
#importing data from kaggle and correcting the file path
os.chdir(r"C:\Users\czsal\PycharmProjects\DataWarehousing")
path = kagglehub.dataset_download("maharshipandya/-spotify-tracks-dataset")
for file in os.listdir(path):
    shutil.copy2(os.path.join(path, file), os.getcwd())

# %% Part 1: Data Cleaning with Python and Pandas
import pandas as pd
df = pd.read_csv("dataset.csv")

critical_cols = [
    "track_id",
    "track_name",
    "artists",
    "album_name",
    "track_genre",
    "popularity",
    "danceability",
    "energy",
    "acousticness",
    "valence",
    "tempo"
]
df = df.dropna(subset=critical_cols)
print(df.shape)
print(df.head)

# %% # Part 2: Generating CSV Files for Neo4j (20%)
path = r"C:\Users\czsal\PycharmProjects\DataWarehousing"
#2.1: tracks.csv
df_tracks = df[[
    "track_id",
    "track_name",
    "popularity",
    "danceability",
    "valence",
    "acousticness",
    "album_name",
    "track_genre",
    "artists"
]].drop_duplicates(subset=["track_id"])
df_tracks.to_csv(f"{path}\\tracks.csv", index=False)
print(df_tracks.shape)
print(df_tracks.head)
# %%
#2.2: artists.csv
df_tracks["artist_list"] = df_tracks["artists"].astype(str).str.split(";")

unique_artists = set(
    artist.strip()
    for sublist in df_tracks["artist_list"]
    for artist in sublist
)

df_artists = pd.DataFrame(unique_artists, columns=["name"])
df_artists.to_csv(f"{path}\\artists.csv", index=False)
print(df_artists.shape)
print(df_artists.head)

#2.3: albums.csv
df_albums = df_tracks[["album_name"]].drop_duplicates()
df_albums.rename(columns={"album_name": "name"}, inplace=True)
df_albums.to_csv(f"{path}\\albums.csv", index=False)
print(df_albums.shape)
print(df_albums.head)

#2.4: genres.csv
df_genres = df_tracks[["track_genre"]].drop_duplicates()
df_genres.rename(columns={"track_genre": "name"}, inplace=True)
df_genres.to_csv(f"{path}\\genres.csv", index=False)
print(df_genres.shape)
print(df_genres.head)

#2.5a: rel_performed_by.csv – (Track)-[:PERFORMED_BY]->(Artist)
rows = []
for _, row in df_tracks.iterrows():
    track_id = row["track_id"]
    for artist in row["artist_list"]:
        rows.append({
            "track_id": track_id,
            "artist_name": artist.strip()
        })

df_performed_by = pd.DataFrame(rows)
df_performed_by.to_csv(f"{path}\\rel_performed_by.csv", index=False)
print(df_performed_by.shape)
print(df_performed_by.head)

#2.5b: rel_belongs_to.csv – (Track)-[:BELONGS_TO]->(Album)
df_belongs_to = df_tracks[["track_id", "album_name"]].drop_duplicates()
df_belongs_to.to_csv(f"{path}\\rel_belongs_to.csv", index=False)
print(df_belongs_to.shape)
print(df_belongs_to.head)

#2.5c: rel_has_genre.csv – (Track)-[:HAS_GENRE]->(Genre)
df_has_genre = df_tracks[["track_id", "track_genre"]].drop_duplicates()
df_has_genre.to_csv(f"{path}\\rel_has_genre.csv", index=False)
print(df_has_genre.shape)
print(df_has_genre.head)