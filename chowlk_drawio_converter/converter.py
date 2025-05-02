import base64
import xml.dom.minidom
import xml.etree.ElementTree as ET
import zlib

import requests


def decode_diagram_data(data):
    compressed_data = base64.b64decode(data)
    decompressed_data = zlib.decompress(compressed_data, -15)
    return decompressed_data.decode('utf-8')

def append_decoded_children(parent, element):
    for child in element:
        if child.text and child.text.strip() and len(child) == 0:
            try:
                decoded_text = decode_diagram_data(child.text.strip())
                decoded_root = ET.fromstring(decoded_text)
                parent.append(decoded_root)
            except Exception:
                parent.append(child)
        else:
            new_child = ET.Element(child.tag, child.attrib)
            parent.append(new_child)
            append_decoded_children(new_child, child)

def export_drawio_page(input_file, page_name=None, page_index=0):
    tree = ET.parse(input_file)
    root = tree.getroot()
    if root.tag != "mxfile":
        raise Exception("Root element is not <mxfile>; this is not a standard draw.io file.")

    diagrams = root.findall('diagram')
    if not diagrams:
        raise Exception('No <diagram> elements found.')

    if page_name:
        diagram = next((d for d in diagrams if d.attrib.get('name') == page_name), None)
        if diagram is None:
            raise Exception(f'Page named "{page_name}" not found.')
    else:
        try:
            diagram = diagrams[page_index]
        except IndexError:
            raise Exception(f'Page index {page_index} out of range.')

    new_root = ET.Element("mxfile", root.attrib)
    new_diagram = ET.Element("diagram", diagram.attrib)
    new_root.append(new_diagram)

    if diagram.text and diagram.text.strip():
        xml_str = decode_diagram_data(diagram.text.strip())
        decoded_root = ET.fromstring(xml_str)
        new_diagram.append(decoded_root)
    else:
        append_decoded_children(new_diagram, diagram)
    # Pretty print using minidom
    rough_string = ET.tostring(new_root, encoding="utf-8")
    dom = xml.dom.minidom.parseString(rough_string)
    pretty_xml_as_string = dom.toprettyxml(indent="  ")
    # Remove empty lines
    pretty_xml_as_string = '\n'.join([line for line in pretty_xml_as_string.split('\n') if line.strip()])
    return pretty_xml_as_string

def send_xml_to_chowlk_api(xml_data):
    """
    Sends the XML data to the Chowlk API and returns the 'ttl_data' field from the JSON response.
    """
    url = "https://chowlk.linkeddata.es/api"

    files = {
        'data': ('diagram.xml', xml_data.encode('utf-8'), 'application/xml')
    }

    response = requests.post(url, files=files)
    response.raise_for_status()
    json_data = response.json()
    if "ttl_data" not in json_data:
        raise Exception("API response does not contain 'ttl_data' field.")
    return json_data["ttl_data"]
