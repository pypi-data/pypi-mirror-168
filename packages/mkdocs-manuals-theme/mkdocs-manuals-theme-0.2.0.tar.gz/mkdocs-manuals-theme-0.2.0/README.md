# Theme for creating team manuals

This theme is based on top of mkdocs-basic-theme.

https://github.com/mkdocs/mkdocs-basic-theme

## Development

Setting up dev environment:

```bash
# create and activate virtual env
python3 -m venv .venv
source .venv/bin/activate

# install requirements
pip install '.[dev]'
```

## Summary of understanding

The documentation around templating is pretty good. It is all on one page :)
https://www.mkdocs.org/dev-guide/themes/#navigation-objects

There are 2 global variables on each page:
`nav` and `toc`

Nav is an iterable of 3 kinds of page: `section`, `page` and `link`