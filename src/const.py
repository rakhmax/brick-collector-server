import os


rebrickableApiKey = os.getenv('API_KEY')
rebrickableApiUrl = 'https://rebrickable.com/api/v3/lego'
rebrickableSearchUrl = 'https://rebrickable.com/search/suggest'

bricklink_consumer_key = os.getenv('BRICKLINK_CONSUMER_KEY')
bricklink_consumer_secret = os.getenv('BRICKLINK_CONSUMER_SECRET')
bricklink_token_value = os.getenv('BRICKLINK_TOKEN_VALUE')
bricklink_token_secret = os.getenv('BRICKLINK_TOKEN_SECRET')
