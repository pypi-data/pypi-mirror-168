## Setup

```sh
pipx install tox
pipx inject tox tox-pyenv
tox
```

## Compiling a new requirements.txt

Modify setup.py with new requirements and then run:
```sh
tox -e build_reqs
```

## Uploading

```sh
tox -e build
tox -e upload
```

Or alternatively, let the pipeline handle it by releasing a versioned tag.
