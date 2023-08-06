# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crescent',
 'crescent.commands',
 'crescent.context',
 'crescent.ext.cooldowns',
 'crescent.ext.tasks',
 'crescent.internal',
 'crescent.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.0.0',
 'croniter>=1.3.5,<2.0.0',
 'hikari>=2.0.0.dev110',
 'pycooldown>=0.1.0-beta.8',
 'sigparse>=1.3.0,<2.0.0',
 'types-croniter>=1.0.10,<2.0.0']

setup_kwargs = {
    'name': 'hikari-crescent',
    'version': '0.3.3',
    'description': '🌕 A command handler for Hikari that keeps your project neat and tidy.',
    'long_description': '# hikari-crescent\n\n<div align="center">\n\n![code-style-black](https://img.shields.io/badge/code%20style-black-black)\n![mypy](https://badgen.net/badge/mypy/checked/2A6DB2)\n![pyright](https://badgen.net/badge/pyright/checked/2A6DB2)\n[![ci](https://github.com/magpie-dev/hikari-crescent/actions/workflows/ci.yml/badge.svg)](https://github.com/magpie-dev/hikari-crescent/actions/workflows/ci.yml)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/magpie-dev/hikari-crescent/main.svg)](https://results.pre-commit.ci/latest/github/magpie-dev/hikari-crescent/main)\n![Pypi](https://img.shields.io/pypi/v/hikari-crescent)\n\n </div>\n\n🌕 A command handler for [Hikari](https://github.com/hikari-py/hikari) that keeps your project neat and tidy.\n\n## Features\n - Simple and intuitive API.\n - Slash, user, and message commands.\n - Error handling for commands, events, and autocomplete.\n - Hooks to run function before or after a command (or any command from a group!)\n - Plugin system to easily split bot into different modules.\n - Easily use a custom context class.\n - Makes typehinting easy.\n\n### Links\n> 📝 | [Docs](https://magpie-dev.github.io/hikari-crescent/crescent.html)<br>\n> 📦 | [Pypi](https://pypi.org/project/hikari-crescent/)\n\n## Installation\nCrescent is supported in python3.8+.\n```\npip install hikari-crescent\n```\n\n## Bots using Crescent\n\n- [mCodingBot](https://github.com/mcb-dev/mCodingBot) - The bot for the mCoding Discord server.\n- [Starboard 3](https://github.com/circuitsacul/starboard-3) - A starbord bot by [@CircuitSacul](https://github.com/CircuitSacul)\nin over 17k servers.\n\n\n## Usage\nCrescent uses [class commands](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/basic/basic.py)\nto simplify creating commands. Class commands allow you to create a command similar to how you declare a\ndataclass. The option function takes a type followed by the description, then optional information.\n\n```python\nimport crescent\n\nbot = crescent.Bot("YOUR_TOKEN")\n\n# Include the command in your bot - don\'t forget this\n@bot.include\n# Create a slash command\n@crescent.command(name="say")\nclass Say:\n    word = crescent.option(str, "The word to say")\n\n    async def callback(self, ctx: crescent.Context) -> None:\n        await ctx.respond(self.word)\n\nbot.start()\n```\n\nSimple commands can use functions instead of classes. It is recommended to use a function when your\ncommand does not have any options.\n\n```python\n@bot.include\n@crescent.command\nasync def ping(ctx: crescent.Context):\n    await ctx.respond("Pong!")\n```\n\nAdding arguments to the function adds more options. Information for arguments can be provided using the `Annotated` type hint.\nSee [this example](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/basic/function_commands.py) for more information.\n\n```python\n# python 3.9 +\nfrom typing import Annotated as Atd\n\n# python 3.8\nfrom typing_extensions import Annotated as Atd\n\n@bot.include\n@crescent.command\nasync def say(ctx: crescent.Context, word: str):\n    await ctx.respond(word)\n\n# The same command but with a description for `word`\n@bot.include\n@crescent.command\nasync def say(ctx: crescent.Context, word: Atd[str, "The word to say"]) -> None:\n    await ctx.respond(word)\n```\n\n\n### Typing to Option Types Lookup Table \n| Type | Option Type |\n|---|---|\n| `str` | Text |\n| `int` | Integer |\n| `bool` | Boolean |\n| `float` | Number |\n| `hikari.User` | User |\n| `hikari.Role` | Role |\n| `crescent.Mentionable` | Role or User |\n| Any Hikari channel type. | Channel. The options will be the channel type and its subclasses. |\n| `List[Channel Types]` (classes only) | Channel. ^ |\n| `Union[Channel Types]` (functions only) | Channel. ^ |\n| `hikari.Attachment` | Attachment |\n\n\n### Error Handling\nErrors that are raised by a command can be handled by `crescent.catch_command`.\n\n```python\nclass MyError(Exception):\n    ...\n\n@bot.include\n@crescent.catch_command(MyError)\nasync def on_err(exc: MyError, ctx: crescent.Context) -> None:\n    await ctx.respond("An error occurred while running the command.")\n\n@bot.include\n@crescent.command\nasync def my_command(ctx: crescent.Context):\n    raise MyError()\n```\n\n### Events\n```python\nimport hikari\n\n@bot.include\n@crescent.event\nasync def on_message_create(event: hikari.MessageCreateEvent):\n    if event.message.author.is_bot:\n        return\n    await event.message.respond("Hello!")\n```\nUsing crescent\'s event decorator lets you use\ncrescent\'s [event error handling system](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/error_handling/basic.py#L27).\n\n# Extensions\nCrescent has 2 builtin extensions.\n\n- [crescent-ext-cooldowns](https://github.com/magpie-dev/hikari-crescent/tree/main/examples/ext/cooldowns) - Allows you to add sliding window rate limits to your commands.\n- [crescent-ext-tasks](https://github.com/magpie-dev/hikari-crescent/tree/main/examples/ext/tasks) - Schedules background tasks using loops or cronjobs.\n\nThese extensions can be installed with pip.\n\n- [crescent-ext-docstrings](https://github.com/Lunarmagpie/crescent-ext-docstrings) - Lets you use docstrings to write descriptions for commands and options.\n- [crescent-ext-kebabify](https://github.com/Lunarmagpie/crescent-ext-kebabify) - Turns your command names into kebabs!\n\n# Support\nYou can ask questions in the `#crescent` channel in the [Hikari Discord server](https://discord.gg/Jx4cNGG).\nYou can also message me. My Discord username is `Lunarmagpie❤#0001`.\n\n# Contributing\nCreate an issue for your feature. There aren\'t any guidelines right now so just don\'t be rude.\n',
    'author': 'Lunarmagpie',
    'author_email': 'bambolambo0@gmail.com',
    'maintainer': 'Lunarmagpie',
    'maintainer_email': 'bambolambo0@gmail.com',
    'url': 'https://github.com/magpie-dev/hikari-crescent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
