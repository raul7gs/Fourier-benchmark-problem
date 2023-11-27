"""Tool used for the calculation of the sine trigonometric terms in te approximation function. This tool
receives as input the coefficient and the harmonics associated to the terms. An additional input is used
for evaluating the expression. The value of the expression can later be used as input for the C discipline."""

import xml.etree.ElementTree as ET
from math import cos, sin
from numpy import pi


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    b = float(root.find("z/B").text)     # Coefficient
    x0 = float(root.find("x").text)
    w_list = []
    for w in root.findall("z/wb"):    # Harmonics
        w = float(w.text) * 2 * pi
        w_list.append(w)

    return b, x0, w_list


def calculate(b, x0, w_list):
    """Calculation of the sines terms."""

    output_z = ""
    c = 0
    for w in w_list:
        output_z = output_z + "{B}*sin({w}*x)+".format(B=b, w=w)
        c = c + b * sin(w * x0)

    return output_z, c


def write_output(path, output_z, c):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('disciplines')
    z_tree = ET.SubElement(root_output_tree, 'z')
    output_z_tree = ET.SubElement(z_tree, 'output_z')
    c_tree = ET.SubElement(z_tree, 'c')

    output_z = str(output_z)
    output_z_tree.text = output_z[:-1]
    c_tree.text = str(c)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    b, x0, w_list = read_input('ToolInput/toolinput.xml')
    output_z, c = calculate(b, x0, w_list)
    write_output('ToolOutput/toolOutput.xml', output_z, c)


if __name__ == '__main__':
    run()
