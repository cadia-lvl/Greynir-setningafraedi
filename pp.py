import importlib.util
from reynir import Greynir

""" Determine which parts of sentences are preposition phrases """

spec = importlib.util.spec_from_file_location("random_sentence_txt", "./random_sentence_txt.py")
random_sentence_txt_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(random_sentence_txt_module)

def get_random_sentence():
    return random_sentence_txt_module.get_random_sentence_from_directory('./generated_data/preposition')

def get_p_phrases(sentence):
    g = Greynir()
    parsed_sentence = g.parse_single(sentence)
    p_phrases = []

    if parsed_sentence.tree is None:
        return p_phrases

    def traverse_tree(node):
        if node.is_terminal:
            return
        if node.tag == "PP":
            p_phrases.append(node.text)
        for child in node.children:
            traverse_tree(child)

    traverse_tree(parsed_sentence.tree)
    
    return p_phrases

"""
def main():
    sentence = random_sentence_module.get_random_sentence_from_directory('./data/2019')
    if not sentence:
        print("Ekki fannst lögleg setning.")
        return
    
    print("Forsetningarliður samanstendur af forsetningu og fallorðinu/fallorðunum sem hún stýrir fallinu á. Finnið forsetningarliðina í eftirfarandi setningu: ")
    print("Setning: ", sentence)
    
    correct_p_phrases = get_p_phrases(sentence)
    print("Skráið forsetningarliðina í setningunni (aðskiliði með kommu), eða ýtið á Enter ef engir nafnliðir eru:")
    user_input = input().strip()
    
    if user_input:
        user_p_phrases = [phrase.strip() for phrase in user_input.split(',')]
    else:
        user_p_phrases = []

    if set(user_p_phrases) == set(correct_p_phrases):
        if correct_p_phrases != []:
            print("Rétt! Forsetningarliðirnir eru:", ', '.join(correct_p_phrases))
        else:
            print("Rétt! Setningin inniheldur engan forsetningarlið")
    else:
        if correct_p_phrases != []:
            print("Rangt. Forsetningarliðirnir í setningunni eru:", ', '.join(correct_p_phrases))
        else:
            print("Rangt! Setningin inniheldur engan forsetningarlið")

if __name__ == "__main__":
    main()
"""
