from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class MyKivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # icon = Image(source='shopping-cart.png', size=(128, 128))  # Replace 'icon.png' with the path to your PNG icon
        # button = Button(text='Click Me', size_hint=(.5, .5), padding=(0, 0), pos_hint={'center_x':.4, 'center_y':.5})
        # button.add_widget(icon)
        
        # layout.add_widget(button)
        button = Button(text='Click Me', size_hint=(1, .5), pos_hint={'center_x':.5, 'center_y':.5}, background_normal='shopping-cart.png' )
        layout.add_widget(button)

        return layout

if __name__ == '__main__':
    MyKivyApp().run()

# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.lang import Builder

# Builder.load_string("""
# <ButtonsApp>:
#     orientation: "vertical"
#     Button:
#         text: "B1"
#         Image:
#             source: 'shopping-cart.png'
#             y: self.parent.y + self.parent.height - 200
#             x: self.parent.x + 10
#     Label:
#         text: "A label"
# """)

# class ButtonsApp(App, BoxLayout):
#     def build(self):
#         return self

# if __name__ == "__main__":
#     ButtonsApp().run()



