import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake=Faker()
random.seed(42)
Faker.seed(42)

num_users=20
num_items=50
num_interactions=200

categories = [
    "comedy", "fitness", "fashion", "gaming", "food", "travel",
    "education", "music", "sports", "beauty", "tech", "memes", "news"
]

interaction_types = [
    "skip",
    "view",
    "like",
    "share",
    "save"
]

users=[]
for user_id in range(1, num_users+1):
   users.append({
      "id":user_id,
      "name": fake.name(),
      "created_at":fake.date_time_between(start_date="-5y", end_date="now") 
    })
   

items=[]
for item_id in range(1, num_items+1):
   category=random.choice(categories)
   items.append({
      "id":item_id,
      "title": f"{category.title()} Reel",
      "category":category,
      "created_at":fake.date_time_between(start_date="-2y", end_date="now")
     
   })

interaction_rules={
   "skip": {
      "watch_range":(0.01, 0.20),
      "strength_range":(0.05, 0.15),
      "rewatch_range":(0,0)
   },
   "view": {
      "watch_range":(0.21, 0.60),
      "strength_range":(0.16, 0.50),
      "rewatch_range":(0,1)
   },
   "like": {
      "watch_range":(0.61, 0.80),
      "strength_range":(0.51, 0.75),
      "rewatch_range":(0,2)
   },
   "save": {
      "watch_range":(0.81, 1.00),
      "strength_range":(0.75, 0.95),
      "rewatch_range":(2,4)
   },
   "share": {
      "watch_range":(0.70, 1.00),
      "strength_range":(0.80, 1.00),
      "rewatch_range":(1,5)
   }
}


interactions=[]
for interaction_id in range(1,num_interactions+1):
   interaction_type=random.choices(
          ["skip", "view", "like", "share", "save"],
           weights=[35,30,20,10,5]
          )[0]
   rule=interaction_rules[interaction_type]
   interactions.append({
    "id":interaction_id,
    "user_id":random.randint(1,num_users),
    "item_id":random.randint(1,num_items),
    "interaction_type":interaction_type,
    "interaction_strength":round(random.uniform(*rule["strength_range"]),2),

    "watch_percentage":round(random.uniform(*rule["watch_range"]),2),
    "rewatch_count":random.randint(*rule["rewatch_range"]),
    "timestamp":fake.date_time_between(start_date="-60d", end_date="now")
   })
   
