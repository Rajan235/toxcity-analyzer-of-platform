import json
import numpy as np
from sklearn.cluster import KMeans

# Load the user toxicity report
with open('user_toxicity_report.json', 'r') as f:
    user_report = json.load(f)

# Prepare data for clustering
users_data = []
user_ids = []

for user_id, report in user_report.items():
    toxic_score = report['toxic_score']
    category_scores = list(report['category_scores'].values())
    
    # Create a feature vector for clustering: [toxic_score, category_scores...]
    feature_vector = [toxic_score] + category_scores
    users_data.append(feature_vector)
    user_ids.append(user_id)

# Convert to NumPy array for clustering
X = np.array(users_data)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)  # 3 clusters: High Toxic, Mid Toxic, Low Toxic
kmeans.fit(X)

# Map clusters to toxicity categories
toxicity_categories = {0: "Low Toxic", 1: "Mid Toxic", 2: "High Toxic"}

# Prepare the clustered report
clustered_report = {}

for idx, user_id in enumerate(user_ids):
    cluster_label = kmeans.labels_[idx]
    category = toxicity_categories[cluster_label]
    
    if category not in clustered_report:
        clustered_report[category] = []
    
    clustered_report[category].append(user_id)

# Save the clustered report to a JSON file
with open('user_clustering_results.json', 'w') as f:
    json.dump(clustered_report, f, indent=4)

print("User clustering report generated successfully.")
