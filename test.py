import xml.etree.ElementTree as ET
import pandas as pd
import io

# The XML string you provided
xml_string = """<ns:getTrxXmlResponse xmlns:ns="http://Test_Ws">ns:return<?xml version="1.0"?><transaction>..."""

# Remove the namespace prefix and wrap the content in a root element
xml_string = xml_string.replace('ns:', '')
xml_string = '<root>' + xml_string + '</root>'

# Parse the XML
tree = ET.fromstring(xml_string)

# Find all 'oary' elements
oary_elements = tree.findall('.//oary')

# Create a list to store the data
data = []