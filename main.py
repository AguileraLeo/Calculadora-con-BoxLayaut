from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


class CalculadoraScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contador_calculos = 0

    def presionar_boton(self, boton):
        texto = boton.text

        if texto == "C":
            self.ids.display.text = "0"

        elif texto == "=":
            self.calcular()

        elif texto == "Salir":
            self.salir_app()

        else:
            if self.ids.display.text in ("0", "ERROR"):
                self.ids.display.text = texto
            else:
                self.ids.display.text += texto

    def ir_a_formulario(self):
        self.manager.current = "formulario"

    def salir_app(self):
        App.get_running_app().stop()

    def calcular(self):
        if self.contador_calculos >= 5:
            self.manager.current = "premium"
            return

        try:
            expresion = self.ids.display.text
            expresion_eval = expresion.replace("×", "*").replace("÷", "/")
            
            resultado = eval(expresion_eval)

            if isinstance(resultado, float) and resultado.is_integer():
                self.ids.display.text = str(int(resultado))
            else:
                self.ids.display.text = str(round(resultado, 6))

            self.contador_calculos += 1
            restantes = 5 - self.contador_calculos

            if restantes > 0:
                self.ids.contador.text = f"FREE • {restantes} cálculos restantes"
            else:
                self.ids.contador.text = "FREE • LÍMITE ALCANZADO"

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


class PremiumScreen(Screen):

    def seleccionar_plan(self, plan):
        pantalla = self.manager.get_screen("confirmacion")
        pantalla.mostrar_plan(plan)
        self.manager.current = "confirmacion"

    def volver(self, boton):
        self.manager.current = "calculadora"


class ConfirmacionScreen(Screen):

    def mostrar_plan(self, plan):
        if plan == "Individual":
            precio = "$2.990 / mes"
            detalle = "Cálculos ilimitados"
        else:
            precio = "$5.990 / mes"
            detalle = "Hasta 5 calculadoras"

        self.ids.mensaje.text = (
            f"PLAN {plan.upper()}\n\n"
            f"{precio}\n"
            f"{detalle}\n\n"
            "¿Seguro que quieres pagar por\n"
            "una calculadora que suma 2 + 2?"
        )

    def suscribirse(self, boton):
        self.ids.mensaje.text = (
            "SUSCRIPCIÓN APROBADA\n\n"
            "El cobro fue 100% imaginario.\n\n"
            "Tu calculadora PRO ya está lista.\n\n"
            "Puedes volver a calcular."
        )

        calculadora = self.manager.get_screen("calculadora")
        calculadora.contador_calculos = 0
        calculadora.ids.contador.text = "FREE • 5 cálculos restantes"
        calculadora.ids.display.text = "0"

    def volver(self, boton):
        self.manager.current = "premium"


class CalculadoraApp(App):

    def build(self):
        manager = ScreenManager()
        manager.add_widget(CalculadoraScreen(name="calculadora"))
        manager.add_widget(FormularioScreen(name="formulario"))
        manager.add_widget(PremiumScreen(name="premium"))
        manager.add_widget(ConfirmacionScreen(name="confirmacion"))
        return manager


if __name__ == "__main__":
    CalculadoraApp().run()