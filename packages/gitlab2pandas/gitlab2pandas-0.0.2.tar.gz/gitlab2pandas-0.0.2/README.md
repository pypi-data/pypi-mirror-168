# Transform GitLab Activities to Pandas Dataframes

## General information

This package is being developed as part of the DiP-iT project [Website](http://dip-it.ovgu.de/).

The package implements Python functions for 
+ aggregating and processing GitLab activities (Commits, Actions, Issues, Merge-Requests, ...)

`gitlab2pandas` stores the collected information in a collection of pandas DataFrames starting from a user defined root folder.

## Installation

`gitlab2pandas` is available on [pypi](https://pypi.org/project/gitlab2pandas/). Use pip to install the package.

### global

On Linux:

```
sudo pip3 install gitlab2pandas 
sudo pip install gitlab2pandas
```

On Windows as admin or for one user:

```
pip install gitlab2pandas
pip install --user gitlab2pandas 
```

### in virtual environment:

```
pipenv install gitlab2pandas
```

## Usage  

GitLab token is required for use, which is used for authentication. The [website](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) describes how you can generate this for your GitLab account. Customise the username and project name and explore any public or private repository you have access to with your account!

## Documentation

The documentation of the module is available at [https://gitlab2pandas.readthedocs.io/](https://gitlab2pandas.readthedocs.io/).