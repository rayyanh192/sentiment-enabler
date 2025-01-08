from transformers import T5Tokenizer, T5ForConditionalGeneration
import re

def generate_keywords(topic, side, model_path="./models/keyword_classifier"):
    """Generate keywords for a given topic and side."""
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    input_text = f"{topic} {side}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Use beam search to support multiple sequences
    outputs = model.generate(
        input_ids, 
        max_length=32, 
        num_return_sequences=10,  # Generate 10 outputs
        num_beams=10,             # Use 10 beams for better diversity
        repetition_penalty=2.0,   # Penalize repetition
        early_stopping=True       # Stop when an end condition is met
    )

    # Decode and clean keywords
    raw_keywords = [tokenizer.decode(output, skip_special_tokens=True).strip() for output in outputs]

    # Compile a regex pattern to match topic words (case-insensitive, word boundaries)
    topic_pattern = re.compile(rf'\b{topic}\b', re.IGNORECASE)

    # Filter out keywords containing the topic word
    filtered_keywords = [
        keyword for keyword in raw_keywords 
        if not topic_pattern.search(keyword)
    ]

    return filtered_keywords

# Example usage
topic = "climate change"
side = "pro-climate action"
print(generate_keywords(topic, side))