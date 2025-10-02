# scripts/upload_papers.py
#  Asimple PDF uploader + embedding generator + index builder.
# It assumes you have tools/paper_reader.py and agent/memory.py working together.


import os
from tools.paper_reader import PaperReader
from agent.memory import MemoryManager

# Where your sample PDFs are
PAPERS_DIR = "data/sample_papers/"

def main():
    reader = PaperReader()
    memory = MemoryManager()

    for filename in os.listdir(PAPERS_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PAPERS_DIR, filename)
            print(f"📄 Processing: {filename}")

            # Example: parse PDF into chunks
            chunks = reader.chunk_pdf(pdf_path)
            for chunk in chunks:
                embedding = reader.embed_text(chunk)
                memory.add_to_index(chunk, embedding)

    # Save your FAISS index
    memory.save_index()
    print("✅ All papers uploaded & indexed!")

if __name__ == "__main__":
    main()