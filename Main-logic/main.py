from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


template = """
Follow the instrcutions below, considering you are
an expert on english vocabulary.

Consider this word: {word}
Consider this profile of the user: {user_context}

Answer me just with 5 lines:
the first for the meaning of the provided word,
the other 4 for a simple dialog using the word
considering the provided context of the user

If the word does NOT exist, send empty JSON.

Answer just with JSON format.
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model # the model will be invoked automatically (the pipe is similar to Linux)

result = chain.invoke({"user_context": "Network Engineer", "word": "Passion"})
print(result)


# if __name__ == "__main__":
