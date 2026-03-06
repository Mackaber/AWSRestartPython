def divide_five_by(number):
    try:
        value = 5 / number
    except ZeroDivisionError:
        print("Error: No se puede dividir por cero.")
        value = 1
    finally:
        print("Esto siempre se ejecuta, sin importar si hubo un error o no.")
    return value

print(divide_five_by(2))
print(divide_five_by(0))