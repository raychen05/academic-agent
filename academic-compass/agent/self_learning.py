import numpy as np
from typing import List, Dict
from agent.memory import MemoryManager
from openai import OpenAI


class SelfLearningAgent:
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.dim = memory_manager.dim

    def store_user_profile(self, user_id: str, interests: List[str], preferences: Dict):
        """
        Create or update a user profile embedding and store it in memory.
        """
        profile_text = f"Interests: {', '.join(interests)} | Preferences: {preferences}"
        embedding = self._embed_text(profile_text)

        self.memory_manager.add_to_index(profile_text, embedding)
        self.memory_manager.store_feedback(
            query=f"user:{user_id}",
            answer=profile_text,
            feedback="profile",
            score=5
        )
        print(f"✅ Profile for {user_id} stored.")

    def retrieve_user_profile(self, user_id: str) -> str:
        """
        Retrieve stored user profile text.
        """
        embedding = self._embed_text(f"user:{user_id}")
        results = self.memory_manager.search_index(embedding, k=1)
        return results[0] if results else ""

    def recommend(self, user_id: str, query: str) -> str:
        """
        Example: personalize an answer by pulling user profile context and combining it with RAG.
        """
        user_profile = self.retrieve_user_profile(user_id)
        personalized_context = f"{user_profile} | User query: {query}"

        # Example: Here you’d run your LLM with this prompt + retrieved chunks
        answer = f"Personalized response based on {personalized_context}"
        return answer

    def _embed_text(self, text: str) -> np.ndarray:
        """
        Dummy embedding generator.
        In production, replace with OpenAI or custom embedding service.
        """
        return np.random.rand(self.dim).astype("float32")
    
    def _embed_text_ai(self, text: str):
        client = OpenAI()
        embedding = client.embeddings.create(
            model="text-embedding-3-large",
            input=text
        ).data[0].embedding
        return np.array(embedding, dtype=np.float32)