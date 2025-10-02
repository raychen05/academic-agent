
### Setup Environment

#### activate the local pipenv

cd /path/to/your/project
export PIPENV_IGNORE_VIRTUALENVS=1
export PIPENV_VENV_IN_PROJECT=1

pipenv --rm  # remove old env

pipenv install
pipenv run pip install -r requirements.txt

pipenv --venv  # should now be in ./venv

pipenv shell
exit

streamlit run app.py

url="https://agai-platform-api.dev.int.proquest.com/large-language-models/gpt_4o"

export OPENAI_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiV29TIFJlc2VhcmNoIEludGVsbGlnZW5jZSIsImJ1c2luZXNzX2lkIjoxLCJpc3N1ZWRfZGF0ZSI6IjA0LzI0LzIwMjQsIDE0OjU2OjU2In0.djZ8Lukkkl-Do4weZdKPXK6UuwR7JDmieo9bEw1gWg0"
export OPENAI_API_BASE="https://agai-platform-api.dev.int.proquest.com/large-language-models/gpt_4o"

#### Permanent Environment Variable

nano ~/.bashrc  # or ~/.zshrc if you use Zsh
export OPENAI_API_KEY="your-openai-api-key-here"
source ~/.bashrc  # or source ~/.zshrc