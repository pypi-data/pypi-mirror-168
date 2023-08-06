# use pipenv-setup to generate the requirement list
# https://pypi.org/project/pipenv-setup/

from setuptools import setup
from gitlab2pandas import __version__


with open("README.md", "r") as f:
   long_description = f.read()



setup(
   name="gitlab2pandas",
   version=__version__,
   packages=["gitlab2pandas"],
   license="BSD 2",
   description="gitlab2pandas supports the aggregation of project activities in a GitLab repository and makes them available in pandas dataframes.",
   long_description = long_description,
   long_description_content_type="text/markdown",
   author="Maximilian Karl",
   url="https://gitlab.com/gitlab-learning-analytics/gitlab2pandas",
   download_url="https://gitlab.com/gitlab-learning-analytics/gitlab2pandas/-/archive/main/gitlab2pandas-main.zip",
   keywords=["git", "gitlab", "collaborative code development", "git mining"],
   install_requires=[
      "human-id>=0.2.0",
      "pandas>=1.4.4",
      "python-gitlab>=3.9.0",
      "XlsxWriter>=3.0.3"
   ], 
   classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
   ],
   python_requires=">=3.9"
)
