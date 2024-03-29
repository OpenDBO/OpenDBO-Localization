#!/usr/bin/python3
#
# OpenDBO - 2024
#
# Author(s): Grender

import re
import sys

def detect_chinese_characters(file_path):
    lines_detected = 0
    try:
        with open(file_path, 'r', encoding='utf-16le') as file:
            line_number = 0
            for line in file:
                line_number += 1
                if line_number == 1:
                    # Remove BOM (Byte Order Mark) if present
                    line = line.lstrip('\ufeff')
                if re.search(r'[\u4e00-\u9fff]+', line):  # Regular expression for Chinese characters
                    lines_detected += 1
                    print(f'Chinese characters detected in line {line_number}')
    except FileNotFoundError:
        print('File not found.')
    except UnicodeDecodeError:
        print('Error: Unable to decode the file. Please ensure the file is encoded correctly.')
    except Exception as e:
        print(f'An error occurred: {e}')
        
    print(f'Total lines detected: %s' % lines_detected)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script_name.py file_name')
    else:
        file_path = sys.argv[1]
        detect_chinese_characters(file_path)
