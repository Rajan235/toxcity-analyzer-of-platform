import json
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from scipy import stats

# Load the user toxicity report
with open('user_toxicity_report.json', 'r') as f:
    user_report = json.load(f)

# Extract toxicity scores
toxicity_scores = np.array([report['toxic_score'] for report in user_report.values()])

# Method 1: Calculate Z-scores
def get_z_scores(scores):
    return stats.zscore(scores)

# Method 2: Isolation Forest for outlier detection
def detect_outliers_isolation_forest(scores):
    model = IsolationForest(contamination=0.1)  # Adjust contamination to your needs
    model.fit(scores.reshape(-1, 1))  # Reshape for the model
    return model.predict(scores.reshape(-1, 1))

# Method 3: One-Class SVM for outlier detection
def detect_outliers_one_class_svm(scores):
    model = OneClassSVM(gamma='auto', nu=0.1)  # nu is the proportion of outliers
    model.fit(scores.reshape(-1, 1))  # Reshape for the model
    return model.predict(scores.reshape(-1, 1))

# Calculate Z-scores
z_scores = get_z_scores(toxicity_scores)
# Identify outliers using Z-scores (threshold set to 3 for outliers)
outliers_z = np.where(np.abs(z_scores) > 3)[0]

# Identify outliers using Isolation Forest
outliers_if = detect_outliers_isolation_forest(toxicity_scores)
outliers_if_indices = np.where(outliers_if == -1)[0]

# Identify outliers using One-Class SVM
outliers_svm = detect_outliers_one_class_svm(toxicity_scores)
outliers_svm_indices = np.where(outliers_svm == -1)[0]

# Print the indices of the detected outliers
print("Outliers detected using Z-scores:", outliers_z)
print("Outliers detected using Isolation Forest:", outliers_if_indices)
print("Outliers detected using One-Class SVM:", outliers_svm_indices)

# Generate user reports with comments and toxicity scores, including flagged users
user_reports_with_flags = {}
flagged_users = []

for user_id, report in user_report.items():
    toxic_score = report['toxic_score']
    
    # Check if the user's toxicity score is an outlier
    flagged = False
    
    if user_id in outliers_z:
        flagged = True
        flagged_users.append(user_id)
    elif user_id in outliers_if_indices:
        flagged = True
        flagged_users.append(user_id)
    elif user_id in outliers_svm_indices:
        flagged = True
        flagged_users.append(user_id)
    
    # Prepare the user's report
    user_reports_with_flags[user_id] = {
        'toxic_score': toxic_score,
        'comments': [],  # Will store comments with their toxicity scores
        'flag': flagged  # Set flag based on toxicity score
    }
    
    # Include each comment and its toxicity score
    for comment in report['comments']:
        comment_id = comment['comment_id']
        comment_content = comment['content']
        # Calculate toxicity score for this comment (if available in the report)
        comment_toxicity_score = sum(comment['categories'].values())  # Sum of the toxicity categories
        
        user_reports_with_flags[user_id]['comments'].append({
            'comment_id': comment_id,
            'content': comment_content,
            'toxicity_score': comment_toxicity_score
        })

# Save all user reports with flags
with open('user_reports_with_flags1.json', 'w') as f:
    json.dump(user_reports_with_flags, f, indent=4)

# Save flagged users in a separate file
with open('flagged_users1.json', 'w') as f:
    json.dump(flagged_users, f, indent=4)

print("User reports with anomaly detection generated successfully. Flagged users saved.")
