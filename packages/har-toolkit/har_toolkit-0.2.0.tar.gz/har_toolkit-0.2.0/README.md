# Har-Toolkit

A module to easily work with HAR (HTTP Archive) files.

## Installation
```
pip install --upgrade har-toolkit
```

## Usage
To use this module in your code:
```
import har_toolkit
```

To read and parse a HAR file:
```
import har_toolkit
har = har_toolkit.read_har_file("<path/to/har_file>")
```
This will return a HarReader object with the contents of the file parsed according to [this W3C document](https://w3c.github.io/web-performance/specs/HAR/Overview.html)

The different sections of the format can be accessed by calling that section attribute on the parent class. Example: `har.browser` or `har.entries`

