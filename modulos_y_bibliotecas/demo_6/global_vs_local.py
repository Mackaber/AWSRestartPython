a = "Lo que sea"

def f():
    # global a
    a = "Otra cosa"
    print(a)

f()
print(a)