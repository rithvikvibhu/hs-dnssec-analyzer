# Handshake DNSSEC Analyzer

A website that checks for DNSSEC with [dnsviz](https://github.com/dnsviz/dnsviz) and [delv](https://kb.isc.org/docs/aa-01152).


Currently available at http://dnssec.rithvik/, will move to a new Handshake name soon.

## Usage
Visit the site and enter any Handshake (or regular) domain.

## Development

```sh
git clone <this repo> && cd hs-dnssec-analyzer
pip install -r requirements.txt # Optionally, use a virtualenv before this
FLASK_ENV=development FLASK_APP=server.py flask run
```
