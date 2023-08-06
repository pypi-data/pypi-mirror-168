# ewoksweb

_ewoksweb_ is a frontend to create, visualize and execute
[ewoks](https://ewoks.readthedocs.io/) workflows in the web.

## Demo

https://workflow.gitlab-pages.esrf.fr/ewoks/ewoksweb/

## From source

Start the frontend

```bash
npm start
```

Build the package for deployment on pypi

```bash
npx -y browserslist@latest --update-db  # optional
npm install
npm run build
python setup.py sdist
```

## From pypi

Install REST server only (`ewoksserver` is another package)

```bash
pip install ewoksserver
```

Install REST server with frontend (`ewoksserver` has `ewoksweb` as optional
dependency)

```bash
pip install ewoksserver[frontend]
```

or alternatively

```bash
pip install ewoksserver
pip install ewoksweb
```

Start the server that serves the frontend

```bash
ewoks-server
```

or for an installation with the system python

```bash
python3 -m ewoksserver.server
```

## Documentation

https://ewoksweb.readthedocs.io/
