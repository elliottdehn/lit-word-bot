# lit-word-bot
This is a bot which finds rare, colorful words in Reddit comments and defines them for readers.

You can see some of its comments here: https://www.reddit.com/user/lit_word_bot

Status: The bot can (nearly) run all day autonomously. Readers seem to by-and-large like the comments it makes. It earned about 250 "upvotes" in the first 8 hours of running.

This project started as a way for me to learn Python but became quite a bit more substantial as I got into the problem. This is a heavily heuristic-based solution, which I may one day upgrade to be a machine-learned solution.

If you'd like to mess around with it, you have a few options:

- Get some API keys for Merriam-Webster's API (collegiate dictionary + collegiate thesaurus) from here: https://dictionaryapi.com/ and/our Reddit API keys from here: https://www.reddit.com/prefs/apps/. Add them to secrets-template.py and rename it to secrets.py. Adjust the code as-appropriate and mess around.

- Modify the code to eliminate the API calls and mess around as such. You're free to do whatever you want.

Running the bot: once you've supplied the keys, you can run the bot using "pipenv install" then "pipenv run python pipeline.py"
It was written on 3.8 and compatibility with older versions is unknown.
