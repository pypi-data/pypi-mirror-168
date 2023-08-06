from learntools.core import *
from learntools.core.problem import injected

class EinsteinMessage(EqualityCheckProblem):
    _var = 'msg'
    _expected = """¿Por qué esta magnífica tecnología científica,\n\tque ahorra trabajo y nos hace la vida mas fácil,\n\t\tnos aporta tan poca felicidad?\n\t\t\tLa repuesta es está, simplemente: porque aún no hemos aprendido a usarla con tino.\n\"Albert Einstein\""""

    _hints = ["Los saltos de línea se escriben con \\n",
              "Usa \\t para tabular en lugar del tabulador",
              r"""Escapa las comillas del autor con \ """]
    _solution = CS('print("¿Por qué esta magnífica tecnología científica,\\n\\tque ahorra trabajo y nos hace la vida mas fácil,\\n\\t\\tnos aporta tan poca felicidad?\\n\\t\\t\\tLa repuesta es está, simplemente: porque aún no hemos aprendido a usarla con tino.\\n\\"Albert Einstein\\"")')

class PrintAddressVar(ThoughtExperiment):
    _hints = ["Asigna una variable `nom_calle` que sea string, `num_calle` que sea string o int, etc.",
                "Usa el método de concatenación para strings",
                "Convierte todo a string"]

    _solution = """Esta es una posible solución:
```python
nom_calle = "Castellana"
num_calle = 24
pobl = "Madrid"
cp = 26774
total = nom_calle + " " + str(num_calle) + " " + pobl + " " + str(cp)
print(total)
```
"""

class PrintAddressOther(ThoughtExperiment):
    _hint = "Hay varias formas de hacerlo: propiedades de concatenación de strings de `print`, método `format`, `fstrings`..."

    _solution = """Posibles soluciones:
```python
print(nom_calle, num_calle, pobl, cp)
print('Mi dirección es: {} {} {} {}'.format(nom_calle, num_calle, pobl, cp))
print(f'Mi dirección es: {nom_calle} {num_calle} {pobl} {cp}')
```
"""

PrintAddress = MultipartProblem(PrintAddressVar, PrintAddressOther)

class SyntaxQuestion(ThoughtExperiment):
    _hints = ["Comprueba una por una e intenta interpretar los errores", 
                "Revisa la convención de nombres para variables en python"]

    _solution = """Esta es una posible solución:\n
                    1. Esta bien\n
                    2. Falta una comilla\n
                    3. No puedo usar True\n
                    4. Espacios en las variables no puedo\n
                    5. Esta bien\n
                    6. Palabra reservada\n
                    7. No puedo poner numeros delante\n
                    8. Esta bien\n
                """

class CelsiusFahrenheitCode(EqualityCheckProblem):
    _vars = ['temp_c', 'temp_f']
    _expected = [100., (100. * 9/5) + 32]

    _hints = ["Usa la función `input` para introducir el dato",
              "Asegúrate de que conviertes el strin del `input` a número",
              "El check sólo funciona para 100ºC",
              "Muestra el resultado por pantalla"]
    _solution = CS('temp_c = float(input("Introduzca una temperatura en ºC"))',
                    'temp_f = (temp_c * 9/5) + 32')

class CelsiusFahrenheitComments(ThoughtExperiment):
    _hint = "Describe la tarea que realiza y no el código usado"
    _solution = """
                Calculadora de grados Fahrenheit

```python
C = input('Introduzca grados celsius: ') # Input del usuario

# Hay que covertir los tipos para que no haya problemas
F = 32 + float(C) * float(9/5)

print("El equivalente en grados Fahrenheit es", F)
```
    """

CelsiusFahrenheit = MultipartProblem(CelsiusFahrenheitCode, CelsiusFahrenheitComments)

qvars = bind_exercises(globals(), [
                                    EinsteinMessage,
                                    PrintAddress,
                                    SyntaxQuestion,
                                    CelsiusFahrenheit
                                    ],
                                    start=0,
                                    )
__all__ = list(qvars)
