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

def score_mf(user_id):
    if user_id not in matrix.index:
        return pd.Series(dtype=float)

    user_index = matrix.index.get_loc(user_id)
    
    
    # gives a real latent score for every item, no truncation
    all_scores = model.item_factors @ model.user_factors[user_index]
    
    result = pd.Series(
        data=all_scores,
        index=matrix.columns
    )
    
    return normalize_scores(result)


def recommend_mf(user_id, top_n=10):
    """Recommendation function - filters seen items at the END"""
    all_scores = score_mf(user_id)

    if all_scores.empty:
        return pd.Series(dtype=float)

    # filter seen items HERE
    seen_items = set(matrix.loc[user_id][matrix.loc[user_id] > 0].index)
    unseen_scores = all_scores[~all_scores.index.isin(seen_items)]

    return unseen_scores.head(top_n)

if __name__ == "__main__":

    user_id = 15

    print(
        f"MF Recommendations for User {user_id}\n"
    )

    print(
        recommend_mf(user_id)
    )