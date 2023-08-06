Generate text-centric icons for your Mac OS X dock.

Examples:

![Edge icon](https://github.com/pamelafox/dock-icons/raw/main//examples/edge.png?raw)

![VS Code icon](https://github.com/pamelafox/dock-icons/raw/main//examples/vscode.png?raw)

![Teams icon](https://github.com/pamelafox/dock-icons/raw/main//examples/teams.png?raw)

## Usage instructions

```
pip install icon-writer
```

```
from icon_writer import write_icon

image = write_icon("VSCODE", bgcolor=(0, 102, 185), fontcolor="white")
image.save("icon.png")
```

The function signature for `write_icon` shows the arguments and their defaults:

```
write_icon(text, size=80, bgcolor="white", fontcolor="black")
```

## Development instructions

Install requirements:

```
pip install -e requirements-dev.txt
```

Install pre-commit hook:

```
pre-commit install
```

Run tests:

```
black . tests/
```

## Deployment steps

First, update the version in `pyproject.toml`. Then run:

```
rm -rf dist/
python3 -m build
python3 -m twine upload dist/*
```
