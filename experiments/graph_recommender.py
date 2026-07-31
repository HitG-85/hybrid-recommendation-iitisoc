from user_item_matrix import matrix
from cosine_sim import similarity_df
import pandas as pd

items_df = pd.read_csv("../dataset/items.csv")

item_categories = dict(
    zip(items_df["id"], items_df["category"])
)


def fallback_recommendations(user_id, top_n=10):
    #items the user has already seen
    seen_items = set(matrix.loc[user_id][matrix.loc[user_id] > 0].index)

    #most seen from interactions matrix
    item_popularity = matrix.sum(axis=0).sort_values(ascending=False)

    #remove seen items
    item_popularity = item_popularity[~item_popularity.index.isin(seen_items)]

    #return top unseen items
    return list(item_popularity.head(top_n).items())

#user_id is the user who sends query
def get_seen_items(user_id):
    if user_id not in matrix.index:
        return set()
    
    row=matrix.loc[user_id]
    seen=row[row>0].index
    return set(seen)

def score_graph(user_id):
    """Scores ALL items including seen ones - for ranker training"""
    seen_items = get_seen_items(user_id)
    if not seen_items:
        return {}

    graph_scores = {}

    for hook_item in seen_items:
        users_for_hook_item = matrix.index[matrix[hook_item] > 0]

        for neighbour_user in users_for_hook_item:
            if neighbour_user == user_id:
                continue

            neighbour_row = matrix.loc[neighbour_user]
            neighbour_items = neighbour_row[neighbour_row > 0]

            for candidate_item, candidate_strength in neighbour_items.items():
                # NO seen filter here
                graph_scores[candidate_item] = (
                    graph_scores.get(candidate_item, 0) + float(candidate_strength)
                )

    return normalize_scores(graph_scores)


def recommend_graph(user_id, top_n=10):
    """Recommendation function - filters seen items at the END"""
    all_scores = score_graph(user_id)

    if not all_scores:
        return fallback_recommendations(user_id, top_n)

    # filter seen items HERE
    seen_items = get_seen_items(user_id)
    unseen_scores = {k: v for k, v in all_scores.items() if k not in seen_items}

    if not unseen_scores:
        return fallback_recommendations(user_id, top_n)

    return sorted(unseen_scores.items(), key=lambda x: x[1], reverse=True)[:top_n] 
            
def normalize_scores(score_dict):             #here score_dict is graph_scores
    if not score_dict:
        return score_dict

    max_score = max(score_dict.values())
    if max_score == 0:
        return score_dict
        
    normalised_dict={}
    for item_id,score in score_dict.items():
        normalised_dict[item_id]=score/max_score
    return normalised_dict

def recommend_graph(user_id, top_n=10):
    all_scores = score_graph(user_id)

    if not all_scores:
        return fallback_recommendations(user_id, top_n)

    seen_items = get_seen_items(user_id)
    unseen_scores = {k: v for k, v in all_scores.items() if k not in seen_items}

    if not unseen_scores:
        return fallback_recommendations(user_id, top_n)

    recommendations = sorted(
        unseen_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]


if __name__ == "__main__":

    recommendations = recommend_graph(15, top_n=10)


    for item_id, score in recommendations:
        category = item_categories.get(item_id, "Unknown")

        print(
            f"Item {item_id} | "
            f"Category: {category} | "
            f"Score: {score:.3f}"
        )

    
# check user 15's interaction history categories
seen = get_seen_items(15)
for item_id in seen:
    print(item_id, item_categories[item_id])


    
            
            


                 



        

    
