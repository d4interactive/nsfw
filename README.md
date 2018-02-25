### NSFW Analyzer

A Python based profanity checker based on the following rules:


- [x] Using textual information/bag of words.

- [x] Using bloomfilter for the adult related domains to skip them.

- [ ] Using pre-trained data for the images to recognize adult content 
from the images.

#### Usage

There are two use cases NSFW solves.

1. By checking the title of the web page, by using the bag of words.

```
from nsfw.nude import ProfanityChecker
score = ProfanityCheck.score('She is so sexy that he did not long last')
print(score)
```

2. Using the bloom filter or checking the restricted words in the domain 
url.

```
from nsfw.nude import ProfanityChecker
result = ProfanityCheck.domain('zbiornik.com')
```