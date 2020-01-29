# lit-word-bot
This is a bot which finds rare, colorful words in Reddit comments and defines them for readers.

You can see some of its comments here: https://www.reddit.com/user/lit_word_bot

Status: The bot can run all day autonomously, and users seem to by-and-large like the comments it makes. It earned about 250 "upvotes" in the first 8 hours of running. There are some issues with API exceptions (such as making too many comments too quickly) that still need to be handled, but I'm happy with the progress.

This project started as a way for me to learn Python but became quite a bit more substantial as I got into the problem. This is a heavily heuristic-based solution, which I may one day upgrade to be a machine-learned solution.

You will need API keys for Merriam-Webster's API (collegiate dictionary + collegiate thesaurus) from here: https://dictionaryapi.com/
and Reddit API keys from here: https://www.reddit.com/prefs/apps/

Running the bot: once you've supplied the keys, you can run the bot using "pipenv install" then "pipenv run python pipeline.py"
It was written on 3.8 and compatibility with older versions is unknown.
