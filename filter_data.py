import os
import xml.etree.ElementTree as ET
from reynir import Greynir

# Function to extract adverb phrases from a sentence
def get_adv_phrases(sentence):
    g = Greynir()
    parsed_sentence = g.parse_single(sentence)
    adv_phrases = []

    if parsed_sentence is None or parsed_sentence.tree is None:
        return adv_phrases  # Return an empty list if the parsed sentence or the tree is None

    # Traverse the parse tree to find adverb phrases
    def traverse_tree(node):
        if node.is_terminal:
            return
        if node.tag == "ADVP":  # "ADVP" is the tag for adverb phrases
            adv_phrases.append(node.text)
        for child in node.children:
            traverse_tree(child)

    traverse_tree(parsed_sentence.tree)

    return adv_phrases

# Function to process XML files and extract sentences with adverb phrases
def extract_sentences_with_adv_phrases(folder_path, output_file):
    # Create the root element of the new XML
    root_element = ET.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0", xml_lang="is")
    tei_header = ET.SubElement(root_element, "teiHeader")
    file_desc = ET.SubElement(tei_header, "fileDesc")
    title_stmt = ET.SubElement(file_desc, "titleStmt")
    title = ET.SubElement(title_stmt, "title", type="main", xml_lang="is")
    title.text = "Sentences with Adverb Phrases"
    text_element = ET.SubElement(root_element, "text")
    body_element = ET.SubElement(text_element, "body")
    main_div = ET.SubElement(body_element, "div", type="main")

    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract sentences and check for adverb phrases
            for s in root.iter("{http://www.tei-c.org/ns/1.0}s"):
                sentence = "".join(s.itertext())
                adv_phrases = get_adv_phrases(sentence)
                if adv_phrases:
                    p_element = ET.SubElement(main_div, "p")
                    s_element = ET.SubElement(p_element, "s")
                    s_element.text = sentence

    # Write the new XML structure to the output file
    tree = ET.ElementTree(root_element)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)

# Define the folder path and output file
folder_path = os.path.join(os.path.dirname(__file__), "data", "2019")
output_file = "output.xml"

# Call the function to process XML files and create a new XML file
extract_sentences_with_adv_phrases(folder_path, output_file)