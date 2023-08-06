from typing import Optional
import tweepy

# https://docs.tweepy.org/en/stable/api.html#API.search
MAX_QUERY_LENGTH = 500
# https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets # noqa: B950
MAX_TWEETS_PER_PAGE_SEARCH = 100
# https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline # noqa: B950
MAX_TWEETS_PER_PAGE_USER_TIMELINE = 200


class TwitterWJ:

    def __init__(
        self,
        twitter_consumer_key: str,
        twitter_consumer_secret: str,
        twitter_key: str,
        twitter_secret: str
    ):
        """Instanciate a tweepy object"""
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_key, twitter_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=3)


    def get_user(self, screen_name: str):
        """
        Description
        ----------
        Given a Twitter screen_name, gets tweepy user object.

        Arguments
        ---------
        screen_name: str
            The screen name, handle, or alias that this user identifies themselves
            with. screen_names are unique but subject to change
            
        Return
        -------
        The user object or error message
            ResponseObject, str | None, error_message
        """
        try:
            user = self.api.get_user(screen_name=screen_name)
            if getattr(user, "protected", False):
                return None, "Protected account"
            return user, ""
        except tweepy.NotFound as e:
            # No twitter account found with screen_name
            return None, str(e)
        except tweepy.Forbidden as e:  # User has been suspended
            return None, str(e)


    def get_term_tweets(
        self,
        term:str,
        num_tweets: Optional[int] = 20,
        since_id: Optional[str] = None,
        lang: Optional[str] = "es",
        result_type: Optional[str] = "mixed"
    ):
        """
        Description
        ----------
        Gets all tweets from a term. Uses twitter search.

        Arguments
        ---------
        term:
            Tweets names
        num_tweets:
            Number of max tweets captured in the request.
        since_id:
            Last tweet id
        lang:
            Language used to make the search
        result_type:
            Specifies what type of search results you would prefer to receive.
            The current default is “mixed.” Valid values include:
             -mixed: include both popular and real time results in the response
             -recent: return only the most recent results in the response
             -popular: return only the most popular results in the response
        Return
        -------
        The user object or error message
            ResponseObject, str | None, error_message
        """
        if not term:
            return []
        if len(term) > MAX_QUERY_LENGTH:
            return []
        params = {
            "q": f"{term} -filter:retweets",  # Exclude retweets
            "lang": lang,
            "result_type": result_type,
            "since_id": since_id,
            "count": MAX_TWEETS_PER_PAGE_SEARCH,  # Max results per page
        }
        return self.__fetch_data(self.api.search_tweets, params, num_tweets)


    def get_user_tweets(
        self,
        user_id: str,
        num_tweets: Optional[int] = 20,
        since_id: Optional[str] = None
    ):
        """
        Description
        ----------
        Gets all user tweets.

        Arguments
        ---------
        user_id:
            id of the user to search tweets.
        num_tweets:
            Number of max tweets captured in the request.
        since_id:
            Last tweet id
            
        Return
        -------
        Dictionary with all Tweet parameters
            Dict
        """
        if not user_id:
            return []
        params = {
            "user_id": user_id,
            "since_id": since_id,
            "count": MAX_TWEETS_PER_PAGE_USER_TIMELINE,
            "include_rts": False,  # Exclude retweets
            "exclude_replies": False,  # Include replies
        }
        return self.__fetch_data(self.api.user_timeline, params, num_tweets)


    def get_tweet(
        self,
        tweet_id: str
    ):
        """
        Description
        ----------
        Gets a specific tweet.

        Arguments
        ---------
        tweet_id:
            Id of tweet
            
        Return
        -------
        Dictionary with all Tweet parameters
            Dict
        """
        try:
            status = self.api.get_status(id=tweet_id, tweet_mode="extended")
            if not getattr(status, "possibly_sensitive", False):
                return self.__format_tweet(status)
            else:
                return None
        except tweepy.errors.TweepyException as e:
            print(
                f"Tweepy exception. Method: get_status "
                f"Params: {tweet_id} Detail: {e}"
            )
            return None


    def lookup_tweets(self, tweet_ids):
        """Retrieve a list of tweet dictionaries given a list of tweet ids."""
        try:
            tweets = self.api.lookup_statuses(id=tweet_ids, tweet_mode="extended")
            return [self.__format_tweet(tweet) for tweet in tweets]
        except tweepy.errors.TweepyException:
            return []


    def __fetch_data(self, method, params, num_tweets=1):
        """Pagination function."""
        try:
            tweets = tweepy.Cursor(method, tweet_mode="extended", **params).items(
                num_tweets
            )
            return [
                self.__format_tweet(status)
                for status in tweets
                if not getattr(status, "possibly_sensitive", False)
            ]
        # If any exception occurs, return empty tweets
        # Includes 401 Unauthorized, private twitter accounts
        # TODO: Handle this better!
        except tweepy.errors.TweepyException as e:
            print(
                f"Tweepy exception. Method: {method} "
                f"Params: {params} Items: {num_tweets} Detail: {e}"
            )
            return []

    @staticmethod
    def __format_tweet(status):
        """Formats final tweet response."""
        return {
            "tweet_id": status.id,
            "screen_name": status.user.screen_name,
            "twitter_id": status.user.id,
            "created_at": status.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "text": status.full_text,
            "place": getattr(status.place, "full_name", None),
            "in_reply_to_status_id": status.in_reply_to_status_id,
            "quoted_status_id": getattr(status, "quoted_status_id", None),
            "favorite_count": status.favorite_count,
            "retweet_count": status.retweet_count,
            "followers_count": status.user.followers_count,
            "friends_count": status.user.friends_count,
            "retweet_id": status.retweeted_status.id
            if hasattr(status, "retweeted_status")
            else None,
            "lang": status.lang,
        }