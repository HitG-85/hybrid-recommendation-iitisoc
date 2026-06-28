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

def get_graph_score(user_id):
    seen_items=get_seen_items(user_id)

    if not seen_items:
        return {}
    
    graph_scores={}

    #hook_item is the item with control in for loop.
    for hook_item in seen_items: 
        user_for_hook_item=matrix.index[matrix[hook_item]>0]

        for neighbour_user in user_for_hook_item:
            if neighbour_user==user_id:
                continue

            neighbour_row=matrix.loc[neighbour_user]
            neighbour_items=neighbour_row[neighbour_row>0]

            for candidate_item, candidate_strength in neighbour_items.items():
                if candidate_item in seen_items:
                    continue

                graph_scores[candidate_item]= (graph_scores.get(candidate_item,0)+float(candidate_strength))

    return graph_scores 
            
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
    raw_graph_scores = get_graph_score(user_id)

    if not raw_graph_scores:
        return fallback_recommendations(user_id, top_n)

    new_graph_scores = normalize_scores(raw_graph_scores)

    recommendations = sorted(
        new_graph_scores.items(),
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

    
# user_id = 12

# print(f"Seen items for User {user_id}:\n")

# for item_id in sorted(get_seen_items(user_id)):
#     score = matrix.loc[user_id, item_id]
#     category = item_categories[item_id]

#     print(
#         f"Item {item_id} | "
#         f"Category: {category} | "
#         f"Interaction: {score:.3f}"
#     )
    
            

    
            
            


                 



        

    
