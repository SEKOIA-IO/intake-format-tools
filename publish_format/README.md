# Publish intake-format to SEKOIA.IO

## Usage

```console
usage: publish_format.py [-h] [--prod] path apikey
publish_format.py: error: the following arguments are required: path, apikey
```

## Example

### Publish in app.test.sekoia.io
```
poetry run python3 publish_format.py intake-formats/SentinelOne/sentinelone/ '<API KEY>'
```

### Publish in production

```console
poetry run python3 publish_format.py --prod intake-formats/SentinelOne/sentinelone/ '<api-key>'
```

### Publish the repo

```console
poetry run python3 publish_format.py intake-formats/ '<api-key>'
```

### Publish the repo to test without prompt

```console
poetry run python3 publish_format.py intake-formats/ --no-diff --allow-deployment '<api-key>'
```

### Publish the repo to prod without prompt

```console
poetry run python3 publish_format.py intake-formats/ --no-diff --allow-deployment --prod --allow-prod '<api-key>'
```
