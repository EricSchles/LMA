from app import db

class FAATwitter(db.Model):
    """
    This model stores the tweets and other information relating to congress members.
    parameters:
    @timestamp - when the tweet was written
    @name - name of the tweeter
    @tweet - the text of the tweet
    @hashtag_of_interest - hashtags of interest are present
    @twitter_handle - the twitter handle of the tweeter
    """

    __tablename__ = 'faa_twitter'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String)
    tweet = db.Column(db.String)
    twitter_handle = db.Column(db.String)
    
    def __init__(
            self, timestamp,
            tweet,
            twitter_handle,
    ):
        self.timestamp = timestamp
        self.tweet = tweet
        self.twitter_handle = twitter_handle
