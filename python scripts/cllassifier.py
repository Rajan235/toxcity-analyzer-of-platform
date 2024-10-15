import json
import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from tqdm import tqdm
import numpy as np

# Load DistilBERT model and tokenizer
model_name = 'distilbert-base-uncased'  # You can change this if using another model
DistilBert_Model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=6)
DistilBert_Tokenizer = DistilBertTokenizer.from_pretrained(model_name)

# Ensure model is on the right device (GPU or CPU)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
DistilBert_Model.to(device)

# Load the JSON data
with open('intertwined_posts_comments222.json', 'r') as f:
    data = json.load(f)

# Function to tokenize and encode the text
def tokenize_and_encode_comments(tokenizer, comments, max_length=64):
    input_ids, attention_masks = [], []
    for comment in comments:
        encoded_dict = tokenizer.encode_plus(
            comment,
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])
    
    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    
    return input_ids, attention_masks

# Prediction function using the model
def predict_comments(comments, model=DistilBert_Model, tokenizer=DistilBert_Tokenizer, device=device):
    # Tokenize and encode the comments
    input_ids, attention_masks = tokenize_and_encode_comments(tokenizer, comments)
    
    # Create a DataLoader
    dataset = TensorDataset(input_ids, attention_masks)
    loader = DataLoader(dataset, batch_size=16, shuffle=False)
    
    # Labels for the 6 toxicity categories
    labels_list = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    
    predictions = []
    model.eval()
    with torch.no_grad():
        for batch in tqdm(loader):
            input_ids, attention_masks = [t.to(device) for t in batch]
            outputs = model(input_ids, attention_mask=attention_masks)
            logits = outputs.logits
            preds = torch.sigmoid(logits).cpu().numpy()
            predictions.extend(preds)
    
    # Return predictions (sigmoid outputs) for each category
    return np.array(predictions), labels_list

# Generate the report for each user, including toxic score
def generate_user_report(data, predictions, labels_list):
    user_reports = {}
    
    index = 0
    for post in data:
        for comment in post['comments']:
            user_id = comment['user_id']
            author_id = comment['author_id']
            
            if author_id not in user_reports:
                user_reports[author_id] = {
                    'author_id': author_id,
                    'user_id': user_id,
                    'total_toxic_score': 0,
                    'category_scores': {label: 0 for label in labels_list},
                    'comments': [],
                    'num_comments': 0  # Track the number of comments per user
                }
            
            # Get the predicted labels for this comment
            predicted_labels = predictions[index]
            index += 1
            
            # Append the comment to the user's report
            user_reports[author_id]['comments'].append({
                'comment_id': comment['comment_id'],
                'content': comment['content'],
                'categories': {labels_list[i]: float(predicted_labels[i]) for i in range(len(labels_list))}
            })
            
            # Update the user's category scores and total toxic score
            for i, label in enumerate(labels_list):
                user_reports[author_id]['category_scores'][label] += float(predicted_labels[i])
            
            # Calculate the toxicity score for this comment (sum of categories)
            toxicity_score = sum(predicted_labels)
            user_reports[author_id]['total_toxic_score'] += float(toxicity_score)
            user_reports[author_id]['num_comments'] += 1  # Increment the comment count
    
    # Normalize scores across all comments
    for report in user_reports.values():
        num_comments = report['num_comments']
        if num_comments > 0:
            # Average toxic score over all comments
            report['toxic_score'] = report['total_toxic_score'] / num_comments
            # Average category scores over all comments
            for label in report['category_scores']:
                report['category_scores'][label] /= num_comments
    
    # Convert user reports to the desired format (array of users)
    user_reports_array = list(user_reports.values())
    
    return user_reports_array

# Classify comments in the JSON data
all_comments = [comment['content'] for post in data for comment in post['comments']]
predictions, labels_list = predict_comments(all_comments)

# Generate a report for each user
user_report = generate_user_report(data, predictions, labels_list)

# Convert numpy types to standard Python types for JSON serialization
def convert_to_serializable(data):
    if isinstance(data, dict):
        return {k: convert_to_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(i) for i in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    else:
        return data

# Convert user report for JSON serialization
serializable_report = convert_to_serializable(user_report)

# Save the report to a JSON file
with open('user_toxicity_report.json', 'w') as f:
    json.dump(serializable_report, f, indent=4)

print("User toxicity report generated successfully.")
