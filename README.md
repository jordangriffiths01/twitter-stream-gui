#Twitter Stream GUI

This application is used to retrieve tweets pertaining to a certain
hashtag or twitter handle, and store them in a Queue. A Tkinter GUI
then allows the user to display a single tweet at a time, taken
from the front of the queue. Further controls allow the user to
manipulate the queue of tweets: removing, re-ordering or adding
fake tweets to the queue as required.

##Dependencies

**python:** version 3.0 or later

**tweepy:** version 3.3 or later


##Repository Contents

**twitter_stream.py** - contains the main body of the code. Invokes an extended
version of the tweepy stream listener class to trigger tweet events.
Implements a tkinter GUI to display tweets.

**example_keys.conf** - Used to demonstrate where to include api keys
(owners keys have been excluded from public domain).

##API Keys

To access the twitter API using oAuth, keys are required.
These are available by registering [here](http://dev.twitter.com).

##Notes On Threading

The Tkinter Library is not thread safe, which may cause issues during
development. It is essential that the Tkinter root is run in the main thread,
so any other threaded processes must be started in a seperate thread.

Python Queues are thread safe, and it is expected that the queue interface
alone will be adequete for data transfer between tweepy thread and tkinter
(main) thread.

#Developer Contact

This repository is currently maintained by [Jordan Griffiths](https://github.com/jordangriffiths01).
