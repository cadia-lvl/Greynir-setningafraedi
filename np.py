import importlib.util
from reynir import Greynir

""" Determine which parts of sentences are noun phrases """

spec = importlib.util.spec_from_file_location("random_sentence_txt", "./random_sentence_txt.py")
random_sentence_txt_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(random_sentence_txt_module)

def get_random_sentence():
    return random_sentence_txt_module.get_random_sentence_from_directory('./generated_data/noun')

def get_noun_phrases(sentence):
    g = Greynir()
    parsed_sentence = g.parse_single(sentence)
    noun_phrases = []

    if parsed_sentence.tree is None:
        return noun_phrases

    def traverse_tree(node):
        if node.is_terminal:
            return
        if node.tag == "NP":
            noun_phrases.append(node.text)
        for child in node.children:
            traverse_tree(child)

    traverse_tree(parsed_sentence.tree)
    
    return noun_phrases

"""
def main():
    sentence = random_sentence_module.get_random_sentence_from_directory('./data/2019')
    if not sentence:
        print("Ekki fannst lögleg setning.")
        return
    
    print("Í nafnlið er aðalorðið nafnorð eða sérstætt fornafn. Finnið nafnliðina í eftirfarandi setningu: ")
    print("Setning: ", sentence)
    
    correct_noun_phrases = get_noun_phrases(sentence)
    print("Skráið nafnliðina í setningunni (aðskiliði með kommu), eða ýtið á Enter ef engir nafnliðir eru:")
    user_input = input().strip()
    
    if user_input:
        user_noun_phrases = [phrase.strip() for phrase in user_input.split(',')]
    else:
        user_noun_phrases = []

    if set(user_noun_phrases) == set(correct_noun_phrases):
        if correct_noun_phrases != []:
            print("Rétt! Nafnliðurinn er:", ', '.join(correct_noun_phrases))
        else:
            print("Rétt! Setningin inniheldur engan nafnlið")
    else:
        if correct_noun_phrases != []:
            print("Rangt. Nafnliðurinn í setningunni er:", ', '.join(correct_noun_phrases))
        else:
            print("Rangt! Setningin inniheldur engan nafnlið")

if __name__ == "__main__":
    main()"""