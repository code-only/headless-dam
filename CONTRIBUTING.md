# Contributing Guide

Thank you for considering contributing!

## How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b fix/some-issue`)
3. Write your code, add tests if applicable
4. Run the test suite (`pytest`)
5. Lint your code (`flake8` and `black .`)
6. Commit and push
7. Submit a pull request (PR)

## Coding Guidelines

- Use `black` for formatting, `flake8` for linting, and `isort` for imports
- All new functionality requires tests
- PRs should reference an issue, or describe the motivation clearly

## Local Setup

- Clone this repo
- Create and activate a virtualenv
- Install requirements: `pip install -r requirements.txt`
- Copy `.env.example` to `.env` and fill in required variables
- Run `uvicorn main:app --reload`

## Getting Help

Open an issue or start a discussion using GitHub Discussions!

---

