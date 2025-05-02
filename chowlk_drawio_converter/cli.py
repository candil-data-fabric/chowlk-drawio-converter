import argparse

from chowlk_drawio_converter.converter import (export_drawio_page,
                                               send_xml_to_chowlk_api)


def main():
    parser = argparse.ArgumentParser(description='Convert a Chowlk diagram in draw.io page to an OWL ontology.')
    parser.add_argument('--input-file', help='Input .drawio file')
    parser.add_argument('--output-file', nargs='?', default='ontology.ttl', help='Output OWL file (default: ontology.ttl)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--page-name', help='Name of the page to export')
    group.add_argument('--page-index', type=int, help='Index of the page to export (0-based)')
    args = parser.parse_args()

    xml_data = export_drawio_page(
        args.input_file,
        page_name=args.page_name,
        page_index=args.page_index if args.page_index is not None else 0
    )

    # Send XML to Chowlk API and write TTL output
    ttl_data = send_xml_to_chowlk_api(xml_data)
    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(ttl_data)
    print(f'OWL ontology code saved to {args.output_file}')

if __name__ == '__main__':
    main()
