import pandas as pd
import pickle
from knn import recommend_knn, score_knn
from graph_recommender import recommend_graph, score_graph
from matrix_factorization import recommend_mf, score_mf

items_df = pd.read_csv("../dataset/items.csv")
item_categories = dict(zip(items_df["id"], items_df["category"]))


with open("../dataset/ranker_model.pkl", "rb") as f:
    ranker = pickle.load(f)


def recommend_hybrid(user_id, top_n=10, candidate_pool_size=100):

    
    knn_recs   = recommend_knn(user_id, top_n=candidate_pool_size)
    graph_recs = recommend_graph(user_id, top_n=candidate_pool_size)
    mf_recs    = recommend_mf(user_id, top_n=candidate_pool_size)

    
    candidate_ids = list(dict.fromkeys(
        [item_id for item_id, _ in knn_recs] +
        [item_id for item_id, _ in graph_recs] +
        list(mf_recs.index)
    ))

    if not candidate_ids:
        return []

    
    knn_scores   = score_knn(user_id)
    graph_scores = score_graph(user_id)
    mf_scores    = score_mf(user_id)

    
    feature_rows = []
    for item_id in candidate_ids:
        feature_rows.append({
            "item_id":     item_id,
            "knn_score":   knn_scores.get(item_id, 0.0),
            "graph_score": graph_scores.get(item_id, 0.0),
            "mf_score":    float(mf_scores.get(item_id, 0.0))
        })

    features_df = pd.DataFrame(feature_rows)

    
    features_df["final_score"] = ranker.predict(
        features_df[["knn_score", "graph_score", "mf_score"]]
    )

    
    recommendations = (
        features_df
        .sort_values("final_score", ascending=False)
        .head(top_n)
    )

    return list(zip(recommendations["item_id"], recommendations["final_score"]))


if __name__ == "__main__":

    recommendations = recommend_hybrid(15)

    for item_id, score in recommendations:
        category = item_categories.get(item_id, "Unknown")
        print(
            f"Item {item_id} | "
            f"Category: {category} | "
            f"Hybrid Score: {score:.3f}"
        )