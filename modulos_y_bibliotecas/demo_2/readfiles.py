print("Here is my diary: \n")
f1 = open("files/diary.txt", "r")
print(f1.read())
f1.close()

print("\nNow let's create another diary !\n")
f2 = open("files/diary2.txt", "w")
# Esto sobreescribe el archivo
# open("files/diary2.txt", "a") # Esto añade al final del archivo
f2.write("\nWriting in my diary file !")
f2.close()


# Leer y añadir al mismo tiempo
print("\nNow let's read and write in the same file !\n")
with open("files/diary3.txt", "a+") as f3:
    f3.seek(0)
    print(f3.read())
    f3.write("\nWriting in my diary file again !")
