# sopel-better-magic8ball
Better Magic 8-ball script for Sopel IRC bot.

Strips junk words from the question then uses basic latin numerology to seed the 8-ball script.

Requires nltk module.

## Basic install of nltk:

    pip install nltk
    python3 -c "import nltk; nltk.download('popular')"


## Basic configuration of module

Assuming the following directory structure:
```
sopel-config
|
+-- modules
|
+-- repositories
     +-- sopel-better-magic8ball
         +-- .git (this repository)
         |-- better-magic8ball.py
         |-- better-magic8ball.prophecies.json
         \-- README.md (this file)
```

The module assumes a file called ```better-magic8ball.prophecies.json``` in the same
folder as the module *.py file.

The following needs to be done, assuming it is done from the modules folder:

```bash
cd sopel-config/modules

ln -s ../repositories/sopel-better-magic8ball/better-magic8ball.py better-magic8ball.py
ln -s ../repositories/sopel-better-magic8ball/better-magic8ball.prophecies.json better-magic8ball.prophecies.json
```
