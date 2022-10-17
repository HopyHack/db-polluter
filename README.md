# Instalation

You could use [Pipenv](https://pipenv.pypa.io/en/latest/install/) to install dependencies.

Install python dependencies:

```
pipenv install
```

Pipenv will create a virtual env.

Activate the virtual env

```
pipenv shell
```

# How to run

Run the project like this

```
python main.py -file forms_datas.json
```

or with the `--burp` flag to analyse the requests send by the script

```
python main.py -file forms_datas.json --burp
```
