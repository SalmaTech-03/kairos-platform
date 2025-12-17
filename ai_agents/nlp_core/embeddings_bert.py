from transformers import BertTokenizer, BertModel
import torch

class BertEmbedder:
    def __init__(self, model_name='bert-base-uncased'):
        print(f"Loading BERT model: {model_name}...")
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval() # Set to evaluation mode

    def encode(self, text: str) -> list:
        """
        Converts a text string into a 768-dimensional vector.
        """
        # Tokenize and run through model
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # We use the [CLS] token (first token) as the sentence embedding
        # Shape: [1, 768] -> Flatten to list
        embeddings = outputs.last_hidden_state[:, 0, :].numpy().flatten().tolist()
        return embeddings

if __name__ == "__main__":
    # Test
    emb = BertEmbedder()
    vector = emb.encode("Suspicious transaction at 2AM")
    print(f"Vector length: {len(vector)}") # Should be 768