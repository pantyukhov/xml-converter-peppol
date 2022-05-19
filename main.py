from src.io import *
from src.convert import *


def convert_xml(file_name, kbo_number):
    """
    Reads, converts and writes an XML file to a XML file that adheres peppol rules.
    """
    xml = read_xml(file_name)
    converted = convert_xml_to_peppol(xml, kbo_number)
    write_xml(xml, file_name)


def convert_xml_to_peppol(xml, kbo_number):
    """
    Converts an XML file to a XML file that adheres peppol rules.
    """
    return xml


xml = read_xml("odoo.xml")
print(xml)
print_xml_children(xml)
print('********************************************************')
create_invoice_elementtree(xml, "0478693713")
# Write the XML to a file
write_xml("test.xml",xml)