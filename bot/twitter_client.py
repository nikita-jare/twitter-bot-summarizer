# bot/twitter_client.py
import tweepy
from datetime import datetime, timedelta
import textwrap
import traceback
from bs4 import BeautifulSoup
from transformers import T5ForConditionalGeneration, T5Tokenizer
import logging

class TwitterClient:
    def __init__(self, bearer_token, api_key, api_secret_key, access_token, access_token_secret):
        self.twitter_client = tweepy.Client(bearer_token, api_key, api_secret_key, access_token, access_token_secret)
        self.twitter_me_id = self.twitter_client.get_me()[0].id
        self.tweet_response_limit = 10
        self.t5_summarizer = T5Summarizer()

    def create_and_post_tweets(self, tweets):
        try:
            tweet_ids = []
            response = self.twitter_client.create_tweet(text=tweets[0])
            tweet_id = response.data['id']
            tweet_ids.append(response.data['id'])

            for i in range(1,len(tweets)):
                # Create a thread if the tweet length exceeds maximum limit
                response = self.twitter_client.create_tweet(
                text = tweets[i],
                in_reply_to_tweet_id=tweet_id
                )
                tweet_ids.append(response.data['id'])
                tweet_id = response.data['id']
            logging.info(f"[Go CHECKOUT YOUR TWEET] : {tweets}")

        except Exception as e:
            logging.error(f"[AHHH! ERROR POSTING TWEETS] : {str(e)}")
            traceback.print_exc()

    def remove_html_tags(self, text):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(text, "html.parser")
        clean_text = soup.get_text()
        logging.info(f"[ALL CLEANED UP]")
        return clean_text

    def get_trending_topics(self, location_id=1):
        pass

    def generate_response(self, mentioned_conversation_tweet_text):
        pass

    def respond_to_mention(self, mention):
        response_text = self.generate_response(mention.text)
        
        # Try and create the response to the tweet. If it fails, log it and move on
        try:
            response_tweet = self.twitter_client.create_tweet(text=response_text, in_reply_to_tweet_id=mention.id)
        except Exception as e:
            print (e)
            return
        
        return True

    def get_mentions(self):
        # Get current time in UTC
        now = datetime.utcnow()
        start_time = now - timedelta(minutes=20)

        # Convert to required string format
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return self.twitter_client.get_users_mentions(id=self.twitter_me_id,
                                                   start_time=start_time_str,
                                                   tweet_fields=['created_at', 'conversation_id']).data


    def respond_to_mentions(self):
        mentions = self.get_mentions()
        # If no mentions, just return
        if not mentions:
            print("No mentions found")
            return
        
        for mention in mentions[:self.tweet_response_limit]:
            # Getting the mention's conversation tweet            
            self.respond_to_mention(mention)
        return True

class T5Summarizer:
    def __init__(self):
        self.t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")
        self.t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")

    def summarize(self, title, text, url, max_summary_length=280):
         # Limit the maximum length of the summary to fit within 280 characters
        tweets = []
        url_length = len(url)
        max_text_length = max_summary_length - len(f"Title: {title}") - url_length  # Account for the title in the tweet
        
        input_ids = self.t5_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = self.t5_model.generate(input_ids, min_length=40, max_length = 1000, length_penalty=2.0, num_beams=4, early_stopping=True)

        summary = self.t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        total_summary = len(summary) + len(f"Title:{title}\n(Part 10)\n{url}")

        if total_summary > max_summary_length:
            part1 = summary[:max_text_length]
            tweet_text = f"Title:{title}\n{part1}\n{url}"
            tweets.append(tweet_text)

            summary_parts = textwrap.wrap(summary[max_text_length:], width=280, break_long_words=False, replace_whitespace=False)
            for i, part in enumerate(summary_parts):
                tweet_text = f"(Part {i + 1})\n{part}"
                tweets.append(tweet_text)
        else:
            # Combine the title and summary into a single tweet
            summary_with_title = f"Title: {title}\n{summary}\n{url}"
            tweets.append(summary_with_title)
        logging.info(f"[ALL SUMMARIZED JUST FOR YOU]")
        return tweets        
