#!/usr/bin/env bash

echo "🛠 Forcing Python 3.10.13 manually"
PYENV_ROOT="$HOME/.pyenv"
export PYENV_ROOT

# Install pyenv and Python 3.10.13
curl https://pyenv.run | bash
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install -s 3.10.13
pyenv global 3.10.13

python --version

# Install requirements
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
