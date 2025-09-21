import origin_os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

# Desactiva el "log" de bienvenida de Kivy
kivy.require('1.0.6')

# Define el tamaño inicial de la ventana (ancho, alto)
Window.size = (600, 800)

class OriginOSGUI(BoxLayout):
    def __init__(self, **kwargs):
        super(OriginOSGUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.entropic_input = TextInput(
            text='Pensamiento entrópico...',
            multiline=True,
            size_hint_y=0.1
        )
        self.add_widget(self.entropic_input)

        self.bifurcation_input = TextInput(
            text='Frase de bifurcación...',
            multiline=True,
            size_hint_y=0.1
        )
        self.add_widget(self.bifurcation_input)
        
        self.generate_button = Button(
            text='Generar Acto de Origen',
            size_hint=(0.7, 0.1)  # ¡Nuevo valor! Botón más ancho y con altura ajustada
        )
        self.generate_button.bind(on_press=self.on_generate_press)
        self.add_widget(self.generate_button)

        self.result_label = Label(
            text='Resultados...',
            size_hint_y=0.5,
            halign='left',
            valign='top'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.add_widget(self.result_label)
        
    def on_generate_press(self, instance):
        entropic_thought = self.entropic_input.text
        bifurcation_phrase = self.bifurcation_input.text
        
        result_output = origin_os.generate_act_of_origin_gui(entropic_thought, bifurcation_phrase)
        self.result_label.text = result_output


class OriginApp(App):
    def build(self):
        return OriginOSGUI()

if __name__ == '__main__':
    OriginApp().run()