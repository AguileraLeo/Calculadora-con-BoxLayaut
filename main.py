from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


class CalculadoraScreen(Screen):

    def presionar_boton(self, boton):
        texto = boton.text

        if texto == "AC":
            self.ids.display.text = "0"

        elif texto == "C":
            if len(self.ids.display.text) > 1:
                self.ids.display.text = self.ids.display.text[:-1]
            else:
                self.ids.display.text = "0"

        elif texto == "Cambiar":
            self.manager.current = "formulario"

        elif texto == "=":
            self.calcular()

        elif texto == "%":
            try:
                valor = float(self.ids.display.text) / 100
                self.ids.display.text = str(int(valor)) if valor.is_integer() else str(valor)
            except Exception:
                self.ids.display.text = "ERROR"

        else:
            if self.ids.display.text == "0":
                self.ids.display.text = texto
            else:
                self.ids.display.text += texto

    def calcular(self):
        try:
            expresion = self.ids.display.text

            if "+" in expresion:
                numeros = expresion.split("+")
                resultado = float(numeros[0]) + float(numeros[1])

            elif "-" in expresion[1:]:
                numeros = expresion.split("-")
                resultado = float(numeros[0]) - float(numeros[1])

            elif "×" in expresion:
                numeros = expresion.split("×")
                resultado = float(numeros[0]) * float(numeros[1])

            elif "÷" in expresion:
                numeros = expresion.split("÷")
                if float(numeros[1]) == 0:
                    self.ids.display.text = "ERROR"
                    return
                resultado = float(numeros[0]) / float(numeros[1])

            else:
                resultado = float(expresion)

            if resultado.is_integer():
                self.ids.display.text = str(int(resultado))
            else:
                self.ids.display.text = str(resultado)

        except Exception:
            self.ids.display.text = "ERROR"


class FormularioScreen(Screen):

    def calcular_suma(self, boton):
        try:
            numero1 = float(self.ids.numero1.text)
            numero2 = float(self.ids.numero2.text)
            resultado = numero1 + numero2

            if resultado.is_integer():
                resultado = int(resultado)

            self.ids.resultado.text = f"Resultado: {resultado}"

        except Exception:
            self.ids.resultado.text = "Ingrese números válidos"

    def volver(self, boton):
        self.manager.current = "calculadora"


class CalculadoraApp(App):

    def build(self):
        manager = ScreenManager()
        manager.add_widget(CalculadoraScreen(name="calculadora"))
        manager.add_widget(FormularioScreen(name="formulario"))
        return manager


if __name__ == "__main__":
    CalculadoraApp().run()
