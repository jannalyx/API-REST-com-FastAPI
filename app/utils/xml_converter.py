import csv
import xml.etree.ElementTree as ET
import os

def converter_csv_para_xml(csv_path: str, xml_path: str, root_element_name: str, item_element_name: str):
    with open(csv_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        root = ET.Element(root_element_name)

        for row in reader:
            item = ET.SubElement(root, item_element_name)
            for key, value in row.items():
                child = ET.SubElement(item, key)
                child.text = value
        
        tree = ET.ElementTree(root)
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)