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



    last_refs = {}

    for sentence in return_data:

        # New index and new shape
        index = 0
        shape = {
            'id': uuid4(),
            'relative_to': 'canvas'
        }

        while index < len(sentence):
            item = sentence[index]
            if item["word"] == "the":
                if sentence[index+1]["word"] in last_refs:
                    shape['relative_to'] = last_refs[sentence[index+1]["word"]][-1]
                elif sentence[index+1]["word"] in ["left", "center", "middle", "right", "top"]:
                    shape['direction'] = sentence[index+1]['word']

                index += 1

            if item['word'] in ["an", "a"]:
                if sentence[index + 1]['POS'] == "NOUN":
                    item = sentence[index + 1]
                    shape['type'] = item['word']
                    if item['word'] in last_refs:
                        last_refs[item['word']].append(shape['id'])
                    else:
                        last_refs[item['word']] = [shape['id']]
                    index += 1

            index += 1

        if 'type' in shape:
            shapes.append(shape)

        # for item in sentence:
        #     if item["POS"] == "NOUN":
        #         if item["word"] in ["center", "left", "right"]:
        #             shape["position"] = item["word"]
        #         if item["word"] in ["square", "circle", "triangle"]:
        #             shape["type"] = item["word"]
        #             shapes.append(shape)
        #
        #             shape = {
        #                 'id': uuid4(),
        #                 'relative_to': 'canvas'
        #             }

    return jsonify(shapes)


if __name__ == '__main__':
    app.run(debug=True)
