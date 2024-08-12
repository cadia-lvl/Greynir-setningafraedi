from flask import Flask, render_template, request, jsonify
import logging
from waitress import serve
import importlib.util

""" Server code for the application. To run the application please run this file. """

# Logging
logging.basicConfig(level=logging.DEBUG)

######## IMPORTS ########
# advp.py module
spec = importlib.util.spec_from_file_location("adv", "./advp.py")
adv_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adv_module)

# pp.py module
spec = importlib.util.spec_from_file_location("pp", "./pp.py")
p_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p_module)

# vp.py module
spec = importlib.util.spec_from_file_location("vp", "./vp.py")
v_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v_module)

# np.py module
spec = importlib.util.spec_from_file_location("np", "./np.py")
noun_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(noun_module)

# ap.py module
spec = importlib.util.spec_from_file_location("ap", "./ap.py")
a_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a_module)

# analyze.py module for the detailed analyzes
spec = importlib.util.spec_from_file_location("analyze", "./analyze.py")
analyze_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze_module)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

####### NAFNLIÐIR ########
@app.route('/nafnliðir', methods=['GET', 'POST'])
def nafnliðir():
    try:
        if request.method == 'GET':
            sentence = noun_module.get_random_sentence()
            result = None
            correct = False
            return render_template('nafnliðir.html', sentence=sentence, result=result, correct=correct)
        else:
            sentence = request.form.get('sentence')
            user_input = request.form.get('noun_phrases', '').strip()
            if user_input:
                user_noun_phrases = [phrase.strip().lower() for phrase in user_input.split(',')]
            else:
                user_noun_phrases = []
            correct_noun_phrases = [phrase.lower() for phrase in noun_module.get_noun_phrases(sentence)]

            if set(user_noun_phrases) == set(correct_noun_phrases):
                correct = True
                if correct_noun_phrases:
                    result_phrases = []
                    for phrase in correct_noun_phrases:
                        if len(phrase.split()) == 1:
                            result_phrases.append(f'<a class="hoverable-word" href="/noun/{phrase}?sentence={sentence}">{phrase}</a>')
                        else:
                            result_phrases.append(phrase)
                    result = f"Rétt! Nafnliðirnir í setningunni eru: <span class='correct-phrases'>{', '.join(result_phrases)}</span>"
                else:
                    result = "Rétt! Setningin inniheldur engan nafnlið"
            else:
                correct = False
                if correct_noun_phrases:
                    result_phrases = []
                    for phrase in correct_noun_phrases:
                        if len(phrase.split()) == 1:
                            result_phrases.append(f'<a class="hoverable-word" href="/noun/{phrase}?sentence={sentence}">{phrase}</a>')
                        else:
                            result_phrases.append(phrase)
                    result = f"Rangt! Nafnliðirnir í setningunni eru: <span class='correct-phrases'>{', '.join(result_phrases)}</span>"
                else:
                    result = "Rangt! Setningin inniheldur engan nafnlið"

        return render_template('nafnliðir.html', sentence=sentence, result=result, correct=correct)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500

@app.route('/noun/<word>', methods=['GET'])
def noun_page(word):
    try:
        sentence = request.args.get('sentence')
        if not sentence:
            raise ValueError("No sentence provided")

        analysis = analyze_module.analyze_word(word, sentence)

        # Find the noun in the phrase
        noun = next((t['text'] for t in analysis['sentence_analysis'] if t['category'] == 'no'), word)
        return render_template('nafnliðir_details.html', analysis=analysis, sentence=sentence, noun=noun)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500

@app.route('/guess_noun', methods=['GET'])
def guess_noun():
    try:
        word = request.args.get('word')
        sentence = request.args.get('sentence')
        guess_type = request.args.get('type')
        guess_value = request.args.get('guess')

        if not word or not sentence or not guess_type or not guess_value:
            return jsonify({"correct": False})

        analysis = analyze_module.analyze_word(word, sentence)
        correct = analysis[guess_type] == guess_value

        return jsonify({"correct": correct})
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return jsonify({"correct": False}), 500


####### ATVIKSLIÐIR ########
@app.route('/atviksliðir', methods=['GET', 'POST'])
def atviksliðir():
    try:
        if request.method == 'GET':
            sentence = adv_module.get_random_sentence()
            result = None
            correct = False
        else:
            sentence = request.form.get('sentence')
            user_input = request.form.get('adv_phrases', '').strip()
            if user_input:
                user_adv_phrases = [phrase.strip().lower() for phrase in user_input.split(',')]
            else:
                user_adv_phrases = []
            correct_adv_phrases = [phrase.lower() for phrase in adv_module.get_adv_phrases(sentence)]

            if set(user_adv_phrases) == set(correct_adv_phrases):
                correct = True
                if correct_adv_phrases:
                    if len(correct_adv_phrases) > 1:
                        result = f"Rétt! Atviksliðirnir í setningunni eru: <span class='correct-phrases'>{', '.join(correct_adv_phrases)}</span>"
                    else:
                        result = f"Rétt! Atviksliðurinn í setningunni er: <span class='correct-phrases'>{', '.join(correct_adv_phrases)}</span>"
                else:
                    result = "Rétt! Setningin inniheldur engan atvikslið"
            else:
                correct = False
                if correct_adv_phrases:
                    if len(correct_adv_phrases) > 1:
                        result = f"Rangt! Atviksliðirnir í setningunni eru: <span class='correct-phrases'>{', '.join(correct_adv_phrases)}</span>"
                    else:
                        result = f"Rangt! Atviksliðurinn í setningunni eru: <span class='correct-phrases'>{', '.join(correct_adv_phrases)}</span>"
                else:
                    result = "Rangt! Setningin inniheldur engan atvikslið"

        return render_template('atviksliðir.html', sentence=sentence, result=result, correct=correct)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500

####### FORSETNINGARLIÐIR ########
@app.route('/forsetningarliðir', methods=['GET', 'POST'])
def forsetningarliðir():
    try:
        if request.method == 'GET':
            sentence = p_module.get_random_sentence()
            result = None
            correct = False
            return render_template('forsetningarliðir.html', sentence=sentence, result=result, correct=correct)
        else:
            sentence = request.form.get('sentence')
            user_input = request.form.get('p_phrases', '').strip()
            if user_input:
                user_p_phrases = [phrase.strip().lower() for phrase in user_input.split(',')]
            else:
                user_p_phrases = []
            correct_p_phrases = [phrase.lower() for phrase in p_module.get_p_phrases(sentence)]

            if set(user_p_phrases) == set(correct_p_phrases):
                correct = True
                if correct_p_phrases:
                    if len(correct_p_phrases) > 1:
                        result = result = f"""Rétt! Forsetningarliðirnir í setningunni eru: {', '.join([f'<a class="hoverable-word" href="/preposition/{phrase}?sentence={sentence}">{phrase}</a>' for phrase in correct_p_phrases])}"""
                    else:
                        result = f"""Rétt! Forsetningarliðurinn í setningunni er: <a class="hoverable-word" href="/preposition/{correct_p_phrases[0]}?sentence={sentence}">{correct_p_phrases[0]}</a>"""
                else:
                    result = "Rétt! Setningin inniheldur engan forsetningarlið"
            else:
                correct = False
                if correct_p_phrases:
                    if len(correct_p_phrases) > 1:
                        result = f"""Rangt! Forsetningarliðirnir í setningunni eru: {', '.join([f'<a class="hoverable-word" href="/preposition/{phrase}?sentence={sentence}">{phrase}</a>' for phrase in correct_p_phrases])}"""
                    else:
                        result = f"""Rangt! Forsetningarliðurinn í setningunni er: <a class="hoverable-word" href="/preposition/{correct_p_phrases[0]}?sentence={sentence}">{correct_p_phrases[0]}</a>"""
                else:
                    result = "Rangt! Setningin inniheldur engan forsetningarlið"

        return render_template('forsetningarliðir.html', sentence=sentence, result=result, correct=correct)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500
    
@app.route('/preposition/<word>', methods=['GET'])
def preposition_page(word): #for prepositions
    try:
        sentence = request.args.get('sentence')
        if not sentence:
            raise ValueError("No sentence provided")

        analysis = analyze_module.analyze_word(word, sentence)
        return render_template('forsetningarliðir_details.html', analysis=analysis, sentence=sentence)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500

@app.route('/guess_preposition', methods=['GET'])
def guess_preposition(): #for prepositions
    try:
        word = request.args.get('word')
        sentence = request.args.get('sentence')
        guess_type = request.args.get('type')
        guess_value = request.args.get('guess')

        if not word or not sentence or not guess_type or not guess_value:
            return jsonify({"correct": False})

        analysis = analyze_module.analyze_word(word.split()[0], sentence)
        correct = analysis[guess_type] == guess_value

        return jsonify({"correct": correct})
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return jsonify({"correct": False}), 500

####### SAGNLIÐIR ########
@app.route('/sagnliðir', methods=['GET', 'POST'])
def sagnliðir():
    try:
        if request.method == 'GET':
            sentence = v_module.get_random_sentence()
            result = None
            correct = False
        else:
            sentence = request.form.get('sentence')
            user_input = request.form.get('v_phrases', '').strip()
            if user_input:
                user_v_phrases = [phrase.strip().lower() for phrase in user_input.split(',')]
            else:
                user_v_phrases = []
            correct_v_phrases = [phrase.lower() for phrase in v_module.get_verb_phrases(sentence)]

            if set(user_v_phrases) == set(correct_v_phrases):
                correct = True
                if correct_v_phrases:
                    if len(correct_v_phrases) > 1:
                        result = f"""Rétt! Sagnliðirnir í setningunni eru: <span class='correct-phrases'>{', '.join([f'<a class="hoverable-word" href="/verb/{phrase}?sentence={sentence}">{phrase}</a>' for phrase in correct_v_phrases])}</span>"""
                    else:
                        result = f"""Rétt! Sagnliðurinn í setningunni er: <a class="hoverable-word" href="/verb/{correct_v_phrases[0]}?sentence={sentence}">{correct_v_phrases[0]}</a>"""
                else:
                    result = "Rétt! Setningin inniheldur engan sagnlið"
            else:
                correct = False
                if correct_v_phrases:
                    if len(correct_v_phrases) > 1:
                        result = f"""Rangt! Sagnliðirnir í setningunni eru: <span class='correct-phrases'>{', '.join([f'<a class="hoverable-word" href="/verb/{phrase}?sentence={sentence}">{phrase}</a>' for phrase in correct_v_phrases])}</span>"""
                    else:
                        result = f"""Rangt! Sagnliðurinn í setningunni er: <a class="hoverable-word" href="/verb/{correct_v_phrases[0]}?sentence={sentence}">{correct_v_phrases[0]}</a>"""
                else:
                    result = "Rangt! Setningin inniheldur engan sagnlið"

        return render_template('sagnliðir.html', sentence=sentence, result=result, correct=correct)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500
    
@app.route('/verb/<word>', methods=['GET'])
def verb_page(word):
    try:
        sentence = request.args.get('sentence')
        phrase = request.args.get('phrase')
        if not sentence:
            raise ValueError("No sentence provided")
        
        analysis = analyze_module.analyze_word(word, sentence)
        
        verb = word
        return render_template('sagnliðir_details.html', analysis=analysis, sentence=sentence, verb=verb, phrase=phrase)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500


@app.route('/guess_verb', methods=['GET'])
def guess_verb():
    try:
        word = request.args.get('word')
        sentence = request.args.get('sentence')
        guess_type = request.args.get('type')
        guess_value = request.args.get('guess')

        if not word or not sentence or not guess_type or not guess_value:
            return jsonify({"correct": False})

        analysis = analyze_module.analyze_word(word, sentence)
        correct = analysis[guess_type] == guess_value

        return jsonify({"correct": correct})
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return jsonify({"correct": False}), 500

####### LÝSINGARLIÐIR ########
@app.route('/lysingarliðir', methods=['GET', 'POST'])
def lysingarliðir():
    try:
        if request.method == 'GET':
            sentence = a_module.get_random_sentence()
            result = None
            correct = False
            return render_template('lysingarliðir.html', sentence=sentence, result=result, correct=correct)
        else:
            sentence = request.form.get('sentence')
            user_input = request.form.get('a_phrases', '').strip()
            if user_input:
                user_a_phrases = [phrase.strip().lower() for phrase in user_input.split(',')]
            else:
                user_a_phrases = []
            correct_a_phrases = [phrase.lower() for phrase in a_module.get_a_phrases(sentence)]

            if set(user_a_phrases) == set(correct_a_phrases):
                correct = True
                if correct_a_phrases:
                    if len(correct_a_phrases) > 1:
                        result = f"""Rétt! Lýsingarliðirnir í setningunni eru: {', '.join([f'<a class="hoverable-word" href="/word/{phrase}?sentence={sentence}">{phrase}</a>' for phrase in correct_a_phrases])}"""
                    else:
                        result = f"""Rétt! Lýsingarliðurinn í setningunni er: <a class="hoverable-word" href="/word/{correct_a_phrases[0]}?sentence={sentence}">{correct_a_phrases[0]}</a>"""
                else:
                    result = "Rétt! Setningin inniheldur engan lýsingarlið"
            else:
                correct = False
                if correct_a_phrases:
                    if len(correct_a_phrases) > 1:
                        result = f"""Rangt! Lýsingarliðirnir í setningunni eru: {', '.join([f'<a class="hoverable-word" href="/word/{phrase}?sentence={sentence}">{phrase}</a>' for phrase in correct_a_phrases])}"""
                    else:
                        result = f"""Rangt! Lýsingarliðurinn í setningunni er: <a class="hoverable-word" href="/word/{correct_a_phrases[0]}?sentence={sentence}">{correct_a_phrases[0]}</a>"""
                else:
                    result = "Rangt! Setningin inniheldur engan lýsingarlið"

            return render_template('lysingarliðir.html', sentence=sentence, result=result, correct=correct)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500

@app.route('/word/<word>', methods=['GET'])
def word_page(word): #for adjectives
    try:
        sentence = request.args.get('sentence')
        if not sentence:
            raise ValueError("No sentence provided")

        analysis = analyze_module.analyze_word(word, sentence)
        return render_template('lysingarliðir_details.html', analysis=analysis, sentence=sentence)
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500

@app.route('/guess', methods=['GET'])
def guess(): #for adjectives
    try:
        word = request.args.get('word')
        sentence = request.args.get('sentence')
        guess_type = request.args.get('type')
        guess_value = request.args.get('guess')

        if not word or not sentence or not guess_type or not guess_value:
            return jsonify({"correct": False})

        analysis = analyze_module.analyze_word(word.split()[-1], sentence)
        correct = analysis[guess_type] == guess_value

        return jsonify({"correct": correct})
    except Exception as e:
        logging.error("Error occurred", exc_info=True)
        return jsonify({"correct": False}), 500
    
if __name__ == "__main__":
    serve(app ,host="0.0.0.0", port=8000)