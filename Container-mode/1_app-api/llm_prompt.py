import requests
import json
from langchain_core.prompts import ChatPromptTemplate
from gtts import gTTS
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
        if isinstance(result.get("response"), str):
            try:
                # Parses the nested JSON string
                result["response"] = json.loads(result["response"])
            except json.JSONDecodeError:
                print("Failed to decode the 'response' field as JSON.")

        print(json.dumps(result["response"], indent=4))
        return json.dumps(result["response"], indent=4)
    else:
        result = {"error": f"Request failed with status code {response.status_code}"}
        print(json.dumps(result, indent=4))
        return json.dumps(result, indent=4)
        
def get_word_pronounce(word, lang='en'):
    tts = gTTS(word, lang=lang) 
    audio_file = f'{word}.mp3'
    tts.save(audio_file)
    return audio_file