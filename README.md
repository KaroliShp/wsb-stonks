# WSB stonks 💵💵💵

Analysing [r/wallstreetbets](https://www.reddit.com/r/wallstreetbets/) for the dankest daily updates. Check our project out at [https://wsbstonks.com](https://wsbstonks.com/)

## 💭 About
We are scraping <i>r/wallstreetbets</i> subreddit and doing some interesting NLP analysis about stock mentions, their popularity across time, and keyword mentions.

To achieve this, we have created a Flask API that handles interaction with MongoDB NoSQL database and schedules cron jobs to scrape <i>r/wallstreetbet</i> with PRAW (Reddit API wrapper). The visualizations of the data are rendered by a React web app, which accesses Flask API via proxy. Both frontend and backend services are hosted on a VM on Digital Ocean Virtual Private Cloud (VPS) Droplet, while for MongoDB service, we use a MongoDB Atlas cloud cluster.

In the past, we used to host GCP App Engine serverless computing environment. If you would like to see how to configurate our React SPA and Python/Flask API for GCP App Engine, head over to [App engine branch of this repo](https://github.com/KaroliShp/wsb-stonks/tree/google-app-engine-deploy).

## 📊 Data Analysis

At the moment, keyword analysis is performed using [pytextrank](https://github.com/DerwenAI/pytextrank). Everything else is built in-house, including stock symbol recognition.

## ⚠️ Disclaimer & Terms of Use

Our website is for informational purposes only. Nothing contained on our Site constitutes investment advice, solicitation, recommendation or endorsement of any investment strategies, practices, or individual decisions. By using this website, you have agreed to assume sole responsibility over assessing risks and merits associated with the use of any content found on the Site. Furthermore, you agree not to hold Site's creators liable for any claim for damages arising from any decision based on content on this Site.

## ⚠️ Statement on data sources

Data used for visualizations has been accessed over Reddit API from <i>r/wallstreetbets</i> subreddit using [PRAW](https://praw.readthedocs.io/en/latest/).
