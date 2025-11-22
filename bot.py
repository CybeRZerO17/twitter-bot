import tweepy
import openai
import os

# ---- API KEYS ----
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER = os.getenv("BEARER")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

# ---- Twitter Auth ----
client = tweepy.Client(
    bearer_token=BEARER,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# ---- Takip edilecek hesaplar ----
TARGET_USERS = ["@drkaanyl"]

def generate_comment(tweet_text):
    prompt = f"""
    The following tweet should be quoted by a smart AI bot.
    Write a helpful, educational and insightful comment in English.
    Do not be aggressive. Keep it short but meaningful.
    
    Tweet: {tweet_text}
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def main():
    tweeted = False
    for username in TARGET_USERS:
        try:
            user = client.get_user(username=username)
            uid = user.data.id
            tweets = client.get_users_tweets(uid, max_results=5)

            # Eğer kullanıcı tweet atmamışsa test tweeti gönder
            if not tweets.data:
                print("No recent tweets, sending test tweet...")
                client.create_tweet(text="This is a test tweet from my bot 🚀")
                tweeted = True
                break

            # Normal tweet varsa
            tweet = tweets.data[0]
            comment = generate_comment(tweet.text)
            client.create_tweet(
                text=comment,
                quote_tweet_id=tweet.id
            )
            tweeted = True

        except Exception as e:
            print("Error:", e)

    if not tweeted:
        print("No tweet sent.")

if __name__ == "__main__":
    main()
