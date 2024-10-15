# import pandas as pd
# import random
# import json
# from faker import Faker

# # Initialize Faker for generating dummy data
# fake = Faker()

# # Load the CSV file with comment content
# csv_file_path = 'train.csv'  # Replace with your actual path
# comments_df = pd.read_csv(csv_file_path)

# # Extract comments into a list
# comments = comments_df['comment_text'].tolist()  # Change to your actual column name

# # Parameters
# num_users = 100  # Number of unique users
# num_posts = 50   # Number of unique posts
# comments_per_user = 20  # Average number of comments per user

# # Generate user IDs and post IDs
# user_ids = [fake.user_name() for _ in range(num_users)]
# post_ids = [fake.uuid4() for _ in range(num_posts)]

# # Prepare the intertwined data
# intertwined_data = []

# for user_id in user_ids:
#     # Generate comments for the user
#     for _ in range(comments_per_user):
#         # Randomly select a post ID and a comment content
#         post_id = random.choice(post_ids)
#         comment_content = random.choice(comments)

#         comment_data = {
#             "comment_id": fake.uuid4(),  # Unique comment ID
#             "comment_author_user_id": user_id,  # Author of the comment
#             "post_id": post_id,  # ID of the post
#             "post_author_user_id": fake.user_name(),  # Random post author (can be made unique if needed)
#             "comment_content": comment_content  # Content of the comment
#         }
#         intertwined_data.append(comment_data)

# # Save to a JSON file
# with open("intertwined_comments.json", "w") as json_file:
#     json.dump(intertwined_data, json_file, indent=2)

# print("Intertwined comments dataset generated.")

import pandas as pd
import random
import json
import uuid
from faker import Faker

# Initialize Faker for generating dummy data
fake = Faker()

# Load the CSV file with comment content
csv_file_path = 'test.csv'  # Replace with your actual path
comments_df = pd.read_csv(csv_file_path)

# Extract comments into a list
comments = comments_df['comment_text'].tolist()  # Change to your actual column name

# Parameters
num_users = 70  # Number of unique users
num_posts = 20   # Number of unique posts
comments_per_post = 20  # Average number of comments per post

# Create unique user and author ID pairs
user_author_pairs = [(fake.user_name(), str(uuid.uuid4())) for _ in range(num_users)]
user_ids, author_ids = zip(*user_author_pairs)  # Unzip into separate lists

# Prepare the posts
posts = []
for _ in range(num_posts):
    # Randomly select a user for the post
    user_index = random.randint(0, num_users - 1)
    user = user_ids[user_index]
    author_id = author_ids[user_index]  # Corresponding UUID for the selected user
    
    post_data = {
        "post_id": str(uuid.uuid4()),  # Unique post ID
        "post_title": fake.sentence(nb_words=10),  # Random title
        "author_id": author_id,  # Use the same UUID for the post author
        "user_id": user,  # Use the same username for the post user
        "comments": []
    }
    posts.append(post_data)

# Assign comments to posts using the same users for multiple posts
for post in posts:
    # Randomly select users for comments, ensuring some users are reused
    commenters = random.sample(user_ids, k=random.randint(2, 5))  # Select 2 to 5 unique commenters for each post
    for user in commenters:
        for _ in range(comments_per_post // len(commenters)):  # Distribute comments evenly
            # Get the corresponding author_id for the user
            author_id_index = user_ids.index(user)
            comment_data = {
                "comment_id": str(uuid.uuid4()),  # Unique comment ID
                "author_id": author_ids[author_id_index],  # Corresponding UUID for the comment author
                "user_id": user,  # Same as comment author (username)
                "content": random.choice(comments)  # Random comment content from the CSV
            }
            post["comments"].append(comment_data)

# Save to a JSON file
with open("intertwined_posts_comments222.json", "w") as json_file:
    json.dump(posts, json_file, indent=2)

print("Intertwined posts and comments dataset generated with unique user and author IDs.")
