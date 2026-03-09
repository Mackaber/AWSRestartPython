import json
import os
# JSON
# Try Except
# File Read
# Input

# Archivo de configuración en JSON config.json
# { users: ["Mackaber", "Ana", "Juan",...] }

# 1. Ver si el archivo existe, si no crearlo...

# 1.a Try Except
#try:
#    file = open("config.json", "r")
#except IOError:
#    file = open("config.json","w")
#    json_file = json.dumps({ "users": []})
#    file.write(json_file)

# 1.b Con os
files = os.listdir()

def write_file(content):
    file = open("config.json","w")
    json_file = json.dumps(content)
    file.write(json_file)

if "config.json" not in files:
    write_file({ "users": [] })

# 2.1 Cargar JSON del archivo en una variable
file = open("config.json","r")
json_file = file.read()
config = json.loads(json_file)

# 2.b
#config = json.load("config.json")

# 3. Pedir el nombre al usuario
user = input("Cual es su nombre?")

# 4. Si el usuario se encuentra en users, no hacer nada, si no agregarlo
if user not in config["users"]:
    config["users"].append(user)

# 5. Volver a escribir el archivo
write_file(config)