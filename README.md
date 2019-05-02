## Gathering Steam
### Insight Data Science Fellowship Project

### Author: [Tyler Blair](https://www.linkedin.com/in/tylerjblair)


----


An interactive demonstration of the results can be found on my [personal website](tylerblair.net).  

A four-minute video of me demonstrating the product can also be found [here](https://youtu.be/fnirYwyQ7Aw).

----

#### Overview:   

Game ratings have the ability to affect a game's visibility, sales, and ultimately, revenue. However, Steam's rating system is binary (thumbs-up/thumbs-down) and offers a limited picture of the game's future performance. With this in mind, I developed Gathering Steam.

Utilizing sentiment analysis of Steam game reviews as a function of time, Gathering Steam has the capability of providing game developers an early alert to predicted changes in game ratings. Additionally, topics are extracted from reviews within each timeframe such that the developers can make informed decisions about additional game changes.  

__Skills/Tools:__  
_Python,
Natural Language Processing (NLP), Scikit-learn (sklearn), Natural Language Toolkit (NLTK), Steam API, requests, altair, matplotlib_  


----

#### Details:

First, I utilized Steam's API to gather all reviews for a given game. The reviews were returned as a list of JSON objects. I extracted a number of each features from each review: upvote/downvote, date, text in review, and others. I then had to clean the reviews, removing undesired characters (\n, \t, etc.). NLTK's vaderSentiment package was used to extract the positive and negative sentiments of each review.  

A windowing function was implemented to create a moving average of these sentiments alongside the average game rating (# positive ratings/total ratings) and its rate of change over this time period. Following this, I used a multinomial logistic regression classification model to predict future changes in game ratings. At a cost to the model's precision, I lowered the prediction threshold for large changes in ratings defined by the standard deviation of the game's rating changes over time.  

For predictions of large changes in ratings lasting more than a few points, using TF-IDF and NMF, I extracted topics from recent reviews. These topics are then displayed with each predicted point, along with an example review. Ultimately, this provides game developers potential points to address and has the capability of preventing revenue-impacting drops in ratings if addressed in a timely manner.
