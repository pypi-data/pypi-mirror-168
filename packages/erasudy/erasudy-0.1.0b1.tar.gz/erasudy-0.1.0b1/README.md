# Erasudy

Erase disks data securely.


## Introduction

Erasudy is a tool for erasing disk data securely.


## Development

### Requirements

Use `poetry install` to get the virtual environments with requirements.

# Create a new release

Use Poetry to create a new release.

To update the version from  and   use the following plugin.

```bash
poetry self add poetry-bumpversion
```

Then create the new release with those steps.

```bash
poetry version <version>
poetry build
poetry publish
```
