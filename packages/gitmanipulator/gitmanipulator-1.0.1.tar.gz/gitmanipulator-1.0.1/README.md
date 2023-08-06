# manipulate many git project

## Project management

First, let's start to add some project to manage.

```shell
gitmanipulator project add ./project1 project2
gitmanipulator project list
```

If this project doesn't have a package.json, set version manually.

```shell
gitmanipulator project update 1 --version 1.2.3
```

### create a release

This feature work only for bitbucket. It will stash all your work, update the version, create a release branch, push it,
and open the browser to create a PullRequest

```shell
gitmanipulator project release
```

## Development memory

### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```