# Import flask
from flask import Flask, request, jsonify

# Import wit and the associated API keys
from wit import Wit
from witkey import key

client = Wit(key)

response = client.message('Add a square under the triangle')

print(response['entities'])
