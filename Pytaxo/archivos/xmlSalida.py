try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
def plantillaGenericaSalida():
    raizXml=ET.Element('plantilla')
    ET.SubElement(raizXml,'enunciado')
    ET.SubElement(raizXml,'opciones')
    return raizXml