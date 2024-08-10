import importlib.util
from reynir import Greynir

""" Determine which parts of sentences are verb phrases """

spec = importlib.util.spec_from_file_location("random_sentence_txt", "./random_sentence_txt.py")
random_sentence_txt_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(random_sentence_txt_module)

def get_random_sentence():
    return random_sentence_txt_module.get_random_sentence_from_directory('./generated_data/verb')

def get_verb_phrases(sentence):
    g = Greynir()
    parsed_sentence = g.parse_single(sentence)
    verb_phrases = []

    if parsed_sentence.tree is None:
        return verb_phrases

    def traverse_tree(node):
        if node.is_terminal:
            return
        if node.tag == "VP":
            verb_phrases.append(node.text)
        for child in node.children:
            traverse_tree(child)

    traverse_tree(parsed_sentence.tree)
    
    return verb_phrases

"""def main():
    sentence = random_sentence_module.get_random_sentence_from_directory('./data/2019')
    if not sentence:
        print("No valid sentence found.")
        return
    
    print("Í sagnlið er aðalorðið sögn. Finnið sagnliðina í eftirfarandi setningu: ")
    print("Setning: ", sentence)
    
    correct_verb_phrases = get_verb_phrases(sentence)
    print("Skráið sagnliðina í setningunni (aðskiliði með kommu):")
    user_input = input().strip()
    
    if user_input:
        user_verb_phrases = [phrase.strip() for phrase in user_input.split(',')]
    else:
        user_verb_phrases = []

    if set(user_verb_phrases) == set(correct_verb_phrases):
        if correct_verb_phrases != []:
            print("Rétt! Atviksliðirnir eru:", ', '.join(correct_verb_phrases))
        else:
            print("Rétt! Setningin inniheldur engan atvikslið")
    else:
        if correct_verb_phrases != []:
            print("Rangt. Atviksliðirnir í setningunni er:", ', '.join(correct_verb_phrases))
        else:
            print("Rangt! Setningin inniheldur engan atvikslið")

if __name__ == "__main__":
    main()"""