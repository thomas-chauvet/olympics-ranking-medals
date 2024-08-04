# Install

Here are detailed install instruction.

Refer to [README.md](README.md) for a quick install with `make` commands.

## IDE configuration

We recommend to use [`VScode`](https://code.visualstudio.com/) as IDE.

We provide some configuration to help you to start. These configuration are located in [`.vscode`](./.vscode) directory.

### Extensions

We recommend some extensions to install in VScode. You can find them in [`.vscode/extensions.json`](./.vscode/extensions.json).

You can install them with the following command:

```bash
cat .vscode/extensions.json | jq -r '.recommendations[]' | xargs -L1 code --install-extension
```

*Note: install [`jq`](https://stedolan.github.io/jq/) to run the command.*

### Settings

We recommend some settings to add in VScode. You can find them in [`.vscode/settings.json`](./.vscode/settings.json).

For instance, we force the use of `ruff` to format and lint the code. We also force the usage of `numpy` docstring style. Some other configuration are also set.

## Python installation

We use [`pyenv`](https://github.com/pyenv/pyenv) to manage python versions. It is a simple and efficient tool to manage python versions. It allows to install several versions of python and to switch between them easily. It doesn't rely on the system python and doesn't require admin rights.

In combination of `pyenv` we use [poetry](https://python-poetry.org/) to manage python dependencies. Poetry is a simple and efficient tool to manage python dependencies. It allows to install dependencies in a virtual environment and to manage them easily.

### Pre-requisites

- [`pyenv`](https://github.com/pyenv/pyenv)
- python (with pyenv)
- [poetry](https://python-poetry.org/)

Additionally, we use [`pre-commit`](https://pre-commit.com/) to run checks on files before committing them.

We also use [`docker`](https://www.docker.com/) to run the application in a container.

Finally, to simplify process we use [`make`](https://www.gnu.org/software/make/) to run commands.

#### Install pyenv

Install pyenv with the following command:

```bash
curl https://pyenv.run | bash
```

Then, setup your shell following [pyenv instructions](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv).

For instance, for zsh:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

#### Install python with `pyenv`

Install python with the following command:

```bash
pyenv install 3.12
```

Use the python installed version for the project:

```bash
pyenv local 3.12  # Activate Python 3.12 for the current project
```

Python version is defined in `.python-version` file. You can directly use the version from the file with:

```bash
pyenv install $(cat .python-version)
```

#### Install poetry

Install poetry with the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then add the following lines to your `.bashrc` or `.zshrc`:

```bash
export PATH="$HOME/.poetry/bin:$PATH"
```

### Install dependencies

To allow poetry to use local pyenv, you need to run the following command:

```bash
poetry config virtualenvs.prefer-active-python true
```

Install dependencies with the following command:

```bash
poetry install
```

It will create a poetry virtual environment. You can list such environment with `poetry env list`.
If you want to remove it, you can run `poetry env remove <env-name>`.

### Pre-commit

Install pre-commit with the following command:

```bash
poetry run pre-commit install
```

If you want to run pre-commit on all files, run the following command:

```bash
poetry run pre-commit run --all-files
```

## Config

We use [`dynaconf`](http://dynaconf.com) to handle configuration in `config/` directory.

## Testing

We use [`pytest`](https://docs.pytest.org/) to write and run tests.

To facilitate development, the template provides two directory in the [`tests`](./tests) directory:

- [`unit`](./tests/unit) for unit tests
- [`integration`](./tests/integration) for integration tests

*Note: integration tests may be not necessary but if could be useful for end-to-end testing or for tests requiring "live" data.*
