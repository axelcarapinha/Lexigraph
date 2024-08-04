from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def get_word_info(user_context, word):
    template = """
    user_context: {user_context}
    word (correct if misspelled): {word}

    Answer only with the JSON in the following format:
    
        definition: definition of the word,
        dialog (a JSON array, with 6 sentences): 
            person1: SENTENCE 1,
            person2: SENTENCE 2
        
            person1: SENTENCE 3,
            person2: SENTENCE 4
        
            person1: SENTENCE 5,
            person2: SENTENCE 6
    """

    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model # the model will be invoked automatically (the pipe is similar to Linux)

    result = chain.invoke({"user_context": {user_context}, "word": {word}})
    print(result) #TODO remove
    return result

# user_context = "Computer Networks and Cybersecurity"
# word = "passion"
# print(get_word_info(user_context, word))