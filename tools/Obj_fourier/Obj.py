"""Tool used for the calculation of the objective function. First the expression for the approximation
function is built. After that, the error between the original sawtooth function and the approximation is
calculated through the integration of the difference square."""

import xml.etree.ElementTree as ET
from math import cos, sin
import numpy as np
from scipy.integrate import quad
from scipy.signal import sawtooth


def read_input(path):
    """Inputs from the XML file are read."""

    tree = ET.parse(path)
    root = tree.getroot()

    obj_list = []

    try:     # Independent term coming from C discipline
        c = float(root.find("C/Surface").text)
        obj_list.append(str(c))
    except AttributeError:
        c = float(root.find("C/Volume").text)
        obj_list.append(str(c))

    for y in root.findall("y/output_y"):    # Terms coming from Y discipline
        term = y.text
        obj_list.append(term)

    for z in root.findall("z/output_z"):    # Terms coming from Z discipline
        term = z.text
        obj_list.append(term)

    return obj_list


def calculate(obj_list):
    """Calculation of the error."""

    g = ""
    for element in obj_list:
        g = g + element + "+"

    g = g[:-1]

    def series(x):
        return eval(g)

    def my_signal(x):
        return 0.5 + sawtooth(2 * np.pi * (x - 0.5))

    def difference(x):
        return (my_signal(x) - series(x)) ** 2

    ideal_result = 0.16006074894366096    # Result from Fourier original solution. Used to normalize objective

    result_series, error = quad(difference, -1, 1)
    result = result_series / ideal_result

    return result


def write_output(path, result):
    """Generation of the output XML file"""

    root_output_tree = ET.Element('disciplines')
    obj_tree = ET.SubElement(root_output_tree, 'Objective')
    obj_obj_tree = ET.SubElement(obj_tree, 'error')

    obj_obj_tree.text = str(result)

    tree_output = ET.ElementTree(root_output_tree)
    tree_output.write(path)

    pass


def run():
    """Execution of the tool"""

    obj_list = read_input('ToolInput/toolinput.xml')
    result = calculate(obj_list)
    write_output('ToolOutput/toolOutput.xml', result)


if __name__ == '__main__':
    run()
