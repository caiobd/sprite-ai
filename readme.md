# Sprite AI


## Description
Sprite AI is an AI companion for your desktop, through LLM technology a sprite can generate text, dialog and even computer code,


## Minimum requirements

Description |  Value
------------|------------------------------
OS          |   MacOS, Linux [Tested only on Linux]
CPU         |   Any
GPU         |   Any [Optionall]
RAM         |   >= 8GB
Storage     |   6GB


## Dependencies
- [Python](https://www.python.org/) >= 3.8
- [Rofi](https://github.com/davatorium/rofi)
- pipx [Optional]


## Installation
1. [Install Python](https://wiki.python.org/moin/BeginnersGuide/Download) >= 3.8
1. [Install Rofi](https://github.com/davatorium/rofi/blob/next/INSTALL.md)
1. [Install pipx](https://pypa.github.io/pipx/#install-pipx) [Optional dependency]
1. Install Sprite AI  
    a. Use pip [default]
    > pip install --user sprite-ai

    b. Use pipx [altenative]
    > pipx install sprite-ai


## Usage

### Starting Sprite AI
In a terminal type the following command
> sprite-ai

### Interacting with the sprite
You can interact with a sprite by clicking on it, this will open the interaction menu

### Interaction menu
In this menu you can either select a command to execute it or a previous message from chat to copy the message to your clipboard

#### Available commands

Command     | Description
------------|-----------------------------------------------------------------
new message | Opens a textbox that allows you to send a message to the sprite
exit        | Closes Sprite AI
