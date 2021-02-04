[![Python](https://img.shields.io/badge/python-3.5%2C%203.6--dev-blue.svg)]()
[![Docker](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000)]()

# twinsie!

A minimal service that measures similarity between two pieces of text producing a score from 0 to 1.

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


### Sample Payload

```
{
    "text1": "I love going to Five Guys Burgers and Fries for lunch",
    "text2": "I think I might go to Five Guys to eat lunch today to celebrate the launch."
}
```
Response:
```
text1: I love going to Five Guys Burgers and Fries for lunch

text2: I think I might go to Five Guys to eat lunch today to celebrate the launch.

sim_score = 0.4805263157894737

########
```


### Sample Call from Command Line with `cURL`

```shell
curl --data '{"text1": "I love going to Five Guys Burgers and Fries for lunch", "text2": "I think I might go to Five Guys to eat lunch today to celebrate the launch."}' http://localhost:5000/twinsie --header 'Content-Type: application/json' --header 'Accept: application/json'
```

Response:
```
text1: I love going to Five Guys Burgers and Fries for lunch

text2: I think I might go to Five Guys to eat lunch today to celebrate the launch.

sim_score = 0.4805263157894737

########
```

### Sample call from [Postman](https://www.postman.com/downloads/)
![](postman_sample.png)



## Development

Create a new branch off the **development** branch for features or fixes.

After making changes rebuild images and run the app:

```shell
docker-compose build
docker-compose run -p 5000:5000 web python app.py
