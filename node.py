import pandas as pd
import json
import ast

df = pd.read_csv("tmdb_5000_movies.csv")
df = df.sort_values("revenue", ascending=False).head(200)
df = df[df["vote_average"] >= 7.5]

nodes = []
links = []

gset = {}
cset = {}

for _, row in df.iterrows():

    genres = ast.literal_eval(row["genres"])
    companies = ast.literal_eval(row["production_companies"])

    movie_id = f"movie_{row['id']}"

    nodes.append({
        "id": movie_id,
        "label": row["title"],
        "type": "movie",
        "budget": row["budget"],
        "revenue": row["revenue"],
        "vote_average": row["vote_average"],
        "primary_genre": f"genre_{genres[0]['id']}" if genres else None
    })

    for g in genres:
        gid = f"genre_{g['id']}"
        if gid not in gset:
            gset[gid] = True
            nodes.append({
                "id": gid,
                "label": g["name"],
                "type": "genre"
            })
        links.append({"source": movie_id, "target": gid})

    for c in companies[:2]:
        cid = f"company_{c['id']}"
        if cid not in cset:
            cset[cid] = True
            nodes.append({
                "id": cid,
                "label": c["name"],
                "type": "company"
            })
        links.append({"source": movie_id, "target": cid})

networks = {"nodes": nodes, "links": links}

with open("network.json", "w") as f:
    json.dump(networks, f, indent=2)


network = "network.json"
network