import pandas as pd

print("loading basics and ratin of movies..")

basics = pd.read_csv("title.basics.tsv.gz",
                     sep="\t",
                     na_values="\\N",
                     low_memory=False)

basics = basics[basics["titleType"] == "movie"]

ratings = pd.read_csv("title.ratings.tsv.gz",
                      sep="\t",
                      na_values="\\N")

df_all = basics.merge(ratings, on="tconst", how="left")
df_all = df_all[["tconst", "primaryTitle", "startYear", "genres", "averageRating", "numVotes"]]

df_all = df_all.dropna()
df_all = df_all[df_all["numVotes"] > 2000]
df_all = df_all.reset_index(drop=True)

df_all.to_csv("imdb_movies.csv", index=False)
print(f"Saved imdb_movies.csv with {len(df_all)} movies")





print("filtering hindi movies..")

chunksize = 500000
filteredChunks = []

for chunk in pd.read_csv("title.akas.tsv.gz",
                         sep="\t",
                         na_values="\\N",
                         low_memory=False,
                         chunksize=chunksize):
    
    sub = chunk[(chunk["language"] == "hi") | (chunk["region"] == "IN")]
    if not sub.empty:
        filteredChunks.append(sub)

hindi_movies = pd.concat(filteredChunks, ignore_index=True)
print("filtered hindi/indian rows:", len(hindi_movies))

df_hindi = basics.merge(hindi_movies, left_on="tconst", right_on="titleId", how="inner")
df_hindi = df_hindi.merge(ratings, on="tconst", how="left")

df_hindi = df_hindi[["tconst", "primaryTitle", "title", "startYear", "genres", "averageRating", "numVotes"]]
df_hindi = df_hindi.dropna()
df_hindi = df_hindi.reset_index(drop=True)

df_hindi.to_csv("hindi_movies.csv", index=False)
print(f"Saved hindi_movies.csv with {len(df_hindi)} movies")
