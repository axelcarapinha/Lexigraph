import requests
import json
import os
from langchain_core.prompts import ChatPromptTemplate
from gtts import gTTS
from flask import Flask, send_file, request, jsonify

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
        if isinstance(result.get("response"), str):
            try:
                # Parses the nested JSON string
                result["response"] = json.loads(result["response"])
            except json.JSONDecodeError:
                print("Failed to decode the 'response' field as JSON.")
        return json.dumps(result["response"], indent=4)
    else:
        result = {"error": f"Request failed with status code {response.status_code}"}
        return json.dumps(result, indent=4), 500
        
def get_word_pronounce(word, lang='en', directory='audios'):
    try:
        if not os.path.exists(directory): #TODO ensure the directory is made from the container
            os.makedirs(directory)

        filepath = os.path.join(directory, f'{word}.mp3')

        # Generates and saves the audio 
        tts = gTTS(word, lang=lang) # Google's Text to Speach
        tts.save(filepath)

        print(f"[INFO] Audio file created ('{filepath}')")
        return filepath
    except Exception as e:
        print(f"[ERROR] Failed to generate or save audio: {e}")
        return None