# Twitter Bot Summarizer 🤖📰

Welcome to Twitter Bot Summarizer – the ultimate tool for generating concise summaries of trending topics from Twitter! This innovative project combines the power of Twitter's real-time data with natural language processing to bring you summarized insights and more.

## Features ✨
- **Find recent relevant information** Using Metaphor API, retrieve latest relevant information to the topic.
- **Summarize:** Summarize your tweets.
- **Tweet Publishing:** Publish the generated summaries as tweets from your Twitter account.
- **Scheduled Execution:** Schedule the bot to run at specific intervals and keep your followers updated.
- **Easy to Use:** Simple configuration and setup to get you started in no time.

## Getting Started 🚀

Follow these steps to get started with the Twitter Bot Summarizer:

1. Clone this repository:
   ```bash
   git clone https://github.com/nikita-jare/twitter-bot-summarizer.git
   cd twitter-bot-summarizer

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Configure your Twitter API and Metaphor API credentials and other settings in config.py.
   ```bash
   # config.py
   TWITTER_API_KEY = 'your_twitter_api_key'
   TWITTER_API_SECRET_KEY = 'your_twitter_api_secret_key'
   TWITTER_ACCESS_TOKEN = 'your_twitter_access_token'
   TWITTER_ACCESS_TOKEN_SECRET = 'your_twitter_access_token_secret'
   TWITTER_BEARER_TOKEN = 'your_twitter_bearer_token'

   # Metaphor API key
   METAPHOR_API_KEY = 'your_metaphor_api_key'

4. Create a list of topics or keywords you want to track in query_list.txt.
   ```bash
      Example: <query> <numer_of_tweets>
      What is JWT in Javascript?
      Most innovative AI projects
      Where to party in NYC?, 2

6. Run the Twitter Bot Summarizer:
    ```bash
    python scheduler.py


Contact 📧
Have questions, suggestions, or just want to chat? Feel free to reach out to me:

Email: nikitajare2022@gmail.com
Twitter: @JareNikita
