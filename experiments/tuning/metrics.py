import pandas as pd 


def precision_at_k(recommended_items, actual_items, k):

    hits = 0

    for item in recommended_items:

        if item in actual_items:

            hits += 1

    return hits / k



def evaluate(recommend_fn, k=10):

    test_df = pd.read_csv("tuning/test_interactions.csv")
    precisions = []

    for user_id in test_df["user_id"].unique():

        # Actual hidden items
        actual_items = set(
            test_df[test_df["user_id"] == user_id]["item_id"]
        )

        # Recommendations
        recommendations = recommend_fn(user_id, top_n=k)

        recommended_items = [
            item_id
            for item_id, score in recommendations
        ]

        # ---------- DEBUG (only first user) ----------
        if len(precisions) == 0:
            print(f"\nUser: {user_id}")
            print("Actual items:")
            print(sorted(actual_items))

            print("\nRecommended items:")
            print(recommended_items)

            overlap = actual_items.intersection(set(recommended_items))

            print("\nOverlap:")
            print(overlap)
            print(f"Hits: {len(overlap)}")
            print("-" * 60)
        # ---------------------------------------------

        precision = precision_at_k(
            recommended_items,
            actual_items,
            k
        )

        precisions.append(precision)

    return sum(precisions) / len(precisions)






