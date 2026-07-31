from tuning.metrics import evaluate

from hybrid_recommender import recommend_hybrid as ranker_hybrid
from hybrid_manual import recommend_hybrid as manual_hybrid

print("Evaluating Manual Hybrid...")
manual_score = evaluate(manual_hybrid)

print("Evaluating Ranker Hybrid...")
ranker_score = evaluate(ranker_hybrid)

print()
print(f"Manual Hybrid Precision@10 : {manual_score:.4f}")
print(f"Ranker Hybrid Precision@10 : {ranker_score:.4f}")