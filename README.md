# lit-word-bot
This is a bot which finds rare, colorful words in Reddit comments and defines them for readers.

You can see some of its comments here: https://www.reddit.com/user/lit_word_bot

Status: The bot can (nearly) run all day autonomously. Readers seem to by-and-large like the comments it makes. It earned about 250 "upvotes" in its first 8 hours of running.

This project started as a way for me to learn Python but became quite a bit more substantial as I got into the problem. This is a heavily heuristic-based solution, which I may one day upgrade to be a machine-learned solution.

If you'd like to mess around with it, you should:

- Modify the code to eliminate the API calls (.define, obtain(), and reddit_rw), then mess around as such. You're free to do whatever you want.

It was written on Python 3.8 and compatibility with older versions is unknown. You'll need to run "pipenv install" in the directory before it will work. Then, run pipenv run python pipeline.py. Wallah!

If you'd like to contribute or improve something, feel free to contribute!! I will look at your pull request and decide whether or not to include it.
