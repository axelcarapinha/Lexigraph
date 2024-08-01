MIN_LEN_PASSWORD = 15 
'''
Even though NIST recommends a minimum of 8 for this case (topic 5.1.1.1)
https://pages.nist.gov/800-63-3/sp800-63b.html
'''

MAX_LEN_PASSWORD = 300
'''
TODO: confirm if special characters are NOT recommended by NIST, and search for a max
'''

MIN_LEN_EMAIL = 4
MAX_LEN_EMAIL = 100

MIN_LEN_USERNAME = 8
MAX_LEN_USERNAME = 100

MIN_LEN_WORD = 1
MAX_LEN_WORD = 100 # 55 (buffer) + 45 (pneumonoultramicroscopicsilicovolcanoconiosis, the longest word in the English dictionary, in 2024)