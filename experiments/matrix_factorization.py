from implicit.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix
import pandas as pd
from user_item_matrix import matrix

sparse_matrix = csr_matrix(matrix.values)         #convert df to matrix

model = AlternatingLeastSquares(
    factors=20,
    regularization=0.1,
    iterations=20,
    random_state=42
)

model.fit(sparse_matrix)

def normalize_scores(scores):

    min_score = scores.min()
    max_score = scores.max()

    if max_score == min_score:
        return scores

    return (
        (scores - min_score)
        / (max_score - min_score)
    )

def recommend_mf(user_id, top_n=10):
    if user_id not in matrix.index:
        return pd.Series(dtype=float)
    
    
    user_index = matrix.index.get_loc(user_id)
    item_ids, scores = model.recommend(
     userid=user_index,
     user_items=sparse_matrix[user_index],
     N=top_n,
     filter_already_liked_items=True
)
    recommendations = pd.Series(
     data=scores,
     index=matrix.columns[item_ids]
)
    recommendations = normalize_scores(
        recommendations
    )

    return recommendations

if __name__ == "__main__":

    user_id = 15

    print(
        f"MF Recommendations for User {user_id}\n"
    )

    print(
        recommend_mf(user_id)
    )