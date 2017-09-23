# Import flask
from flask import Flask, request, jsonify

# Import the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from uuid import uuid4

# Import wit and the associated API keys
from wit import Wit
from witkey import key

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"

app = Flask(__name__)


@app.route('/syntax', methods=['GET'])
def test():
    data = request.args.to_dict()

    # Initialize the clients
    google_client = language.LanguageServiceClient()
    wit_client = Wit(key)

    # Instantiates a plain text document.
    document = types.Document(
        content=data["text"].lower(),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    # document.type == enums.Document.Type.HTML
    tokens = google_client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    return_data = [[]]

    # Initialises x as an index
    x = 0

    for token in tokens:
        return_data[x].append({
            'word': str(token.text.content),
            'POS': pos_tag[token.part_of_speech.tag]
        })
        if token.text.content == ".":
            x += 1
            return_data.append([])

    # Now that we have the data, process it into something we can draw on the canvas
    return_entities = []

    for sentence in return_data:
        sentence_str = ""
        for item in sentence:
            sentence_str += item['word'] + " "

        print("sentence_str: " + sentence_str.strip("."))
        try:
            wit_response = wit_client.message(sentence_str.strip("."))
            entities = wit_response['entities']
        except:
            break
            
        entity = {'intent': entities['intent'][0]['value']}

        if entity['intent'] == "draw_shape":
            entity['type'] = entities['shape'][0]['value']
        elif entity['intent'] == "add_text":
            entity['text'] = entities['text'][0]['value'].strip('"').strip("'") # Get rid of quotes

        if 'origin' in entities:
            entity['origin'] = entities['origin'][0]['value']
        if 'direction' in entities:
            entity['direction'] = entities['direction'][0]['value']

        return_entities.append(entity)

    return jsonify(return_entities)


if __name__ == '__main__':
    app.run(debug=True)
