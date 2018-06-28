from app import db

class FAATwitter(db.Model):
    """
    This model stores the tweets and other information relating to congress members.
    parameters:
    @timestamp - when the tweet was written
    @tweet - the text of the tweet
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

        
class Hashtag(db.Model):
    """
    This model stores hashtags of interest with the following parameters:
    @hashtag - any hashtags of interest
    @faa_twitter_id - the id from FAATwitter table
    """

    __tablename__ = 'hashtag'
    id = db.Column(db.Integer, primary_key=True)
    faa_twitter_id = db.Column(db.Integer)
    hashtag = db.Column(db.String)

    def __init__(self,faa_twitter_id, hashtag):
        self.faa_twitter_id = faa_twitter_id
        self.hashtag = hashtag
