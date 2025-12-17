import spacy

class EntityExtractor:
    def __init__(self, model="en_core_web_sm"):
        print(f" Loading SpaCy model: {model}...")
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f" Model '{model}' not found. Downloading...")
            from spacy.cli import download
            download(model)
            self.nlp = spacy.load(model)

    def extract_entities(self, text: str) -> dict:
        """
        Extracts entities like PERSON, GPE (Location), ORG.
        """
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        return entities