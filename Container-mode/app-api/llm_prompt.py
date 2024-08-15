from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from gtts import gTTS
import os

def get_word_info(user_context, word):
    print(f"[INFO] Getting info about the word '{word}'")

    prompt = """
    user_context: {user_context}
    word (correct if misspelled): {word}

    Answer only with the JSON in the following format:
    
        definition: definition of the word,
        dialog (a JSON array, with 2 pairs of sentences): 
            person1: SENTENCE 1,
            person2: SENTENCE 2
        
            person1: SENTENCE 3,
            person2: SENTENCE 4
    """
    
    # The URL considers that both the API and the Ollama container run in the same network
    model = OllamaLLM(model="llama3", base_url="http://ollama-container:11434")
    prompt = ChatPromptTemplate.from_template(prompt)
    chain = prompt | model # the model will be invoked automatically (the pipe works like the Linux one)

    result = chain.invoke({"user_context": {user_context}, "word": {word}})
    print(result)
    return result

def get_word_pronounce(word, lang='en'):
    tts = gTTS(word) 
    audio_file = f'{word}.mp3'
    tts.save(audio_file)
    return audio_file