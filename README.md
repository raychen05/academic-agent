
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

export OPENAI_API_KEY="Ew1gWg0"
export OPENAI_API_BASE="https://openai/large-language-models/gpt_4o"

#### Permanent Environment Variable

nano ~/.bashrc  # or ~/.zshrc if you use Zsh
export OPENAI_API_KEY="your-openai-api-key-here"
source ~/.bashrc  # or source ~/.zshrc
