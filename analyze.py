from reynir import Greynir

def get_gender(variants):
    genders = ["kk", "kvk", "hk"]
    for variant in variants:
        if variant in genders:
            return variant
    return ""

def get_number(variants):
    numbers = ["et", "ft"]
    for variant in variants:
        if variant in numbers:
            return variant
    return ""

def get_case(variants):
    cases = ["nf", "þf", "þgf", "ef"]
    for variant in variants:
        if variant in cases:
            return variant
    return ""

def get_episode(variants):
    cases = ["nh", "vh", "bh", "fh", "lh", "lhþt"]
    for variant in variants:
        if variant in cases:
            return variant
    return ""

def get_person(variants):
    cases = ["p1", "p2", "p3"]
    for variant in variants:
        if variant in cases:
            return variant
    return ""

def get_tense(variants):
    cases = ["nt", "þt"]
    for variant in variants:
        if variant in cases:
            return variant
    return ""

def get_level(variants):
    levels = {"esb": "esb", "mst": "mst", "evb": "esb"}
    for variant in variants:
        if variant in levels:
            return levels[variant]
    return "frumstig"

def get_voice(variants):
    cases = {"mm": "mm", "gm": "gm"}
    for variant in variants:
        if variant in cases:
            return variant
    return "þolmynd"

def get_inflection(variants):
    inflections = ["vb", "sb"]
    for variant in variants:
        if variant in inflections:
            return variant
    return ""

def get_article(variants):
    articles = {"gr":"gr"}
    for variant in variants:
        if variant in articles:
            return variant
    return "ngr"

def get_sagnbot(variants):
    sagnbot = {"sagnb"}
    for variant in variants:
        if variant in sagnbot:
            return "sagnb"
    return ""

def analyze_word(word, sentence):
    g = Greynir()
    parsed_sentence = g.parse_single(sentence)
    
    sentence_analysis = []
    for t in parsed_sentence.terminals:
        sentence_analysis.append({
            "text": t.text,
            "lemma": t.lemma,
            "category": t.category,
            "variants": t.variants
        })
        if t.text == word:
            gender = get_gender(t.variants)
            number = get_number(t.variants)
            case = get_case(t.variants)
            voice = get_voice(t.variants)
            episode = get_episode(t.variants)
            person = get_person(t.variants)
            level = get_level(t.variants)
            tense = get_tense(t.variants)
            inflection = get_inflection(t.variants)
            article = get_article(t.variants)
            sagnbot = get_sagnbot(t.variants)
            return {
                "word": t.text,
                "gender": gender,
                "number": number,
                "case": case,
                "voice": voice,
                "episode": episode,
                "person": person,
                "level": level,
                "tense": tense,
                "inflection": inflection,
                "article": article,
                "sagnbot": sagnbot,
                "sentence_analysis": sentence_analysis
            }
    return {
        "word": word,
        "gender": "",
        "number": "",
        "case": "",
        "voice": "þolmynd",
        "episode": "",
        "person": "",
        "level": "frumstig",
        "tense": "",
        "inflection": "",
        "article": "ngr",
        "sagnbot":"",
        "sentence_analysis": sentence_analysis
    }

sentence = "segir börnunum að forðast ókunnuga"
g = Greynir()
parsed_sentence = g.parse_single(sentence)
for t in parsed_sentence.terminals:
    print(t.variants)