import requests
import os
import json
import hashlib
import numpy as np


def save_json(file_name, json_dict):
    with open(file_name+".json", "w") as file:
        json.dump(json_dict, file)

## reading the token
with open("token", "r") as file:
    token = file.read()

## Getting the json
response = requests.get("https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token="+token)
json_response = response.json()

## Saving json to a file
save_json("answer", json_response)
print(json_response["cifrado"])

## Creating a array of ascii alphabet
alph = np.arange(97, 123).tolist()
for i, num in enumerate(alph[len(alph)-1-json_response['numero_casas'] : len(alph)-1]):
    alph.insert(i,num)
print(alph)

## Decrypting the message
resume = ""
for letter in json_response["cifrado"]:
    if letter == ".":
        resume = resume + "."
    elif letter.isspace():
        resume = resume + " "
    else:
        if ord(letter) - 97 - json_response['numero_casas'] < 0:
            resume = resume + chr(alph[ord(letter) - 97 - json_response['numero_casas']])
        else: 
            resume = resume + (chr(ord(letter) - json_response['numero_casas']))

print(resume)

## Saving decrypeted message to the json file
json_response["decifrado"] = resume
save_json("answer", json_response)

## Encrypting message with SHA1 and writing into json file
sha1 = hashlib.sha1()
sha1.update(b"charles leadbeater")
print("Hash: ",sha1.digest())
json_response["resumo_criptografico"] = hashlib.sha1(json_response["decifrado"].encode()).hexdigest()
print(json_response["resumo_criptografico"])
save_json("answer", json_response)

## Sending file
json_file = {"answer" : open("answer.json", "rb")}
response = requests.post("https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token="+token, files=json_file)
print(response.text)
print(response.status_code)