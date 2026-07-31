import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle

df = pd.read_csv("../dataset/training_data.csv")

print(f"Training data shape: {df.shape}")
print(df.head())

FEATURES = ["knn_score", "graph_score", "mf_score"]
LABEL    = "label"

X = df[FEATURES]
y = df[LABEL]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTrain size: {len(X_train)} | Test size: {len(X_test)}")

model = lgb.LGBMRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    num_leaves=15,
    random_state=42,
    verbose=-1
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"\nTest MAE: {mae:.4f}")

importances = pd.Series(
    model.feature_importances_,
    index=FEATURES
).sort_values(ascending=False)

print("\nFeature Importances:")
print(importances)

with open("../dataset/ranker_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nRanker saved to ../dataset/ranker_model.pkl")

# print(df[["knn_score", "graph_score", "mf_score"]].describe())
# print((df["mf_score"] == 0).mean())
# print((df["knn_score"] == 0).mean())
# print((df["graph_score"] == 0).mean())