# Publish intake-format to SEKOIA.IO

## Usage

```console
usage: publish_format.py [-h] [--prod] path apikey
publish_format.py: error: the following arguments are required: path, apikey
```

## Getting started

To ease the installation of tools, this project relies on [mise-en-place](https://mise.jdx.dev/).
Please follow the [getting started](https://mise.jdx.dev/getting-started.html) to install and set up mise-en-place.

## Example

### Publish in app.test.sekoia.io
```
uv run publish_format.py intake-formats/SentinelOne/sentinelone/ '<API KEY>'
```

### Publish in production

```console
uv run publish_format.py --prod intake-formats/SentinelOne/sentinelone/ '<api-key>'
```

### Publish the repo

```console
uv run publish_format.py intake-formats/ '<api-key>'
```

### Publish the repo to test without prompt

```console
uv run publish_format.py intake-formats/ --no-diff --allow-deployment '<api-key>'
```

### Publish the repo to prod without prompt

```console
uv run publish_format.py intake-formats/ --no-diff --allow-deployment --prod --allow-prod '<api-key>'
```
