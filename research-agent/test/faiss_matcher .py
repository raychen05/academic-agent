from matching.faiss_matcher import FAISSNameMatcher

matcher = FAISSNameMatcher("data/author_embeddings.npy", "data/author_names.json")

query = "J Smith"
matches = matcher.match(query)

print("Top matches:")
for m in matches:
    print(f"{m['name']} (distance: {m['score']:.3f})")


'''
Output

Top matches:
John Smith (distance: 0.015)
J. A. Smith (distance: 0.023)
'''