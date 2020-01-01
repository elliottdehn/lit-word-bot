# lit-word-bot
This is a bot which finds rare, colorful words in Reddit comments and defines them for readers.

Once the bot is up-and-running, you can see its comments here: https://www.reddit.com/user/lit_word_bot

Status: not done yet. You are able to clone the repository, supply API keys in secrets.py, and run the script. It will scan Reddit comments and print out the words it thinks are likely rare. Then, it will perform some basic algorithms using the Merriam-Webster API to determine whether or not the words are actually rare. Afterward, you'll have an opportunity to pick a word in order to automatically generate a comment.

You will need API keys for Merriam-Webster's API (collegiate dictionary + collegiate thesaurus) from here: https://dictionaryapi.com/
and Reddit API keys from here: https://www.reddit.com/prefs/apps/

Note that you can run the bot up until the point where it polls the Merriam Webster API. If you do this, you'll be able to see the comments it picks as "candidates" (after supplying Reddit credentials of course)

Running the bot: once you've supplied the keys, you can run the bot using "pipenv install" then "pipenv run python main.py"
It was written on 3.8 and compatibility with older versions is unknown.
