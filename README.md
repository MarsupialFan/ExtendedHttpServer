# extended-python-webserver

An extension of Python's `http.server` supporting custom MIME types and server-side processing.

## Extended functionality
* Support for server-side processing of .scss files to produce the corresponding .css files.
* Return `text/css` MIME type for explicitly requested .scss files (rather than the `application/octet-stream` MIME type returned by `http.server`).

## Setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
This can be skipped if you have `libsass` installed.

## Usage
```
python3 webserver.py
```

## Cleaning up the Python virtual environment
```
deactivate
rm -r venv
```
