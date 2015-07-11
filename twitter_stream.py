import tweepy
import json
from tkinter import *
from tkinter.ttk import *
from queue import Queue
import threading
import configparser


KEYS_LOCATION = 'keys.conf' #location of keys config file

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui

    def on_data(self, data):
        # Twitter returns data in JSON format
        decoded = json.loads(data)
        #self.gui.event_generate('<<test>>', when='tail')
        #convert UTF-8 to ASCII
        tweet_text = '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        self.gui.tweet_q.put(tweet_text)
        print(tweet_text)
        return True

    def on_error(self, status):
        print(status)

class TwitterGui:
    def __init__(self, window, tweet_q):
        self.tweet_q = tweet_q
        self.window = window
        self.newest = StringVar()
        self.newest_label = Label(window, textvariable=self.newest)
        self.newest_label.pack()
        self.new_button = Button(window, text='next', command=self.update_newest)
        self.new_button.pack()


    def update_newest(self, *args):
        if not self.tweet_q.empty():
            self.newest.set(self.tweet_q.get())


def read_conf(settings_location):
    """Read the given setting file
    and return the configparser
    """
    settings = configparser.ConfigParser()
    settings.optionxform = str
    settings.read(settings_location)
    return settings


def init_stream(gui):
    print('INITIALISING STREAMING')
    listener = StdOutListener(gui)
    keys = read_conf(KEYS_LOCATION)['MAIN']
    print(keys)
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=['programming'])


if __name__ == '__main__':
    window = Tk()
    tweet_q = Queue()
    gui = TwitterGui(window, tweet_q)
    t1 = threading.Thread(target=init_stream, args=(gui,))
    t1.start()
    window.mainloop()
