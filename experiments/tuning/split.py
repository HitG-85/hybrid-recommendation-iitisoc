import pandas as pd

# Load interactions
df = pd.read_csv("../../dataset/interactions.csv")

train_parts = []
test_parts = []

# Process each user separately
for user_id, user_df in df.groupby("user_id"):

    # Shuffle this user's interactions
    user_df = user_df.sample(
        frac=1,
        random_state=42
    )

    split_index = int(0.8 * len(user_df))

    train_parts.append(
        user_df.iloc[:split_index]
    )

    test_parts.append(
        user_df.iloc[split_index:]
    )

# Combine all users back together
train_df = pd.concat(
    train_parts,
    ignore_index=True
)

test_df = pd.concat(
    test_parts,
    ignore_index=True
)

# Save
train_df.to_csv(
    "train_interactions.csv",
    index=False
)

test_df.to_csv(
    "test_interactions.csv",
    index=False
)

print("Train interactions:", len(train_df))
print("Test interactions:", len(test_df))

##Testing if each user's interactions were split into 80/20
# for user in train_df["user_id"].unique():       

#     train_count = len(train_df[train_df["user_id"] == user])
#     test_count = len(test_df[test_df["user_id"] == user])

#     total = train_count + test_count

#     print(
#         user,
#         f"{train_count/total:.2%}",
#         f"{test_count/total:.2%}"
#     )