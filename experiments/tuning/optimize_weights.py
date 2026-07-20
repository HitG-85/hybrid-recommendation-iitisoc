from metrics import evaluate
import time

best_precision = -1
count=0
best_weights = None
##avg_precision is one from the metrics file, the average precision@10 to compare each of it with diff weights
for knn in range(11):
    for graph in range(11):
        for mf in range(11):

            if knn + graph + mf == 10:

                weights = {
                    "knn": knn / 10,
                    "graph": graph / 10,
                    "mf": mf / 10
                }
                count+=1
                print(f"\n[{count}/66] Testing {weights}")

                start = time.time()

                avg_precision = evaluate(weights)
                

                print(f"Took {time.time() - start:.1f} seconds")
                print(f"Precision: {avg_precision:.4f}")

                if avg_precision > best_precision:
                    best_precision = avg_precision
                    best_weights = weights

                    print(f"New Best: {best_precision:.4f}")
                    print(f"Weights: {best_weights}")


if __name__=="__main__":
    print(f"Best Weights: {best_weights}")
    print(f"Best Average Precision@10:{best_precision}")