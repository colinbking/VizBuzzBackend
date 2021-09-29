import spacy
#from spacytextblob.spacytextblob import SpacyTextBlob


def what_color_is_this_sentence(text):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe("spacytextblob")
    doc = nlp(text)
    return "green" if doc._.polarity > 0 else "red"
