import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

def make_pretty(xml_etree, indent=2):
    """Pretty-printer for XML etree."""

    etree_str = ET.tostring(xml_etree.getroot(), 'utf-8')
    as_minidom = minidom.parseString(etree_str)
    indent_spaces = ' ' * indent
    xml_str = as_minidom.toprettyxml(indent=indent_spaces)

    return xml_str.lstrip('<?xml version="1.0" ?>').lstrip()
