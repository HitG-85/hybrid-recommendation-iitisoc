import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from user_item_matrix import matrix

sim = cosine_similarity(matrix)

similarity_df = pd.DataFrame(
    sim,
    index=matrix.index,
    columns=matrix.index
)

##print(similarity_df.head())