# split_types

Types used for Split


# Deployment

To build and deploy, increment the version number in `pyproject.toml`, then run

```bash
pip install --upgrade build twine
python -m build
python -m twine upload dist/* --skip-existing
```

If you're prompted to log in, you'll need to generate an API token and
store it in `$HOME/.pypirc`
