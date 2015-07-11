import tweepy
import json
from tkinter import *
from tkinter.ttk import *
from queue import Queue
import threading
import configparser
import sys

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
        self.cur_tweet = StringVar()
        self.cur_tweet_lbl = Label(window, textvariable=self.cur_tweet)
        self.cur_tweet_lbl.pack()
        self.quit_button = Button(window, text="Quit", command=self.quit).pack(side=LEFT)
        self.new_button = Button(window, text='next', command=self.update_tweet)
        self.new_button.pack(side=LEFT)
        self.scroll()

    def scroll(self):
        if not self.tweet_q.empty():
            current = self.cur_tweet.get()
            next_tweet = self.tweet_q.get()
            self.cur_tweet.set(next_tweet)
            if current:
                self.tweet_q.put(current)
        if self.tweet_q.qsize() < 8:
            self.window.after(5000, self.scroll)


    def update_tweet(self, *args):
        if not self.tweet_q.empty():
            self.current_tweet.set(self.tweet_q.get())

    def quit(self):
        self.window.destroy()

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
    t1.setDaemon(True)
    gui.stream_thread = t1
    t1.start()
    window.mainloop()
