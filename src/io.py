import xml.etree.ElementTree as ET


def read_xml(file_path):
    """
    Reads an nested XML file and returns a dictionary with the data.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


def write_xml(file_path, data):
    """
    Writes an XML file with the data.
    :param file_path: The path to the file.
    :param data: The elementTree to write.
    """
    tree = ET.ElementTree(data)
    tree.write(file_path, xml_declaration=True, encoding="utf-8")


def print_xml_children(element):
    """
    Prints the children of an element.
    :param element: The element to print the children of.
    """
    for child in element:
        print(child.tag, child.attrib)
