"""Tool used for the calculation of the cosine trigonometric terms in te approximation function. This tool
receives as input the coefficient and the harmonics associated to the terms. An additional input is used
for evaluating the expression. The value of the expression can later be used as input for the C discipline."""

import xml.etree.ElementTree as ET
from math import cos, sin
from numpy import pi


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    a = float(root.find("y/A").text)    # Coefficient
    x0 = float(root.find("x").text)
    w_list = []
    for w in root.findall("y/wa"):    # Harmonics
        w = float(w.text) * 2 * pi
        w_list.append(w)

    return a, x0, w_list


def calculate(a, x0, w_list):
    """Calculation of the constant term."""

    output_y = ""
    c = 0
    for w in w_list:
        output_y = output_y + "{A}*cos({w}*x)+".format(A=a, w=w)
        c = c + a * cos(w * x0)

    return output_y, c


def write_output(path, output_y, c):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('disciplines')
    y_tree = ET.SubElement(root_output_tree, 'y')
    output_y_tree = ET.SubElement(y_tree, 'output_y')
    c_tree = ET.SubElement(y_tree, 'c')

    output_y = str(output_y)
    output_y_tree.text = output_y[:-1]
    c_tree.text = str(c)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    a, x0, w_list = read_input('ToolInput/toolinput.xml')
    output_y, c = calculate(a, x0, w_list)
    write_output('ToolOutput/toolOutput.xml', output_y, c)


if __name__ == '__main__':
    run()
