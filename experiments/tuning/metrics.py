import pandas as pd 
from hybrid_eval import recommend_hybrid, weights

def precision_at_k(recommended_items, actual_items, k):

    hits = 0

    for item in recommended_items:

        if item in actual_items:

            hits += 1

    return hits / k



def evaluate(weights, k=10):

    test_df = pd.read_csv("test_interactions.csv")
    precisions=[]

    for user_id in test_df["user_id"].unique():
        #Actual items are the recommended items hidden in test dataset
        actual_items = set(
            test_df[test_df["user_id"] == user_id]["item_id"]
        )

        ##print(user_id, actual_items)
        

        recommendations=recommend_hybrid(user_id,weights,top_n=k)
        recommended_items=[
              item_id
              for item_id,score in recommendations
            ]
        precision = precision_at_k(
         recommended_items,
         actual_items,
          k
        )
        
        
        
        
        
        
        precisions.append(precision)

    return sum(precisions)/len(precisions)
   

if __name__ == "__main__":
    avg=evaluate(weights)
    print(f"Average Precision@10 for a user {avg:.4f} \n")    





