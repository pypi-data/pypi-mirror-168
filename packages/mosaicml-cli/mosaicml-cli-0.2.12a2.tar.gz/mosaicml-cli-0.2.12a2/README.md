# MCLI (MosaicML Command Line Interface)

## Understanding MCLI

MCLI is a command line interface for the Mosaic Cloud.

To understand MCLI use cases, read the [customer-facing docs](https://mcli.docs.mosaicml.com/) and go through installation and tutorials.

There is also documentation specific to [internal use cases](https://internal.mcli.docs.mosaicml.com).

## Development environment setup

### Pre-requisites

**Git**

We’re using git and GitHub for source control. In case your dev box does not have git installed, [this is a good resource on installing git](https://github.com/git-guides/install-git#install-git) (and it has [even more resources](https://github.com/git-guides/) to help get started with git concepts and commands).

**Python**

MCLI is developed with Python3. To install Python, start [here](https://www.python.org/downloads/).

### Setup steps

**Clone repository**

Clone the repo from GitHub and cd into the newly created project dir

```bash
$ git clone git@github.com:mosaicml/mosaicml-cli.git
$ cd mosaicml-cli
```

**Create a virtual environment**

Run this command from the project root:

```bash
$ python -m venv venv
```

Note that the virtual environment files will be stored in a folder named "venv" under the current directory, and this folder is ignored by git via .gitignore

**Activate your new virtual environment**

```bash
$ source venv/bin/activate
```

You will now see your terminal prompt being updated to start with the virtual environment name in parenthesis: "(venv)". This is how you know you are working in an activated virtual environment!

**Update pip to the latest version**

```bash
$ pip install --upgrade pip
```

**Install mcli dependencies (including dev dependencies)**

Here we're using the -e flag to indicate this module is "editable", meaning changes to the source directory will immediately affect the installed package without requiring to re-install.

```bash
$ pip install -e ".[all]"
```

**Give `mcli` a quick test**

Check you have local mcli installed by running the commend below, and ensuring you get the same version as in the file [`mcli/version.py`](https://github.com/mosaicml/mosaicml-cli/blob/dev/mcli/version.py)

```bash
$ mcli version
```

**Run `mcli` tests**

Run tests to make sure setup in in order. All tests should either pass or configured to be ignored.

```bash
# Runs all unit tests
$ pytest

# Runs all integration tests
$ pytest --integration

# Runs all end-to-end tests
$ pytest --e2e
```

**Note on running end-to-end tests**
In its current state, you'll need to have the following services running locally:

- [MAPI](https://github.com/mosaicml/MAPI) (gql, db, localstack)
- [MORC](https://github.com/mosaicml/MORC) (db, orch, worker)

It may be helpful for debugging failures to also have database connections open for both services and an additional terminal for kubectl commands.
Note that you _do not_ need to edit anything in your local config - the tests will handle this for you

**Running MCLI against MAPI locally**
You'll need to set the following environment variables:

- MOSAICML_API_ENDPOINT=http://localhost:3001/graphql
- MOSAICML_API_KEY_ENV=test.mosaicml-secret-testing-api-key
- MCLI_MODE_ENV=DEV

And turn on the MAPI feature flag (`mcli use feature` -> `USE_FEATUREDB`).
Before submitting CLI or SDK commands, make sure [MAPI](https://github.com/mosaicml/MAPI) (gql, db, localstack) is running locally

**And… you are done!**

A few notes for later on:

- To exit the virtual environment later on: `$ deactivate`
- To get back into your virtual environment: `$ source venv/bin/activate`
