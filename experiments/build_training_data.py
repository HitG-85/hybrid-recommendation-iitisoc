import pandas as pd
import psycopg2
from knn import score_knn
from graph_recommender import score_graph
from matrix_factorization import score_mf
from user_item_matrix import matrix

conn = psycopg2.connect(
    dbname="hybrid_recommendation_db",
    user="shivikasingh"
)

df = pd.read_sql("SELECT * FROM interactions", conn)

df["final_score"] = (
    0.5 * df["interaction_strength"]
    + 0.3 * df["watch_percentage"]
    + 0.2 * (df["rewatch_count"].clip(upper=5) / 5)
).round(4)

df_agg = (
    df.groupby(["user_id", "item_id"])["final_score"]
    .max()
    .reset_index()
)

print(f"Total (user, item) pairs: {len(df_agg)}")

# Get unique users — compute scores once per user, not once per pair
unique_users = df_agg["user_id"].unique()
print(f"Unique users to process: {len(unique_users)}")


knn_cache   = {}
graph_cache = {}
mf_cache    = {}

for i, user_id in enumerate(unique_users):
    if i % 50 == 0:
        print(f"Precomputing scores for user {i}/{len(unique_users)}...")

    knn_cache[user_id]   = score_knn(user_id)        # dict {item_id: score}
    graph_cache[user_id] = score_graph(user_id)      # dict {item_id: score}
    mf_series            = score_mf(user_id)
    mf_cache[user_id]    = mf_series.to_dict()       # convert Series to dict

print("Precomputation done. Building training rows...")


rows = []
for _, row in df_agg.iterrows():
    user_id  = row["user_id"]
    item_id  = row["item_id"]
    label    = row["final_score"]

    rows.append({
        "user_id":     user_id,
        "item_id":     item_id,
        "knn_score":   knn_cache[user_id].get(item_id, 0.0),
        "graph_score": graph_cache[user_id].get(item_id, 0.0),
        "mf_score":    mf_cache[user_id].get(item_id, 0.0),
        "label":       label
    })

training_df = pd.DataFrame(rows)
training_df.to_csv("../dataset/training_data.csv", index=False)

print(f"\nDone. Training data saved: {len(training_df)} rows")
print(training_df.describe())