from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import csv
 
# Get data from file
filename = 'data_new.tsv'

tsvfile = open(filename, 'r', newline='')
reader = csv.reader(tsvfile, delimiter='\t')
data = list(reader)
cart_contents = dict()         # {drink name:{amount:int, price:float}
cart_count = 0
class MainApp(App):
    def build(self):
        main_layout =  BoxLayout(orientation='vertical',spacing=15)
        child_layout1 = ScrollView()
        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        data_width = len(data[0])
        for row in data:
            if len(row) >= 2:
                drink, price0, price1, price2 = row[0], row[1], row[2], row[3]
                table_row = self.create_row(drink, price0, price1, price2)
                grid_layout.add_widget(table_row)
        self.cart_btn = Button(text=f'Cart: {cart_count}', size_hint_y=None, height='10mm', background_color=[0,1.5,1.5,1.6])
        self.cart_btn.bind(on_press=self.cart_btn_press)
        child_layout1.add_widget(grid_layout)
        main_layout.add_widget(self.cart_btn)
        main_layout.add_widget(child_layout1)
        return main_layout
    def create_row(self, drink, price0, price1, price2):
        class DrinkBtn(Button):
            def __init__(self, name, price, **kwargs):
                self.name = name
                self.price = price
                super().__init__(**kwargs)
        row_layout = GridLayout(cols=4, spacing=10, size_hint_y=None, height='9mm')
        # TODO: convert below to loop in range of var data_width
        drink_price_button = DrinkBtn(text=drink + ' ' + price0 + '€',name=drink, price=float(price0.replace(',','.')))
        drink_price_button.bind(on_press=self.on_press)
        row_layout.add_widget(drink_price_button)

        button_1 = DrinkBtn(text=price1+'€', size_hint_x=None, name=drink+' '+price1+'€', price=float(price1.replace(',','.')))
        button_1.bind(width=lambda _, value: setattr(button_1, 'width', value))
        button_1.bind(on_press=self.on_press)
        row_layout.add_widget(button_1)

        button_2 = DrinkBtn(text=price2+'€', size_hint_x=None, name=drink+' '+price2+'€', price=float(price2.replace(',','.')))
        button_2.bind(width=lambda _, value: setattr(button_2, 'width', value))
        button_2.bind(on_press=self.on_press)
        row_layout.add_widget(button_2)

        button_free = DrinkBtn(text='Free', size_hint_x=None, name=drink+' Free', price=0.0)
        button_free.bind(width=lambda _, value: setattr(button_free, 'width', value))
        button_free.bind(on_press=self.on_press)
        row_layout.add_widget(button_free)
    
        return row_layout
        # class PlusMinusBtn(Button):
            # pass
    def on_press(self, instance):
        # Update cart dictionary, create new or update amount and price of existing entry
        global cart_count
        cart_contents.setdefault(instance.name, {'amount':0, 'price':0})
        cart_contents[instance.name]['amount']+=1
        cart_contents[instance.name]['price']+=instance.price
        cart_count = len(cart_contents)
        self.cart_btn.text = f'Cart: {cart_count}'

    def cart_btn_press(self, instance):
        # Creates Cart popup UI:
        total = 0.0
        Cart_ui = BoxLayout(orientation='vertical', spacing=5)
        Total = Label(text=f'Total {total}€')   # Add total
        cart_container = BoxLayout(orientation='vertical', padding=[2,0,0,0])
        class CartRow(BoxLayout):
            def __init__(self, name, amount, price):
                self.name = Label(text=name, halign='left', valign='middle')
                self.name.bind(size=self.name.setter('text_size')) 
                self.amount = Label(text=amount, size_hint_x=0.1)
                self.price = Label(text=price, size_hint_x=0.3)
                self.unit_price = float(price.replace('€', '')) / float(amount)
                # Declare buttons
                self.minus_btn = Button(text='-', size_hint_x=None, width='10mm')
                self.plus_btn = Button(text='+', size_hint_x=None, width='10mm')
                # Bind buttons
                self.minus_btn.bind(on_press=self.substract)
                self.plus_btn.bind(on_press=self.add)
                super().__init__(orientation='horizontal', spacing=5, size_hint_y=None, height='9mm')
                self.add_widget(self.name)
                self.add_widget(self.amount)
                self.add_widget(self.price)
                self.add_widget(self.minus_btn)
                self.add_widget(self.plus_btn)
            # TODO add class method for the + - buttons to change amount and price both in UI ancart_contents dict
            def update_cart(self, key, amount, price):
                if amount == 0:
                    del cart_contents[key]
                else:
                    cart_contents[key] = {'amount': amount, 'price': price}
            def add(self, instance):
                nonlocal total
                new_amount = int(self.amount.text) + 1
                self.amount.text = str(new_amount)
                new_price = float(self.price.text.replace('€','')) + self.unit_price
                self.price.text = str(new_price)+'€'
                self.update_cart(self.name.text, new_amount, new_price)
                total += self.unit_price
                Total.text = f'Total {total}€'
            def substract(self, instance):
                nonlocal total
                if int(self.amount.text) >= 1:
                    new_amount = int(self.amount.text) - 1
                    self.amount.text = str(new_amount)
                    new_price = float(self.price.text.replace('€','')) - self.unit_price
                    self.price.text = str(new_price)+'€'
                    self.update_cart(self.name.text, new_amount, new_price)
                    total -= self.unit_price
                    Total.text = f'Total {total}€'
        def Clear_action(instance):
            global cart_contents
            if cart_contents and cart_container is not None:
                cart_contents = {}
                cart_container.clear_widgets()
                self.cart_btn.text = f'Cart: 0'
                nonlocal total
                total = 0.0
                Total.text = 'Total 0.0€'
        def checkout_action(instance):
            global cart_contents
            cart_contents = {}
            self.cart.dismiss()
            self.cart_btn.text = f'Cart: 0'
        def close_action(instance):
            self.cart.dismiss()
        if cart_contents:
            for name, val in cart_contents.items():
                # Format dictioinary item row string
                name = name
                amount = str(val['amount'])
                price = str(val['price'])+'€'
                total += val['price']
                Total.text = f'Total {total}€'
                cart_container.add_widget(CartRow(name, amount, price))
            Cart_ui.add_widget(cart_container)
        Cart_ui.add_widget(Total)
        Checkout = Button(text='Checkout',size_hint_y=None, height='11mm', background_color=[0,1.5,0,1])
        Checkout.bind(on_release=checkout_action)
        Clear = Button(text='Clear', background_color=[2,0,0,1.6])
        Clear.bind(on_release=Clear_action)
        Close = Button(text='Close', background_color=[0,0,2,2])
        Close.bind(on_release = close_action)
        PP_Buttons = BoxLayout(orientation='horizontal',spacing=10, size_hint_y=None, height='9mm')
        PP_Buttons.add_widget(Clear)
        PP_Buttons.add_widget(Close)
        Cart_ui.add_widget(PP_Buttons)
        Cart_ui.add_widget(Checkout)
        # TODO: make
        self.cart = Popup(title='Cart', content=Cart_ui, size_hint=(0.7, None), height='120mm')
        self.cart.open()
if __name__ == "__main__":
    MainApp().run()
