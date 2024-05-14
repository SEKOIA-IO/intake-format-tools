# Send events to SEKOIA.IO

## Usage

```console
Usage: send_events.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.
  --prod                Send events to prod (test by default)

Commands:
  from-cli
  from-intake-formats
  from-text-file
```

## Example

### From intake-formats input files

Each test file `["input"]["message"]` will be sent as an event.

```console
poetry run send_events.py from-intake-formats "<intake-key>" intake-formats/SentinelOne/sentinelone/
```

### From text file

Each line will be sent as an event

```console
poetry run send_events.py from-text-file "<intake-key>" ~/Downloads/stormshield.txt
```

### From the terminal

Send one line from the terminal

```console
poetry run send_events.py from-cli "<intake-key>" '<event>'
```
