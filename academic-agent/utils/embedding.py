
from sklearn.feature_extraction.text import TfidfVectorizer

def get_keywords_tfidf(target_text, other_texts):
    docs = other_texts + [target_text]
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(docs)
    scores = X[-1].toarray().flatten()
    terms = vectorizer.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in ranked[:10]]