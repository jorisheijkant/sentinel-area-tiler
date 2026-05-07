# Project Context

When working with this codebase, prioritize readability and clean code over cleverness. Ask clarifying questions before making architectural changes.

## About This Project

This project fetches and tiles satellite imagery through the Sentinel API. 

## Key Directories

- `data/` - where the tiles are output (not committed)
- `.env` - where the API keys/login live (not committed)
- `functions/` - where most functionality is written
- `fetch_area.py` - the main script

## MCP servers

Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask. 

## Standards

My coding standard is heavily focused on clean, modular code. Avoid long files and put explanations in READMEs rather then in the code itself. I prefer provider agnostic code, where functionality is implemented in a way that there is an abstraction layer on top which allows you to switch providers easily when it comes to things such as databases, deployment etc. 

### Naming variables and functions

- Use descriptive and meaningful names 
- For variables and properties: Nouns or short phrases with adjectives
- For functions and methods: verbs short phrases with adjectives
- For classes: nouns
- For booleans: yes/no questions (like isValid) 

### General clean code principles

- Limit the number of parameters in functions
- Functions should be small and do one thing. Avoid mixing levels of abstraction, but also avoid redundant splitting
- Use small classes with a single responsibility and with high cohesion
- Stay DRY: do not repeat yourself. Put functionality in different files and load them in different parts of the code if needed
- Avoid unexpected side effects
- Prefer positive checks
- Avoid deep nesting. Use the law of Demeter for "real objects" 
- Use the SOLID principles, especially SRP and OCP. 

### Folder and file structure

- When using python, place functions in a functions/ folder and if needed, subfolders for functions in a common category.
- When using python, place common variables in a .env file (and always a .env.example equivalent) and use python-dotenv
- When using javascript, place functions in separate js files if it makes files less readable otherwise
- When using javascript frameworks, stick to component structures but avoid long functions in component files (put these in separate js files)

### Comments

- Avoid comments as much as possible, use clear variable naming and clean code instead
- If more elaborate explanation feels necessary, create a README file or add some explanation there
- Comments are acceptable for legal stuff, warnings, helpful explanations (i.e. with regex) or todo's

