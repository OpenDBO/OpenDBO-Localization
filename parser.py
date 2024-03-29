#!/usr/bin/python3
#
# OpenDBO - 2024
#
# Author(s): Grender

import argparse
import struct
import xml.etree.ElementTree as ET
import os


def parse_binary_to_xml(input_file, file_type):
    with open(input_file, 'rb') as f:
        root = ET.Element('table')
        
        if file_type == 'quest':
            padding = f.read(1)
            table_data = ET.SubElement(root, 'table_data')
            while True:
                table_idx_bytes = f.read(4)
                if not table_idx_bytes:
                    break
                table_idx = struct.unpack('<I', table_idx_bytes)[0]
                text_size = struct.unpack('<H', f.read(2))[0]
                text = f.read(text_size * 2).decode('utf-16le')
                
                text_elem = ET.SubElement(table_data, 'text', id=str(table_idx))
                text_elem.text = text
        else:
            while True:
                section_idx_bytes = f.read(4)
                if not section_idx_bytes:
                    break
                section_size_bytes = f.read(4)
                padding = f.read(1)
                
                section_size = struct.unpack('<I', section_size_bytes)[0]
                bytes_read = 1
                table_data = ET.SubElement(root, 'table_data')
                while True:
                    if bytes_read == section_size:
                        break
                    table_idx_bytes = f.read(4)
                    table_idx = struct.unpack('<I', table_idx_bytes)[0]
                    text_size = struct.unpack('<H', f.read(2))[0]
                    text = f.read(text_size * 2).decode('utf-16le')
                    
                    bytes_read += 4 + 2 + (text_size * 2)
                    
                    text_elem = ET.SubElement(table_data, 'text', id=str(table_idx))
                    text_elem.text = text
        

    output_file = input_file.replace('.rdf', '.xml')
    indent(root)
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-16le', xml_declaration=True)


def generate_binary_from_xml(input_file, file_type):
    output_file = input_file.replace('.xml', '.rdf')
    root = ET.parse(input_file).getroot()

    with open(output_file, 'wb') as f:
        if file_type == 'quest':
            f.write(b'\x01')
            for text_elem in root.find('table_data').findall('text'):
                table_idx = int(text_elem.get('id'))
                text = text_elem.text.encode('utf-16le') if text_elem.text else b''  # Treat empty text as empty bytes
                text_size = len(text_elem.text) if text_elem.text else 0
                f.write(struct.pack('<I', table_idx))
                f.write(struct.pack('<H', text_size))
                f.write(text)
        else:
            section_idx = 0
            for table_data in root.findall('table_data'):
                # Write section index
                f.write(struct.pack('<I', section_idx))

                # Start writing section size placeholder
                section_size_pos = f.tell()
                f.write(struct.pack('<I', 0))  # Placeholder for section size
                f.write(b'\x01')  # Padding byte

                # Count the total bytes to be written in this section
                total_bytes = 1  # For padding byte
                for text_elem in table_data.findall('text'):
                    table_idx = int(text_elem.get('id'))
                    text = text_elem.text.encode('utf-16le') if text_elem.text else b''  # Treat empty text as empty bytes
                    text_size = len(text_elem.text) if text_elem.text else 0
                    f.write(struct.pack('<I', table_idx))
                    f.write(struct.pack('<H', text_size))
                    f.write(text)
                    total_bytes += 4 + 2 + len(text)
                
                # Write the actual section size after counting the total bytes
                f.seek(section_size_pos)
                f.write(struct.pack('<I', total_bytes))
                f.seek(0, os.SEEK_END)  # Move to the end of the file

                section_idx += 1  # Increment section index for the next section


def indent(elem, level=0):
    indent_size = 2
    i = '\n' + level * ' ' * indent_size
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + ' ' * indent_size
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def main():
    parser = argparse.ArgumentParser(description='Convert RDF files to XML or vice versa.')
    parser.add_argument('input_file', type=str, help='Input file name')
    parser.add_argument('--file-type', type=str, choices=['quest', 'text'], required=True,
                        help='Type of the input file: "quest" or "text"')
    parser.add_argument('--to-xml', action='store_true', help='Convert binary to XML')
    parser.add_argument('--to-rdf', action='store_true', help='Convert XML to binary')
    args = parser.parse_args()

    if args.to_xml:
        parse_binary_to_xml(args.input_file, args.file_type)
    elif args.to_rdf:
        generate_binary_from_xml(args.input_file, args.file_type)
    else:
        print('Please specify either \'--to-xml\' or \'--to-rdf\'.')


if __name__ == '__main__':
    main()
