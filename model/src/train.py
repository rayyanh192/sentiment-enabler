from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from preprocess import load_data, split_data

# Load and preprocess data
data_path = "./src/compiled_topics.json"
inputs, targets = load_data(data_path)
train_inputs, val_inputs, train_targets, val_targets = split_data(inputs, targets)

# Tokenizer and Model
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Tokenize data
train_encodings = tokenizer(train_inputs, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_inputs, truncation=True, padding=True, max_length=128)

train_labels = tokenizer(train_targets, truncation=True, padding=True, max_length=32)
val_labels = tokenizer(val_targets, truncation=True, padding=True, max_length=32)

# Prepare dataset
class KeywordDataset:
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.encodings.input_ids)

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings.input_ids[idx],
            "attention_mask": self.encodings.attention_mask[idx],
            "labels": self.labels.input_ids[idx],
        }

train_dataset = KeywordDataset(train_encodings, train_labels)
val_dataset = KeywordDataset(val_encodings, val_labels)

# Training arguments
training_args = TrainingArguments(
    output_dir="../models/keyword_classifier",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir="../models/logs",
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Train
trainer.train()
model.save_pretrained("./models/keyword_classifier")
tokenizer.save_pretrained("./models/keyword_classifier")