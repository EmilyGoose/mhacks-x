# Import flask
from flask import Flask, request, jsonify, send_from_directory

# Import requests
import requests

# Import the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from uuid import uuid4

# Import wit and the associated API keys
from wit import Wit
from witkey import key

# Import the giphy API key
from giphykey import giphy_key

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "Hello, world!"


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

        try:
            wit_response = wit_client.message(sentence_str.strip("."))
            entities = wit_response['entities']
        except:
            break

        entity = {'intent': entities['intent'][0]['value']}

        if entity['intent'] == "draw_shape" and 'shape' in entities:
            entity['shape'] = entities['shape'][0]['value']
            entity['colour'] = entities['colour'][0]['value']
        elif entity['intent'] == "add_text" and 'text' in entities:
            entity['text'] = entities['text'][0]['value'].strip('"').strip("'") # Get rid of quotes
            entity['colour'] = entities['colour'][0]['value']
        elif entity['intent'] == "add_gif" and 'query' in entities:
            entity['query'] = entities['query'][0]['value']
        elif entity['intent'] == "draw_icon" and 'query' in entities:
            entity['query'] = entities['query'][0]['value']

        if 'origin' in entities:
            for item in entities['origin']:
                if item['value'] != "the":
                    entity['origin'] = item['value']
        if 'direction' in entities:
            entity['direction'] = entities['direction'][0]['value']
        if 'query' in entity:
            r = requests.get("https://api.giphy.com/v1/gifs/random" +
                             "?api_key=" + giphy_key +
                             "&tag=" + entity['query']
                             )
        if 'size' in entity:
            entity['size'] = entities['size'][0]['value']

        # Add giphy API
            entity['url'] = r.json()['data']['image_mp4_url']

        return_entities.append(entity)

    return jsonify(return_entities)

@app.route('/')
def send_index():
    return send_from_directory('dist', 'index.html')
app.route('/view')(send_index)
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('dist', path)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
