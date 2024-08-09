import os
import random
import xml.etree.ElementTree as ET
import re

def is_valid_sentence(sentence):
    # A valid sentence should not start with a comma
    if sentence.startswith(','):
        return False
    
    # A valid sentence should not have a period in the middle
    if re.search(r'\.\s+', sentence):
        return False

    return True

def get_random_sentence_from_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
    sentences = root.findall('.//tei:s', namespaces)

    valid_sentences = []
    for sentence in sentences:
        sentence_content = []
        for elem in sentence:
            if elem.tag.endswith('w') or elem.tag.endswith('pc'):
                sentence_content.append(elem.text)
        full_sentence = ' '.join(sentence_content).strip()
        word_count = len(full_sentence.split())
        if 5 <= word_count < 7 and is_valid_sentence(full_sentence):
            valid_sentences.append(full_sentence)

    if not valid_sentences:
        return None

    return random.choice(valid_sentences)

def get_random_sentence_from_directory(directory_path):
    xml_files = []
    for root_dir, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root_dir, file))

    if not xml_files:
        return None

    random_file = random.choice(xml_files)
    return get_random_sentence_from_file(random_file)

if __name__ == "__main__":
    parent_directory_path = './data'
    random_sentence = get_random_sentence_from_directory(parent_directory_path)
    if random_sentence:
        print("Random sentence:", random_sentence)
    else:
        print("No valid sentences found in the selected files.")