import os
import nltk
import spacy
from collections import Counter
from datetime import datetime
from nltk.tokenize import word_tokenize, sent_tokenize
from spacy import displacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")


# The Complex Automated Legal Document Drafting Agent
class ComplexAutomatedLegalDocumentDraftingAgent:

    def __init__(self, document_path):
        self.document_path = document_path
        self.document_text = ""
        self.legal_terms = ["lawsuit", "defendant", "plaintiff", "contract", "agreement", "litigation"]
        self.legal_entities = ["defendant", "plaintiff", "judge", "court", "law", "lawsuit", "litigation"]
        self.citations = []
        self.keywords = []
        self.legal_clauses = []

    def load_document(self):
        if os.path.exists(self.document_path):
            with open(self.document_path, 'r') as file:
                self.document_text = file.read().replace('\n', ' ')
        else:
            print("Document not found.")

    def process_document(self):
        """
        Process the document by extracting legal terms, entities, and references.
        Uses NLP techniques like tokenization, NER, and keyword extraction.
        """
        doc = nlp(self.document_text)
        words = word_tokenize(self.document_text)

        # Count legal terms
        legal_term_count = {term: 0 for term in self.legal_terms}
        for word in words:
            if word.lower() in self.legal_terms:
                legal_term_count[word.lower()] += 1

        # Named Entity Recognition (NER)
        entities = doc.ents
        entity_count = Counter([ent.label_ for ent in entities])

        # Extract citations (e.g., legal references like cases, laws, etc.)
        # A basic example here, you can improve this by pattern matching for case numbers or laws.
        self.citations = [ent.text for ent in entities if ent.label_ == "LAW"]

        # Extract keywords using TF-IDF
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
        tfidf_matrix = tfidf_vectorizer.fit_transform([self.document_text])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        self.keywords = feature_names

        return legal_term_count, entity_count, self.citations, self.keywords

    def draft_summary(self, legal_term_count, entity_count, citations, keywords):
        """
        Drafts a detailed summary of the document, highlighting the legal terms, entities, citations, and key concepts.
        """
        summary = "Summary of Legal Document:\n\n"
        summary += "Legal Term Frequency:\n"
        for term, count in legal_term_count.items():
            summary += f"- The term '{term}' has been used {count} times.\n"

        summary += "\nEntities Identified:\n"
        for entity, count in entity_count.items():
            summary += f"- {entity}: {count} occurrences.\n"

        summary += "\nLegal Citations Found:\n"
        if citations:
            for citation in citations:
                summary += f"- {citation}\n"
        else:
            summary += "No legal citations found.\n"

        summary += "\nKeywords Identified:\n"
        for keyword in keywords:
            summary += f"- {keyword}\n"

        return summary

    def generate_legal_clauses(self):
        """
        Generates new legal clauses based on existing patterns in the document.
        For simplicity, we’ll assume that if certain keywords or legal terms are identified, a standard clause
        is generated. You can expand this by using a template system or machine learning models.
        """
        clauses = []
        if "contract" in self.keywords:
            clauses.append(
                "This agreement is binding upon the parties and shall remain in effect until terminated by mutual consent.")
        if "defendant" in self.keywords or "plaintiff" in self.keywords:
            clauses.append(
                "The Defendant agrees to comply with the terms outlined in this document and acknowledges the Plaintiff's claims.")

        self.legal_clauses = clauses
        return clauses

    def visualize_entities(self):
        """
        Visualizes named entities using spaCy's displaCy tool.
        """
        doc = nlp(self.document_text)
        displacy.render(doc, style="ent", page=True)


if __name__ == "__main__":
    agent = ComplexAutomatedLegalDocumentDraftingAgent("path_to_legal_document")

    # Load and process document
    agent.load_document()
    legal_term_count, entity_count, citations, keywords = agent.process_document()

    # Generate summary of document
    summary = agent.draft_summary(legal_term_count, entity_count, citations, keywords)
    print(summary)

    # Generate legal clauses based on the document's context
    clauses = agent.generate_legal_clauses()
    print("\nGenerated Legal Clauses:")
    for clause in clauses:
        print(clause)

    # Visualize legal entities (requires web browser)
    agent.visualize_entities()
