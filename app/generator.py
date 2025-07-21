from transformers import pipeline

class Generator:
    def __init__(self):
        self.pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

    def generate_answer(self, query, chunks):
        context = "\n".join([chunk['text'] for chunk in chunks])
        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        output = self.pipeline(prompt, max_length=256)
        return output[0]['generated_text']