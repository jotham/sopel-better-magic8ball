# sopel-better-magic8ball
Better Magic 8-ball script for Sopel IRC bot.

Strips junk words from question then uses basic latin numerology to seed the 8-ball script.

Requires nltk module.

## Basic install of nltk:

    pip install nltk
    python3 -c "import nltk; nltk.download()"
    
    ...

    Downloader> d popular
    Downloader> q
