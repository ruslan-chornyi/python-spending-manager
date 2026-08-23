# Python Spending Manager

A personal expense tracker with two interfaces: a command-line tool and a Telegram bot, built with pure Python and OOP principles.

## Features

- Add expenses with name, price, and category
- View all recorded expenses
- Calculate total spending
- Filter expenses by category
- Telegram bot with multi-step conversation flow (FSM) for adding expenses

## Tech Stack

- Python 3.13
- aiogram (async Telegram bot framework)
- python-dotenv (environment variables management)

## Project structure

## How to run

### CLI version

```bash
git clone https://github.com/ruslan-chornyi/python-spending-manager.git
cd python-spending-manager
python main.py
```

### Telegram bot

1. Create a bot via [@BotFather](https://t.me/BotFather) and get a token.
2. Create a `.env` file in the project root:
3. Install dependencies:
```bash
pip install aiogram python-dotenv
```
4. Run the bot:
```bash
python bot.py
```

## What I learned

Building this project helped me practice OOP (classes, magic methods), file I/O, exception handling, code organization across modules, Git workflow, type hints, and asynchronous programming with `asyncio`/`aiogram`, including finite state machines for multi-step conversations.

## Possible improvements

- Add unit tests
- Store data in a database (PostgreSQL) instead of a plain text file
- Add inline keyboard buttons instead of text commands
- Deploy the bot to a VPS for 24/7 availability