# Import flask
from flask import Flask, request, jsonify

# Import the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from uuid import uuid4

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys.json"

app = Flask(__name__)


@app.route('/syntax', methods=['GET'])
def test():
    data = request.args.to_dict()

    client = language.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(
        content=data["text"].lower(),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    # document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

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
    shapes = []

    shape = {
        'id': uuid4(),
        'relative_to': 'canvas'
    }
    for sentence in return_data:
        for item in sentence:
            if item["POS"] == "NOUN":
                if item["word"] in ["center", "left", "right"]:
                    shape["position"] = item["word"]
                if item["word"] in ["square", "circle", "triangle"]:
                    shape["type"] = item["word"]
                    shapes.append(shape)

                    shape = {
                        'id': uuid4(),
                        'relative_to': 'canvas'
                    }

    return jsonify(shapes)


if __name__ == '__main__':
    app.run(debug=True)
