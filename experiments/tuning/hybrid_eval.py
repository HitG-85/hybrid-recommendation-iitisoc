from knn_eval import recommend_knn
from graph_eval import recommend_graph
from mf_eval import recommend_mf
import pandas as pd

items_df = pd.read_csv("../../dataset/items.csv")

item_categories = dict(
    zip(items_df["id"], items_df["category"])
)

weights = {
    "knn": 0.35,
    "graph": 0.20,
    "mf": 0.45
}

def recommend_hybrid(user_id, weights, top_n=10):

    knn_recs = recommend_knn(user_id, top_n=top_n)
    graph_recs = recommend_graph(user_id, top_n=top_n)
    mf_recs = recommend_mf(user_id, top_n=top_n)

    final_scores = {}

    # KNN contribution
    for item_id, score in knn_recs:

        final_scores[item_id] = (
            final_scores.get(item_id, 0)
            + weights["knn"] * score
        )

    # Graph contribution
    for item_id, score in graph_recs:

        final_scores[item_id] = (
            final_scores.get(item_id, 0)
            + weights["graph"] * score
        )

    # MF contribution
    for item_id, score in mf_recs.items():

        final_scores[item_id] = (
            final_scores.get(item_id, 0)
            + weights["mf"] * score
        )

    recommendations = sorted(
        final_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]


if __name__ == "__main__":

    weights = {
        "knn": 0.35,
        "graph": 0.20,
        "mf": 0.45
    }

    recommendations = recommend_hybrid(15, weights)

    for item_id, score in recommendations:

        category = item_categories.get(
            item_id,
            "Unknown"
        )

        print(
            f"Item {item_id} | "
            f"Category: {category} | "
            f"Hybrid Score: {score:.3f}"
        )
        