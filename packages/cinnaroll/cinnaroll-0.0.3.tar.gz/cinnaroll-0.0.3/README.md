# cinnaroll Python library

## PyCharm setup

Make sure the following bundled plugins are enabled:
* Docker
* Git
* Markdown
* Ini
* IntelliLang (for language injections, e.g. Markdown/shell scripts in YAML)
* Shell Script (also: agree to enable Shellcheck when asked)
* YAML

Install the following non-bundled plugins from Marketplace:
* [.ignore](https://plugins.jetbrains.com/plugin/7495--ignore)
* [Requirements](https://plugins.jetbrains.com/plugin/10837-requirements/)


## (Optional) Git hook setup

Install [`shellcheck`](https://github.com/koalaman/shellcheck#installing) and [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

Install npm packages:
```shell
npm install --global remark-cli remark-lint-no-dead-urls remark-validate-links
```

From the top-level folder of the repository, run the following command:
```shell
ln -s ../../ci/checks/run-all-checks.sh .git/hooks/pre-commit
```


## Run tests locally

To develop that project and run tests locally, it is needed to have Python installed with `tox`.

Use `tox -e venv` to setup virtual environment to work on that project in your favorite IDE.
Use `.tox/venv/bin/python` as a reference `python` interpreter in your IDE.

To run tests, execute `tox`.

It's also possible to execute tests graphically in PyCharm (right-clicking on the test file
or clicking the green triangle on the left of the test case name), which can be very useful when debugging a single test case.
To do so, make sure that the libraries from [requirements.testenv.txt](requirements.testenv.txt) are installed in the current venv.


## Versioning

This tool is [semantically versioned](https://semver.org) with respect to all of the following:

* Python version compatibility
* command-line interface (commands and their options)
* format of its specific files (currently just `~/.config/cinnaroll`)
* accepted environment variables


## Release TODO list

Note that we merge code to `main` and use git tags for releases.

To perform a release:

1. Tag the current `main` commit and push the tag:

```shell
git checkout main
git pull origin main
git tag v<VERSION>
git push origin v<VERSION>
```

1. Once the [CI](https://github.com/carthago-cloud/cinnaroll-python-lib/actions) completes,
   verify that the latest pack has been uploaded to [PyPI](https://pypi.org/project/cinnaroll).
