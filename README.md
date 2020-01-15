# lit-word-bot
This is a bot which finds rare, colorful words in Reddit comments and defines them for readers.

You can see some of its comments here: https://www.reddit.com/user/lit_word_bot

Status: MVP completed, currently being refactored to better support full-autonomous functionality. At present, it's a one-shot application.

This project started as a way for me to learn Python but became quite a bit more substantial as I got into the problem. This is a heavily heuristic-based solution, which I may one day upgrade to be a machine-learned solution.

You will need API keys for Merriam-Webster's API (collegiate dictionary + collegiate thesaurus) from here: https://dictionaryapi.com/
and Reddit API keys from here: https://www.reddit.com/prefs/apps/

Running the bot: once you've supplied the keys, you can run the bot using "pipenv install" then "pipenv run python main.py"
It was written on 3.8 and compatibility with older versions is unknown.
