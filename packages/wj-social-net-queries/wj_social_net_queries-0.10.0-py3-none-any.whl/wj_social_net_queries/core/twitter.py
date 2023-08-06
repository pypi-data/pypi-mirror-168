from typing import Optional, List
from wj_social_net_queries.controllers.twitter_controller import fetch_terms_tweets

from requests_oauthlib import OAuth1Session
import json
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Twitter():
    """
    Description
    ----------
    Allows the use of functions related with Twitter platform
    
    """


    def __init__(
        self,
        twitter_consumer_key: str,
        twitter_consumer_secret: str,
        twitter_key: str,
        twitter_secret: str
    ):
        self.twitter_consumer_key = twitter_consumer_key
        self.twitter_consumer_secret = twitter_consumer_secret
        self.twitter_key = twitter_key
        self.twitter_secret = twitter_secret


    def fetch_terms_tweets(
        self,
        terms: List[str],
        max_tweets_per_term: Optional[int] = 20
    ):
        tweets, terms_updated = fetch_terms_tweets(
            terms=terms,
            twitter_consumer_key=self.twitter_consumer_key,
            twitter_consumer_secret=self.twitter_consumer_secret,
            twitter_key=self.twitter_key,
            twitter_secret=self.twitter_secret,
            max_tweets_per_term=max_tweets_per_term
        )
        return tweets, terms_updated
    
    def write_tweet(
        self,
        tweet: str,
        name: str,
        password: str
    ):
        consumer_key = self.twitter_consumer_key
        consumer_secret = self.twitter_consumer_secret
        name = name
        password = password
        
        # Be sure to add replace the text of the with the text you wish to Tweet.
        # You can also add parameters to post polls, quote Tweets, Tweet with reply settings,
        # and Tweet to Super Followers in addition to other features.
        payload = {"text": tweet}
        
        # Get request token
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
        
        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )
        
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)
        
        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')

        chromedriver_autoinstaller.install()
        ## for windows ##
        driver = webdriver.Chrome()

        ## for linux ##
        #driver = webdriver.Chrome(executable_path='/home/oscar/Labs/robo_journalist/chromedriver')

        driver.get(authorization_url)
        WebDriverWait(driver,
                    10).until(EC.element_to_be_clickable((By.XPATH,
                                                            '//*[@id="username_or_email"]'))).send_keys(name)
        WebDriverWait(driver,
                    10).until(EC.element_to_be_clickable((By.XPATH,
                                                            '//*[@id="password"]'))).send_keys(password)
        WebDriverWait(driver,
                    10).until(EC.element_to_be_clickable((By.XPATH,
                                                            '//*[@id="allow"]'))).click()
        verifier = WebDriverWait(driver,
                                10).until(EC.element_to_be_clickable((By.XPATH,
                                                                    '//*[@id="oauth_pin"]/p/kbd/code'))).get_attribute("innerHTML")
        driver.quit()
        #print("Please go here and authorize: %s" % authorization_url)
        #verifier = input("Paste the PIN here: ")
        
        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        
        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]
        
        # Make the request
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )
        
        # Making the request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )
        
        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )
        
        print("Response code: {}".format(response.status_code))
        
        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
