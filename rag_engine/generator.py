from typing import List
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from rag_engine import config

class ResponseGenerator:
    def __init__(self):
        self.llm = OllamaLLM(
            model = config.CHAT_MODEL,
            temperature = config.TEMPERATURE,
            max_tokens = config.MAX_TOKENS
        )

        self.prompt_template = PromptTemplate(
            input_variables=['conversation', 'context', 'question'],
            template="""
You are a helpful assistant.
Use only the provided context to answer the question.
If the answer is not in the context, say you don't know.

Previous Conversation: {conversation}
Context: {context}
Question: {question}
Answer:
            """
        )

    def generate(self, question: str, documents: List[Document], history: List[dict] = None) -> str:
        if history is None:
            history = []
        if not documents:
            return "No relevant information found."

        context = "\n\n".join([doc.page_content for doc in documents])

        conversation = ""
        for turn in history:
            conversation += (
                f"User: {turn['question']}\n"
                f"Assistant: {turn['answer']}\n"
            )

        prompt = self.prompt_template.format(
            conversation=conversation,
            context=context,
            question=question
        )

        response = self.llm.invoke(prompt)

        if isinstance(response, str):
            return response
        return response.content.strip()