# CLI Spending Manager

A simple command-line tool for tracking personal expenses, built with pure Python.

## Features

- Add expenses with category and amount
- View all recorded expenses
- Calculate total spending
- Filter expenses by category

## Tech Stack

- Python 3.13
- No external dependencies (standard library only)

## How to run

```bash
git clone https://github.com/ruslan-chornyi/python-spending-manager.git
cd python-spending-manager
python main.py
```

## What I learned

This was my first standalone Python project, built without following a step-by-step guide. 
Key concepts practiced: file I/O, exception handling, functions, and basic code organization (DRY principle via `load_expenses()`).

## Possible improvements

- Add unit tests
- Store data in JSON instead of plain text
- Add input validation for negative amounts
