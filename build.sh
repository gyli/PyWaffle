pyenv install -s 3.10.2
virtualenv -p ~/.pyenv/versions/3.10.2/bin/python --clear --always-copy venv

source venv/bin/activate
pip3 install -r requirements_dev.txt

python3 -m examples.generate_plots

#build docs
#cd docs
#python -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html

deactivate

