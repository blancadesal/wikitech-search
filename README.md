# wikitech search

FastAPI-based API for searching wikitech.wikimedia.org using NLP. Key components:

1. Sentence Transformers: These are used to encode or convert text into numerical representations (vectors) that can be understood and processed by the machine learning models.

2. Annoy Index: This is a library that helps in searching for items that are close in similarity to the input query. It is used here to find the sections of text (from Wikitech) that are most similar to the user's query.

3. Question-Answering Model (deepset/tinyroberta-squad2): This is a pre-trained model from the HuggingFace Model Hub that's fine-tuned for question-answering tasks. Given a context and a question, it can provide the most likely answer.

Adapted from <https://github.com/wikimedia/research-api-endpoint-template/tree/wikitech-search>
