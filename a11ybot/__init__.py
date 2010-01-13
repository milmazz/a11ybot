#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Retweet messages with especified hashtag search terms to twitter'''

__author__ = 'milmazz@gmail.com'
__version__ = '0.1dev'
__date__ = ''
__copyright__ = 'Copyright (c) 2010 Milton Mazzarri'
__license__ = 'MIT'

import os
import logging
import gettext
import ConfigParser
from optparse import OptionParser

import tweepy

class GetConfig(object):
    """Get options from config file"""
    def __init__(self):
        self._config = None
        self._section = 'a11ybot'

    def get_username(self):
        """Get username option from config file"""
        return self._get_option('username')

    def get_password(self):
        """Get password option from config file"""
        return self._get_option('password')

    def get_language(self):
        """Get language option from config file"""
        return self._get_option('language')

    def get_search_term(self):
        """Get search terms options from config file"""
        try:
            return self._get_option('search').split(" ")
        except AttributeError, error:
            logging.warn(error)
            return None

    def _get_option(self, option):
        """Internal method to get an option from config file"""
        try:
            return self._get_config().get(self._section, option)
        except ConfigParser.NoOptionError, error:
            logging.debug(error)
            return None

    def _get_config(self):
        """Try to read config from file"""
        if not self._config:
            self._config = ConfigParser.SafeConfigParser()
            try:
                self._config.readfp(open(os.path.expanduser('~/.a11ybotrc')))
            except IOError, error:
                logging.warn(error)
        return self._config

#def _retweet(tweet):
#    """Retweet method"""
#    try:
#        api.retweet(tweet.id)
#        logging.info(tweet.text)
#    except tweepy.TweepError:
#        logging.warn(tweet.text)

def main():
    """Main method of the script"""

    # i18n (gettext support)
    gettext_domain = 'a11ybot'
    try:
        localedir = os.environ['BOT_LOCALE_DIR']
    except KeyError:
        localedir = os.path.join('/', 'usr', 'share', 'locale')

    t = gettext.translation(gettext_domain, localedir)
    _ = t.ugettext

    usage = _('%prog [options]')
    description = _('Retweet messages with especified search terms to twitter')
    # help messages
    help_messages = {
        'username': _('Twitter username'),
        'password': _('Twitter password'),
        'search': _('Search term to retweet'),
        'lang': _('Restricts retweets to the given language, given \
                by an \'ISO 639-1\' code (default: %default)'),
        'verbose': _('Explain what is being done (default: %default)'),
        'quiet': _('Suppress what is being done')
    }

    parser = OptionParser(usage=usage, description=description)
    parser.add_option('-u', '--username', dest='username',
            help=help_messages['username'])
    parser.add_option('-p', '--password', dest='password',
            help=help_messages['password'])
    parser.add_option('-s', '--search', dest='search', action='append',
            help=help_messages['search'])
    parser.add_option('-l', '--lang', dest='language', default='en',
            help=help_messages['lang'])
    parser.add_option('-v', '--verbose', action='store_true', 
            dest='verbose', default=True,
            help=help_messages['verbose'])
    parser.add_option('-q', '--quiet', action='store_false',
            dest='verbose', 
            help=help_messages['quiet'])

    (options, args) = parser.parse_args()

    # Basic config for logging messages
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=os.path.expanduser('~/.a11ybot.log'),
                        filemode='w')

    config = GetConfig()

    if options.verbose:
        # INFO messages or higher to sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a much simple format for console use
        formatter = logging.Formatter('[%(levelname)s] - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    username = options.username or config.get_username()
    password = options.password or config.get_password()
    search = options.search or config.get_search_term()
    lang = options.language or config.get_language()

    if not username or not password or not search:
        parser.print_help()
        exit(2)

    auth = tweepy.BasicAuthHandler(username, password)

    api = tweepy.API(auth)

    if len(search) >= 2:
        query = ' OR '.join(search)
    else:
        query = search[0]

    try:
        tweets = tweepy.api.search(q=query, lang=lang)
    except tweepy.TweepError, error:
        logging.error(error)
        exit(2)

#    [_retweet(tweet) for tweet in tweets]
    for tweet in tweets:
        try:
            api.retweet(tweet.id)
            logging.info(tweet.text)
        except tweepy.TweepError, error:
            logging.warn(error)

if __name__ == '__main__':
    main()
