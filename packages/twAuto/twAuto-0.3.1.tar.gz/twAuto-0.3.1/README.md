
  

# twAuto - Twitter Automation Test Tool 🦆

  

twAuto is a library for testing your code on pre-Twitter API application stage. This library can do "Tweeting", "Retweeting", "Replying", "Tweet Quoting", "Tweet Liking" without any API requirements using Selenium.

  

###Only For Testing Purposes!!!###



## Requirements

- Python 3.6;

- beautifulsoup4;

- selenium

  

## Installation
 **Pip:**
```bash
pip3 install twAuto
```

**After Pip:**
Download chromium driver from https://chromedriver.chromium.org/downloads and place the chromedriver.exe file to same place as your code.
```bash
https://chromedriver.chromium.org/downloads
```

## Functions
**- Import:**
```python
import twAuto
```

**- Configure:**
```python
tw = twAuto.twAuto(
username="Your Twitter Username",
email="Your Twitter E-Mail",
password="Your Twitter Password",
headless=True/False)
```

**- Start:** Start functions runs the selenium driver.
```python
tw.start()
```

**- Login:** Logs in to the Twitter account
```python
tw.login()
```

**- Like:** Likes tweet in the given url
```python
tw.like(url="")
```

**- Reply:** Replies to the tweet in the given url with given text.
```python
tw.reply(url="", text="")
```

**- Tweet:** Tweets the text and image if given.
```python
tw.tweet(text="",imgpath="")
```

**- Quote Tweet:** Quotes the tweet in the given url with the given text.
```python
tw.quoteTweet(url="", text="")
```

**- Retweet:** Retweets the tweet in the given url.
```python
tw.retweet(url="")
```

**- Logout:** Logs out from current Twitter account and deletes the cookies file.
```python
tw.logout()
```

**- Quit/Close:** Ends the session, closes the selenium driver application
```python
tw.close()
```