# https://www.reddit.com/user/lit_word_bot/?sort=top

Warning: ugly code ahead. This project started as a way for me to learn Python but became quite a bit more substantial as I got into the problem. In summary, it's a producer/consumer with some clever heuristics, all of which do a pretty good job collectively.

# lit-word-bot
This is a bot which finds rare, colorful words in Reddit comments and defines them for readers.

It relies on heuristics to make a good guess as to whether or not a word is worth defining. While it's not 100% perfect, readers seem to enjoy the comments. Any given comment can be easily deleted by readers if it's not desired.

Status: The bot can run all day autonomously. Readers seem to by-and-large like the comments it makes. As of writing this, it's earned 1864 "upvotes" in the space of about 2 days. It earns an average of 35 Karma per comment, which beats my personal account's average of 25.


If you'd like to mess around with it, you should:

- Modify the code to eliminate the API calls (.define, obtain(), and reddit_rw), then mess around as such. You're free to do whatever you want.

It was written on Python 3.8 and compatibility with older versions is unknown. You'll need to run "pipenv install" in the directory before it will work. Then, run pipenv run python pipeline.py. Wallah!

If you'd like to contribute or improve something, feel free to contribute!! I will look at your pull request and decide whether or not to include it.
