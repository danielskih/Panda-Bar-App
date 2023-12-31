from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


colors = ['mustard', 'champagne', 'brown', 'lime', 'white', 'lemon', 'blue']
codes = [
    [0.9, 0.6, 0.04, .9],  # mustard
    [1, 0.7, 0.7, 1],  # champagne
    [0.4, 0.16, 0.16,.9],  # brown
    [0.20, 0.80, 0.20,1],  # lime
    [1.00, 1.00, 1.00,1],  # white
    [1.0, 0.97, 0.0, 1],  # lemon
    [0.1, 0.1, 1.00,1]   # blue
]
codes = [[i*2 for i in j] for j in codes]
# codes = [[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]]

class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')
        for color, code in zip(colors, codes):
            main_layout.add_widget(Button(text = '', background_color = code))
        return main_layout
    
if __name__ == "__main__":
    MainApp().run()

