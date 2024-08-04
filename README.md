# Olympics ranking medals

## Pre-requisites

- [vscode](https://code.visualstudio.com/) to edit the code
- [pyenv](https://github.com/pyenv/pyenv)
- [poetry](https://python-poetry.org/)
- [jq](https://stedolan.github.io/jq/) to install vscode extension (it will be useful anyway for all JSON manipulation)
- [make](https://www.gnu.org/software/make/) to run the commands
- [Docker](https://docs.docker.com/get-docker/)
- [git](https://git-scm.com/) to manage the code

## Setup the project

### If you use(d) `conda`

If you have `conda` installed, we recommend to deactivate the `base` environment used by default with `conda config --set auto_activate_base false`. This will avoid to have the `base` environment activated by default when you open a new terminal. You can still activate it with `conda activate base`. This is needed to avoid to mess with `pyenv` which is used in this template to isolate python version.

### Setup

Once the project is created, you can setup it with the following command:

```bash
make setup
```

This command will install everything needed to work on the project.

Once the setup is done, you can activate the virtual environment with the following command:

```bash
source $(poetry env info --path)/bin/activate
```

### VSCode

You can select the interpreter in VSCode with `Ctrl+Shift+P` and select `Python: Select Interpreter`.

If VScode was already opened, you will need to reload the window with `Ctrl+Shift+P` and select `Developer: Reload Window`.

### Poetry virtual environment

The name of the virtual environment could be retrieved with the following command:

```bash
poetry env list
```

More details are provided with command:

```bash
poetry env info
```
