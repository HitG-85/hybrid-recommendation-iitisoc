import pandas as pd
import psycopg2

df = pd.read_csv("train_interactions.csv")


df["final_score"] = (
    0.5 * df["interaction_strength"]
    + 0.3 * df["watch_percentage"]
    + 0.2 * (df["rewatch_count"] / 5)
).round(2)

matrix=df.pivot_table(
    index="user_id",
    columns="item_id",
    values="final_score",
    aggfunc="max",
    fill_value=0
)

if __name__ == "__main__":
    print(matrix)

