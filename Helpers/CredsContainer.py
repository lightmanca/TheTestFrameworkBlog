class CredsContainer:

    consumer_key = None
    consumer_secret = None
    access_token = None,
    access_token_secret = None

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
