# chowlk-drawio-converter

Generate OWL ontology from Chowlk diagram directly from the specified drawio page.

## Usage Instructions

```
usage: chowlk-drawio-converter [-h] [--input-file INPUT_FILE] [--output-file [OUTPUT_FILE]]
                               (--page-name PAGE_NAME | --page-index PAGE_INDEX)

Convert a Chowlk diagram in draw.io page to an OWL ontology.

options:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        Input .drawio file
  --output-file [OUTPUT_FILE]
                        Output OWL file (default: ontology.ttl)
  --page-name PAGE_NAME
                        Name of the page to export
  --page-index PAGE_INDEX
                        Index of the page to export (0-based)
```

## Examples

Export by page name:

```bash
chowlk-drawio-converter --input-file diagram.drawio --page-name “Page 1”
````

Export by page index and specify output files:

```bash
chowlk-drawio-converter --input-file diagram.drawio --output_file result.ttl --page-index 0
```
