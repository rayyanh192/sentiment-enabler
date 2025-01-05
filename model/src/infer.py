from transformers import T5Tokenizer, T5ForConditionalGeneration

def generate_keywords(topic, side, model_path="../models/keyword_classifier"):
    """Generate keywords for a given topic and side."""
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    input_text = f"{topic} {side}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_length=32, num_return_sequences=10)
    keywords = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    return keywords

# Example usage
topic = "climate change"
side = "pro-climate action"
print(generate_keywords(topic, side))