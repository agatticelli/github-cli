deactivate
rmvirtualenv github-cli
mkvirtualenv -p python3 github-cli
pip install -r requirements.txt
pyinstaller --onefile --clean github.py
mv dist/github /usr/local/bin/
rm -r build __pycache__ dist github.spec *.pyc
