# Synthetic challenge

## Installation for Task №1 (TodoList)
1. Clone repository:
```
git clone https://github.com/Dima12334/synthetic.git
```
2. Create python virtual environment:
```
python3 -m venv <venv_name>
source <venv_name>/bin/activate
```
3. Install project dependencies:
```
pip install -r requirements.txt
```
4. Configure db using Flask shell. First you need to go to the task1 directory:
```
/synthetic$ cd task1
```
then run Flask shell
```
synthetic/task1$ flask --app todo_list shell
```
and then run these commands in shell:
```
>>> from todo_list import db
>>> db.create_all()
>>> exit()
```
5. Run todo_list.py file:
6. Done. Use the App.

## Installation for Task №2 (HTML validator)
1. Just fill out the example.html file as you wish (or leave it as is) and run html_validator.py :)
