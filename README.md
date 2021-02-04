# twinsie
Measure the similarity between two text strings


[![Python](https://img.shields.io/badge/python-3.5%2C%203.6--dev-blue.svg)]()
[![Requirements](https://requires.io/github/stuck3y/requirements.svg?branch=main)](https://requires.io/github/stuck3y/twinsie/requirements/?branch=main)
[![Docker](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000)]()

# twinsie!

Minimal API that measures similarity between two pieces of text producing a score from 0 to 1.

The overall score ranges from 0 (not similar at all) to 1 (perfectly
similar, or exactly the same). Twinsie uses three methods to determine
this score. First, it looks at common words in comparison to all of the words.
This is similar to the Jaccard distance calculation. This is the most basic 
of the three methods and can be a poor similarity method on its own. 
    
To mitigate that, and add more precision, method two attempts to take all 
of the uncommon words between the two strings and see if we can fuzzy match 
them against each other. Any fuzzy matches are accounted for and factored 
into the overall score. 
    
Lastly, we look at the order of the words to add even more precision to the 
final score. We take all of the common words and evaluate their position in
one text string in relation to its position in the other text string. If it
exist within the bounds of a pre-defined window, we consider that a "match"
and that is factored into the final score.



## Getting started

Install [docker](https://docs.docker.com/engine/installation/) and run:

```shell
docker-compose up --build
# docker-compose stop
```

Otherwise, for the standalone web service:

```shell
pip install -r requirements.txt
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) to see the Home Page.

There you will see instructions to send a POST request containing your two strings in the body of a JSON blob to the `/twinsie` endpoint. You will want to label them *text1* and *text2*.

`http://localhost:5000/twinsie`


## Development

Create a new branch off the **develop** branch for features or fixes.

After making changes rebuild images and run the app:

```shell
docker-compose build
docker-compose run -p 5000:5000 web python app.py
