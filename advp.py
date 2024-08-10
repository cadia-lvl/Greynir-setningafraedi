import importlib.util
from reynir import Greynir

""" Determine which parts of sentences are adverb phrases """

# Import the get_random_sentence_from_directory function from random_sentence.py
spec = importlib.util.spec_from_file_location("random_sentence_txt", "./random_sentence_txt.py")
random_sentence_txt_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(random_sentence_txt_module)

def get_random_sentence():
    return random_sentence_txt_module.get_random_sentence_from_directory('./generated_data/adverb')

def get_adv_phrases(sentence):
    g = Greynir()
    parsed_sentence = g.parse_single(sentence)
    adv_phrases = []

    if parsed_sentence.tree is None:
        return adv_phrases  # Return an empty list if the tree is None

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

###### ATHUGA ########
# Önnur möguleg verkefni
# Búa bara til setningar sem innihalda atviksliði?
# Flokka atviksliði í undirflokka

"""
def main():
    sentence = random_sentence_module.get_random_sentence_from_directory('./data/2021')
    if not sentence:
        print("Ekki fannst lögleg setning.")
        return

    print("Atviksliður samanstendur af einu atviksorði. Finnið atviksliðina í eftirfarandi setningu: ")
    print("Setning: ", sentence)

    correct_adv_phrases = get_adv_phrases(sentence)
    print("Skráið atviksliðina í setningunni (aðskiliði með kommu), eða ýtið á Enter ef engir atviksliðir eru:")
    user_input = input().strip()
    
    if user_input:
        user_adv_phrases = [phrase.strip() for phrase in user_input.split(',')]
    else:
        user_adv_phrases = []

    if set(user_adv_phrases) == set(correct_adv_phrases):
        if correct_adv_phrases:
            print("Rétt! Atviksliðirnir eru:", ', '.join(correct_adv_phrases))
        else:
            print("Rétt! Setningin inniheldur engan atvikslið")
    else:
        if correct_adv_phrases:
            print("Rangt. Atviksliðirnir í setningunni eru:", ', '.join(correct_adv_phrases))
        else:
            print("Rangt! Setningin inniheldur engan atvikslið")

if __name__ == "__main__":
    main()
"""    