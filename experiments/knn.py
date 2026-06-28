from user_item_matrix import matrix
from cosine_sim import similarity_df
import pandas as pd

items_df = pd.read_csv("../dataset/items.csv")
item_categories = dict(zip(items_df["id"], items_df["category"]))

def get_similar_users(user_id):
    similar_users=(
        similarity_df
        .loc[user_id]
        .drop(user_id)
        .sort_values(ascending=False)
    )
    return similar_users

##print(get_similar_users(1))
def fallback_recommendations(user_id, top_n=10):
    #items the user has already seen
    seen_items = set(matrix.loc[user_id][matrix.loc[user_id] > 0].index)

    #most seen from interactions matrix
    item_popularity = matrix.sum(axis=0).sort_values(ascending=False)

    #remove seen items
    item_popularity = item_popularity[~item_popularity.index.isin(seen_items)]

    #return top unseen items
    return list(item_popularity.head(top_n).items())

##print(top_k)
def recommend_knn(user_id, k=3, top_n=10):

    top_k = get_similar_users(user_id).head(k)
    if top_k.empty:
        print(f"User {user_id} has no new unseen items from similar users. Using fallback recommendations.")
        return fallback_recommendations(user_id,top_n)

    seen_items = matrix.loc[user_id]
    seen_items = seen_items[seen_items > 0]

    candidate_weighted_scores = {}
    candidate_similarity_sums = {}

    for similar_user, similarity in top_k.items():

        user_items = matrix.loc[similar_user]

        unseen_items = user_items[
            (user_items > 0)
            & (~user_items.index.isin(seen_items.index))
        ]

        for item_id, item_score in unseen_items.items():

            weighted_score = similarity * item_score

            candidate_weighted_scores[item_id] = (
                candidate_weighted_scores.get(item_id, 0)
                + weighted_score
            )

            candidate_similarity_sums[item_id] = (
                candidate_similarity_sums.get(item_id, 0)
                + similarity
            )

    candidate_scores = {}

    for item_id in candidate_weighted_scores:

        candidate_scores[item_id] = (
            candidate_weighted_scores[item_id]
            / candidate_similarity_sums[item_id]
        )
    
    if not candidate_scores:
        print(f"User {user_id} has no new unseen items from similar users. Using fallback recommendations.")
        return fallback_recommendations(user_id,top_n)
    
    recommendations = sorted(
        candidate_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]

if __name__ == "__main__":

    recommendations = recommend_knn(15)

    print("item_id\tcategory\tscore")

    for item_id, score in recommendations:

        category = item_categories.get(
            item_id,
            "Unknown"
        )

        print(
            f"{item_id}\t"
            f"{category}\t"
            f"{score:.3f}"
        )