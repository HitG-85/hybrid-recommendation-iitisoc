import psycopg2

from hybrid_recommender import recommend_hybrid
from user_item_matrix import matrix


conn = psycopg2.connect(
    dbname="hybrid_recommendation_db",
    user="postgres",
    password="1234qwerA@"
)

cursor = conn.cursor()

cursor.execute(
    "DELETE FROM recommendations"
)

conn.commit()


for user_id in matrix.index:

    recommendations = recommend_hybrid(
        user_id,
        top_n=100
    )

    rows = []

    for rank, (item_id, score) in enumerate(
        recommendations,
        start=1
    ):

        rows.append(
            (
                int(user_id),
                int(item_id),
                float(score),
                rank
            )
        )

    cursor.executemany(
        """
        INSERT INTO recommendations
        (user_id, item_id, score, rank)
        VALUES (%s, %s, %s, %s)
        """,
        rows
    )

    if user_id % 50 == 0:
        print(f"Done {user_id} users")


conn.commit()

cursor.close()
conn.close()

print("Precomputation done")