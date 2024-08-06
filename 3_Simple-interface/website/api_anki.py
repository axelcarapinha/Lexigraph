import config
import json

def api_anki_get_card_notes(input_word, info_word):
    print(f"[INFO] [CMD ADD] Adding word '{input_word}' to the deck '{config.ANKI_DECK_NAME}'.")

    # Extract dialog parts from the word object
    dialog_parts = info_word.get('dialog', [])

    # Create the ANKI card
    deck_name = config.ANKI_DECK_NAME
    model_name = "basic"
    front_text = f"{input_word}"

    # Generates the HTML content for the card's back
    back_text = f'''
    <ul>
        <li> 
            <u>Word</u>: {input_word}
            <br>
            <u>Meaning</u>: {info_word.get('definition', 'No definition available')}
            <br>
            <ul>
    '''
    
    # Add dialog parts to the HTML for the card
    for i, dialog_part in enumerate(dialog_parts):
        back_text += f'''
                <!-- PART {i + 1} / {len(dialog_parts)} -->
                <li>
                    <strong>Bob:</strong>   {dialog_part.get('person1', 'No text available')}
                    <br>
                    <strong>Alice:</strong> {dialog_part.get('person2', 'No text available')}
                    <br>
                </li>
        '''
    back_text += '''
            </ul>
        </li>
    </ul>
    '''

    # Remove all newlines from the back_text (were being presented after the JSON.stringify())
    back_text = back_text.replace('\n', '')

    # Build the JSON for the card
    tags = ["lexigraph"]
    audio_url = f"http://127.0.0.1:5001/wordpronounce/{front_text}"
    audio_filename = "filename_audio.mp3"
    video_url = "url_video"
    video_filename = "filename_video.mp4"
    picture_url = "url_picture"
    picture_filename = "filename_pictre.jpg"
    notes = [{
        "deckName": deck_name,
        "modelName": model_name,
        "fields": {
            "Front": front_text,
            "Back": back_text
        },
        "tags": tags,
        #TODO
        # "audio": [{
        #     "url": audio_url,
        #     "filename": f'{front_text}.mp3',
        #     "skipHash": "skip_hash",  
        #     "fields": ["Front"]
        # }],
    }]

    return notes
