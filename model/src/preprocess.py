import json
from sklearn.model_selection import train_test_split

def load_data(file_path):
    """Load and preprocess the dataset."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    inputs, targets = [], []
    for entry in data:
        topic = entry['topic']
        for side in entry['sides']:
            side_label = side['side']
            keywords = side['keywords']
            for keyword in keywords:
                inputs.append(f"{topic} {side_label}")
                targets.append(keyword)
    return inputs, targets

def split_data(inputs, targets, test_size=0.2):
    """Split data into training and validation sets."""
    return train_test_split(inputs, targets, test_size=test_size, random_state=42)