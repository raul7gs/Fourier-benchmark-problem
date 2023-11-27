"""Tool used for the calculation of the constant term found in the approximation function. Inputs can come from
the Y and/or Z discipline, depending on an architectural decision. The constant term is calculated as the
surface or volume of an imaginary cone generated with the inputs mentioned before."""

import xml.etree.ElementTree as ET
from math import cos, sin
import numpy


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    c_list = []

    for c in root.findall("z/c"):    # Terms coming from the Z discipline
        c = float(c.text)
        c_list.append(c)

    for c in root.findall("y/c"):    # Terms coming from the Y discipline
        c = float(c.text)
        c_list.append(c)

    return c_list


def calculate(c_list):
    """Calculation of the constant term."""

    # Cone properties
    height = numpy.sum(c_list)
    radius = numpy.sum(c_list)

    if radius > 0 and height > 0:    # Output will be set to 0 if any measure is negative
        volume = numpy.pi * radius ** 2 * height / 3
        g = numpy.sqrt(radius ** 2 + height ** 2)
        surface = numpy.pi * radius ** 2 + numpy.pi * radius * g
    else:
        volume = 0
        surface = 0

    return surface, volume


def write_output(path, surface, volume):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('disciplines')
    c_tree = ET.SubElement(root_output_tree, 'C')
    surface_tree = ET.SubElement(c_tree, 'Surface')
    volume_tree = ET.SubElement(c_tree, 'Volume')

    surface_tree.text = str(surface)
    volume_tree.text = str(volume)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    c_list = read_input('ToolInput/toolinput.xml')
    surface, volume = calculate(c_list)
    write_output('ToolOutput/toolOutput.xml', surface, volume)


if __name__ == '__main__':
    run()
