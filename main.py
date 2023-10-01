# main.py
import logging
import config
import argparse
from bot.twitter_client import TwitterClient
from bot.metaphor_client import MetaphorClient


def parse_args():
    parser = argparse.ArgumentParser(description="Twitter Bot")
    parser.add_argument("query", help="The query to search for on Twitter")
    parser.add_argument("--num_of_tweets", type=int, default=1, 
                        help="Number of tweets to create and post (default: 1)")
    return parser.parse_args()

def main():
    args = parse_args()

    logging.basicConfig(filename='bot.log', level=logging.INFO, filemode='a')
    logging.info("[TWITTER BOT INITIALISED]")

    metaphor_client = MetaphorClient(config.METAPHOR_API_KEY)
    twitter_client = TwitterClient(
        config.TWITTER_BEARER_TOKEN,
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET_KEY,
        config.TWITTER_ACCESS_TOKEN,
        config.TWITTER_ACCESS_TOKEN_SECRET,
    )

    query = args.query
    num_of_tweets = args.num_of_tweets

    search_results = metaphor_client.search(query, num_of_tweets)
    if(search_results):
        logging.info("[METAPHOR API IS COOL]: Search successful")
        for search in search_results:
            title = search.title
            url = search.url
            id = search.id
            html_content = metaphor_client.get_contents(id)
            if html_content:
                logging.info("[METAPHOR API IS COOL]: Webpage content retrieved")
                cleaned_content = twitter_client.remove_html_tags(html_content)
                tweets = twitter_client.t5_summarizer.summarize(title, cleaned_content, url)
                twitter_client.create_and_post_tweets(tweets)

    logging.info("TWITTER BOT STOPPED")

if __name__ == "__main__":
    main()
