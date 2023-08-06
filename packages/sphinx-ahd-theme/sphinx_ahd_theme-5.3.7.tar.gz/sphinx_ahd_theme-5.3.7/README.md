# [Sphinx AHD theme](https://sphinx-ahd-theme.netlify.app/)
## Installation

```sh
pip install sphinx-ahd-theme
```

## Usage

Select the "Sphinx AHD theme" in the `conf.py` file of a Sphinx

```python
# include the theme in the list of extensions to be loaded
extensions = ['sphinx_ahd_theme', …]

# select the theme
html_theme = 'sphinx_ahd_theme'
```

-   See the documentation for more usage instructions

## Development

### Getting started

-   [Instructions for Mac, Linux, and Windows](docs/development.rst)

### Release process

Checklist:

-   [ ] `CONTRIBUTORS.md` is updated
-   [ ] `CHANGELOG.md` is updated
-   [ ] `setup.cfg` is updated (see `version`)
-   [ ] Everything is committed, clean checkout
-   [ ] `~/.pypirc` has a username and password (token)
-   [ ] Add a git tag and a Github release once completed

With an active virtual environment:

```sh
python -m pip install --upgrade -r requirements.txt
make clean
make clean-frontend
npm ci
npm run build
prerelease
git tag -a N.N.N -m "N.N.N"
git push origin N.N.N
python -m build
python -m twine upload --repository pypi dist/*
postrelease
```

## Credits

[Sphinx AHD theme](https://github.com/ahdcreative/sphinx_ahd_theme) is based on [Sphinx Typo3 theme](https://github.com/TYPO3-Documentation/sphinx_typo3_theme) which is based on [t3SphinxThemeRtd](https://github.com/typo3-documentation/t3SphinxThemeRtd) which is based on the [Read the Docs Sphinx theme](https://github.com/readthedocs/sphinx_rtd_theme).
