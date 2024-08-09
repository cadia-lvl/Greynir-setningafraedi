import os
import random
import re

def is_valid_sentence(sentence):
    if sentence.startswith(','):
        return False
    
    if sentence.startswith('-'):
        return False
    
    if sentence.startswith(':'):
        return False
    
    if re.search(r'\.\s+', sentence):
        return False

    return True

def get_random_sentence_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    
    valid_sentences = []
    for sentence in sentences:
        full_sentence = sentence.strip()
        word_count = len(full_sentence.split())
        if 5 <= word_count < 7 and is_valid_sentence(full_sentence):
            valid_sentences.append(full_sentence)

    if not valid_sentences:
        return None

    return random.choice(valid_sentences)

def get_random_sentence_from_directory(directory_path):
    txt_files = []
    for root_dir, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root_dir, file))

    if not txt_files:
        return None

    random_file = random.choice(txt_files)
    return get_random_sentence_from_file(random_file)

if __name__ == "__main__":
    parent_directory_path = './generated_data'
    random_sentence = get_random_sentence_from_directory(parent_directory_path)
    if random_sentence:
        print("Random sentence:", random_sentence)
    else:
        print("No valid sentences found in the selected files.")
