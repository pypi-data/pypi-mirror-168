from learntools.core import *
from learntools.core.problem import injected

class TypesChecker(CodingProblem):
    _vars = ['var1', 'var2', 'var3']

    _hints = ["Recuerda que el operador de asignación es `=`",
              "Los `float` son números reales (decimales) y los `int` enteros (-1, 0, 1, ...)",
              "Función para obtener tipo: `type(var)`\nFunción para mostrar por pantalla: `print(var)`",
              "Podemos definir `var3` como la suma de `var1` y `var2` usando el operador `+` y sus nombres"]
    _solution = CS("Una posible solución es\n"
                    "var1 = 4",
                    "var2 = 6.0",

                    "print(type(var1))",
                    "print(type(var2))",

                    "var3 = var1 + var2",
                    "print(type(var3))")

    def check(self, var1, var2, var3):
        
        if (type(var1) == int and type(var2) == float)&(var3 == var1 + var2):
            return
        assert (type(var1) == int and type(var2) == float), ("Revisa los tipos.")
        # return assert (isinstance(var1, int) and isinstance(var2, float)), ("Revisa los tipos. No están correctos")
        assert (var3 == var1 + var2), ("`var3` mal definida")
        # assert (var1 + var2 == var3), ("La suma no es correcta")

class DegreeRadiansCode(EqualityCheckProblem):
    pi = 22/7
    _vars = ['degree', 'radian']
    _expected = [180., 180. * (pi/180)]

    _hints = ["Usa la función `input` para introducir el dato",
              "Asegúrate de que conviertes el string del `input` a `float`",
              "El `check` sólo funciona para 180 grados",
              "Muestra el resultado por pantalla"]
    _solution = CS('degree = float(input("Input grados: "))',
                    'radian = degree*(pi/180)')

class Paralelogram(EqualityCheckProblem):
    _vars = ['base', 'height', 'area']
    _expected = [10., 15., 10. * 15.]

    _hints = ["Usa la función `input` para introducir el dato",
              "Asegúrate de que conviertes el string del `input` a `float`",
              "El check sólo funciona para base 10 y altura 15",
              "Muestra el resultado por pantalla"]
    _solution = CS("base = float(input('Length of base: '))",
                    "height = float(input('Measurement of height: '))",
                    "area = base * height",
                    "print('Area is: ', area)")

class ABCEquivalence(ThoughtExperiment):
    _hints = ["Revisa los operadores de comparación",
                "Las comparaciones devuelven `Bool` type",
                "Muestra los resultados por pantalla usando `print`"]

    _solution = CS("""
A = 4
B = "Text"
C = 4.1

print(A == B)
print(A != C)
print(A > C)
print(C <= A)
print(B != C)
""")


class InputBool1(ThoughtExperiment):
    _hints = ["Usa la función `input` para introducir el dato",
              "Asegúrate de que conviertes el string del `input` a `float`",
                "No es lo mismo `=` que `==`",
                "Las comparaciones devuelven `Bool` type",
                "Muestra los resultados por pantalla usando `print`"]

    _solution = CS("""
inp_1 = input("Input 1: ")
inp_2 = input("Input 2: ")
print(inp_1 == inp_2)
""")

class InputBool2(EqualityCheckProblem):
    _hints = ["Usa la función `input` para introducir el dato",
              "Trabajamos con strings en este ejercicio",
                "No es lo mismo `=` que `==`",
                "Las comparaciones devuelven `Bool` type",
                "Muestra los resultados por pantalla usando `print`"]
    _vars = ['inp_1', 'inp_2', 'inp_3', 'todos', 'dos']
    _expected = ['a', 'a', 'b', False, True]

    _solution = CS("""
inp_1 = input("Input 1: ")
inp_2 = input("Input 2: ")
inp_3 = input("Input 3: ")

todos = inp_1 == inp_2 and inp_1 == inp_3 and inp_2 == inp_3
print("Todos son iguales:", todos)

dos = inp_1 == inp_2 or inp_1 == inp_3 or inp_2 == inp_3
print("Todos son iguales:", dos)
""")

class InputBool3(ThoughtExperiment):
    _hints = ["Usa la función `input` para introducir el dato",
              "Convierte los inputs a `float`",
              "Define una variable intermedia",
                "No es lo mismo `=` que `==`",
                "Las comparaciones devuelven `Bool` type"]
    _solution = CS("""
in1 = input("Input 1: ")
in2 = input("Input 2: ")

suma = float(in1) + float(in2)

print("Es mayor que 10:", suma > 10)
print("Es menor que 10:", suma < 10)
print("Es igual que 10:", suma == 10)
""")

class BoolQuestions(ThoughtExperiment):
    _hints = ["`True` puede considerarse 1, `False` 0, `and` como producto y `or` suma",
              "Probar con código y comprobar",
              "1. `False`. Explicación: `True and True` -> `True` -> `True and False` -> `False`",
              "2. `False`. Explicación: `True or False` -> `True` -> `not ((True or False) and (True or False))` -> `not (True and True)` -> `not True` -> `False`",
              "3. `False`. Explicación: Cualquier cosa `and` `False` -> `False`",
              "4. `False`. Explicación: Cadena de `and` que contiene un 'not True' (`False`) es siempre `False`"]
    _solution = CS("1. False. Explicación: True and True -> True -> True and False -> False",
                    "2. False. Explicación: True or False -> True -> not ((True or False) and (True or False)) -> not (True and True) -> not True -> False",
                    "3. False. Explicación: Cualquier cosa and False -> False",
                    "4. False. Explicación: Cadena de and que contiene un not True (False) es siempre False"
            )

class StringMethods(ThoughtExperiment):
    _hints = ["Revisa los métodos para strings en https://www.w3schools.com/python/python_ref_string.asp",
              "Ejemplo:\n"
              """
              >>'palabra'.upper()
              >>'PALABRA'
              """,
              "Define la variable\n"
              """
              ej_10 = 'A quien madruga, dios le ayuda'
              """,
              "1. Mayúsculas\n"
              """
              ej_10.upper()
              """,
              "2. Minúsculas\n"
              """
              ej_10.lower()
              """,
              "3. Iniciales Mayúsculas\n"
              """
              ej_10.title()
              """,
              "4. Lista\n"
              """
              ej_10.split(' ')
              """,
              "5. Sustituye comas\n"
              """
              ej_10.replace(',', ';')
              """,
              "6. Elimina 'a'\n"
              """
              ej_10.replace('a', '')
              """]
              
    _solution = CS("""
    ej_10 = "A quien madruga, dios le ayuda"
    print(ej_10.upper())
    print(ej_10.lower())
    print(ej_10.title())
    print(ej_10.split(' '))
    print(ej_10.replace(',', ';'))
    print(ej_10.replace('a', ''))
    """
    )

class ListMethods(ThoughtExperiment):
    _hints = ["Revisa los métodos para listas en https://www.w3schools.com/python/python_ref_list.asp",
                "CUIDADO: Algunos métodos como `append` modifican la lista pero no devuelven output."
                "Por ello, si lo asignamos a una nueva variable va a estar vacía"
                """\n\nEjemplo:\n

                ls = [1, 2, 3]
                ls.append(4)
                >>ls
                >>[1, 2, 3, 4]

                ls2 = ls.append(4)
                >>ls2
                >>None

                """,
                "1. Define la lista\n"
                """
                list_11 = [1, 2, 3]
                """,
                "2. Añade y suma\n"
                """
                list_11.append(4)
                sum(list_11)
                """,
                "3. Elimina\n"
                """
                list_11.remove(1)
                """,
                "4. Añade en la posicion 3\n"
                """
                list_11.insert(2, 5)
                """,
                """
                5. Concatena\n
                list_11_2 = [6, 7, 8, 9]
                print(list_11 + list_11_2)
                """]
              
    _solution = CS("""
    list_11 = [1, 2, 3]
    list_11.append(4)
    print(sum(list_11))

    list_11.remove(1)
    print(list_11)

    list_11.insert(2, 5)
    print(list_11)

    list_11_2 = [6, 7, 8, 9]
    print(list_11 + list_11_2)
    """)

InputBool = MultipartProblem(InputBool1, InputBool2, InputBool3)

qvars = bind_exercises(globals(), [
                                    TypesChecker,
                                    DegreeRadiansCode,
                                    Paralelogram,
                                    ABCEquivalence,
                                    InputBool,
                                    BoolQuestions,
                                    StringMethods,
                                    ListMethods
                                    ],
                                    start=0,
                                    )
__all__ = list(qvars)
