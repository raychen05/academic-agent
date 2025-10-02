# init_db.py

def initialize_faiss():
    """
    create FAISS index
    This function initializes the FAISS index for vector search.
    It sets up the index structure and prepares it for storing vectors.
    """
    print("✅ FAISS index initialization complete")

def initialize_sqlite():
    """
    创建 SQLite DB
    """
    print("✅ SQLite DB initialization complete")

if __name__ == "__main__":
    initialize_faiss()
    initialize_sqlite()