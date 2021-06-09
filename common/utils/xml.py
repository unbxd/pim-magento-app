from xml.etree.ElementTree import Element, SubElement, Comment, tostring


def create_root_element(element_name, attributes):
    root = Element(element_name)
    for attribute_key, attribute_value in attributes.items():
        root.set(attribute_key, attribute_value)
    return root


def add_sub_element(parent_element, element_name, text=None):
    sub_element = SubElement(parent_element, element_name)
    if text:
        sub_element.text = text
    return sub_element
