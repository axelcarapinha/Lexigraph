import requests
from langchain_core.prompts import ChatPromptTemplate
from gtts import gTTS
import json
import os

def get_word_info(user_context, word):
    print(f"[INFO] Getting info about the word '{word}'")

    prompt_template = """
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

    # Prepare the request
    formatted_prompt = prompt_template.format(user_context=user_context, word=word)
    payload = {
        "model": "llama3",
        "prompt": formatted_prompt,
        "stream": False 
    }
    response = requests.post("http://ollama-container:11434/api/generate", json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
    else:
        result = {"error": f"Request failed with status code {response.status_code}"}
    
    #TODO parse the content correctly again
    print(result.dialog[0])
    return result
    
def get_word_pronounce(word, lang='en'):
    tts = gTTS(word, lang=lang) 
    audio_file = f'{word}.mp3'
    tts.save(audio_file)
    return audio_file
