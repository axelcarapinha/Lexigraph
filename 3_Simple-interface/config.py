MIN_LEN_PASSWORD = 15 
'''
Even though NIST recommends a minimum of 8 for this case (topic 5.1.1.1)
https://pages.nist.gov/800-63-3/sp800-63b.html
'''

MAX_LEN_PASSWORD = 300
'''
TODO: confirm if special characters are NOT recommended by NIST, and search for a max
'''

#TODO confirm some values (max number of chars for email, ...)

MIN_LEN_EMAIL = 4
MAX_LEN_EMAIL = 100

MIN_LEN_USERNAME = 8
MAX_LEN_USERNAME = 100

MIN_LEN_WORD = 1
MAX_LEN_WORD = 100 # 55 (buffer) + 45 (pneumonoultramicroscopicsilicovolcanoconiosis, the longest word in the English dictionary, in 2024)

BASE_API_WORD = "http://127.0.0.1:5001/" # base URL for the API responsible for word info



MIN_LEN_OCCUPATION = 1
MAX_LEN_OCCUPATION = 50

ANKI_DECK_NAME = 'Example'

URL_ABOUT_PAGE = "https://axelcarapinha.github.io/Lexigraph/"