import importlib.util
from reynir import Greynir

""" Determine which parts of sentences are adjective phrases """

spec = importlib.util.spec_from_file_location("random_sentence_txt", "./random_sentence_txt.py")
random_sentence_txt_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(random_sentence_txt_module)

def get_random_sentence():
    return random_sentence_txt_module.get_random_sentence_from_directory('./generated_data/adjective')

def get_a_phrases(sentence):

    g = Greynir()
    parsed_sentence = g.parse_single(sentence)
    a_phrases = []

    terminals = parsed_sentence.terminals

    if terminals is None:
        return a_phrases
    
    for i in range(len(terminals)):
        if terminals[i].category == "lo":
            if i > 0 and terminals[i - 1].category == "eo":
                a_phrases.append(f"{terminals[i - 1].text} {terminals[i].text}")
            else:
                a_phrases.append(terminals[i].text)
    
    if parsed_sentence.tree is None:
        return a_phrases
    
    return a_phrases

"""
def main():
    sentence = random_sentence_module.get_random_sentence_from_directory('./data/2019')
    #sentence = "Stelpan er svakalega falleg"
    if not sentence:
        print("Ekki fannst lögleg setning.")
        return
    
    print("Í lýsingarlið er aðalorðið lýsingarorð en þau geta einnig tekið með sér áhersluatviksorð og þá tilheyrir atviksorðið lýsingarliðnum. Finnið lýsingarliðina í eftirfarandi setningu: ")
    print("Setning: ", sentence)
    
    correct_ad_phrases = get_ad_phrases(sentence)
    print("Skráið lýsingarliðina í setningunni (aðskiliði með kommu), eða ýtið á Enter ef engir lýsingarliðir eru:")
    user_input = input().strip()
    
    if user_input:
        user_ad_phrases = [phrase.strip() for phrase in user_input.split(',')]
    else:
        user_ad_phrases = []

    if set(user_ad_phrases) == set(correct_ad_phrases):
        if correct_ad_phrases != []:
            print("Rétt! lýsingarliðurinn er:", ', '.join(correct_ad_phrases))
        else:
            print("Rétt! Setningin inniheldur engan lýsingarlið")
    else:
        if correct_ad_phrases != []:
            print("Rangt. lýsingarliðurinn í setningunni er:", ', '.join(correct_ad_phrases))
        else:
            print("Rangt! Setningin inniheldur engan lýsingarlið")

if __name__ == "__main__":
    main()
"""