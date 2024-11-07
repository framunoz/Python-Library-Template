# Basic ```poetry``` usage

This short tutorial is a summary of the official ``poetry`` 
documentation. For more information, see the 
[official documentation](https://python-poetry.org/docs/basic-usage/).

## Adding a dependency

When you want to add a new dependency to the project, you can run the
following command:

```bash
poetry add <DEPENDENCY>
```

Where `<DEPENDENCY>` is the name of the dependency you want to add.

In case you want to add a development dependency, you can run the following

```bash
poetry add --dev <DEPENDENCY>
```

## Installing dependencies

To install the dependencies of the project, you can run the following command:

```bash
poetry install
```

## Activating the virtual environment

To activate the virtual environment, you can run the following command:

```bash
poetry shell
```

## Running a script

To run a script, you can use the following command:

```bash
poetry run <SCRIPT>
```

Where `<SCRIPT>` is the name of the script you want to run.
