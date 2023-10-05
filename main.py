from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.uix.popup import Popup
from kivy.clock import Clock
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
# Get data from file
filename = 'data_new.tsv'
tsvfile = open(filename, 'r', newline='')
reader = csv.reader(tsvfile, delimiter='\t')
data = list(reader)

# Get price list from Google Sheet:

# # Set up credentials
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name('pand-bar-61be1c8d5995.json', scope)
# client = gspread.authorize(creds)
# spreadsheet = client.open_by_key('1z-vlC8xdc2H1yxFrwqsZepCV4Y0Ir5pet0G97ltTP3U')
# worksheet = spreadsheet.worksheet('Sheet1')
# # Read the contents of the sheet
# data = worksheet.get_all_values()

# Define global vars
cart_contents = dict()         # {drink name:{amount:int, price:float}
colors = ['mustard', 'champagne', 'brown', 'lime', 'white', 'orange', 'blue']
codes = [
    [0.9, 0.6, 0.04, .9],  # mustard
    [1, 0.7, 0.7, 1],  # champagne
    [0.4, 0.16, 0.16,.9],  # brown
    [0.20, 0.80, 0.20,1],  # lime
    [1.00, 1.00, 1.00,1],  # white
    [1.0, 0.97, 0.0, 1],  # lemon
    [0.1, 0.1, 1.00,1]   # blue
]
codes = [[i*1.3 for i in j] for j in codes]
color_codes = {key:val for key, val in zip(colors, codes)}
cart_count = 0
daily_total = {}
total_daily = 0.0
last_item = Label(text='', size_hint_x=None)
last_item.bind(texture_size=last_item.setter('size'))
class MainApp(App):
    def build(self):
        main_layout =  BoxLayout(orientation='vertical', spacing=7)
        scroll_view = ScrollView()
        menu = BoxLayout(orientation = 'horizontal', size_hint_y=None, height='16mm', padding=(12,12,12,12), spacing=12)
        self.rows_layout = self.build_price_list(data)
        self.cart_btn = Button(text=f'Cart: {cart_count}', size_hint_y=None, height='12mm', background_color=[0,1.5,1.5,1.6])
        self.daily_btn = Button(text=f'Log', size_hint=(None,None), height='12mm', width='40mm', background_color=[1,1,1,1])
        self.search = TextInput(multiline=False)
        self.search.bind(text=self.calc)


        # self.last_item = Label(text=last_item)
        self.daily_btn.bind(on_press=self.daily_btn_press)
        self.cart_btn.bind(on_press=self.cart_btn_press)
        scroll_view.add_widget(self.rows_layout)
        menu.add_widget(last_item)
        menu.add_widget(self.cart_btn)
        menu.add_widget(self.search)
        menu.add_widget(self.daily_btn)
        main_layout.add_widget(menu)
        main_layout.add_widget(scroll_view)
        return main_layout
    

    def calc(self, instance, search_term):
        if not search_term:
            self.rows_layout = self.build_price_list(data)
        if search_term:
            f = filter(lambda x: search_term in x[0], data)

            self.rows_layout = self.build_price_list(f)

    

    def build_price_list(self, data):
        rows_layout = GridLayout(cols=1, spacing=6, size_hint_y=None)
        rows_layout.bind(minimum_height=rows_layout.setter('height'))
        for row in data:
            if len(row) >= 2:
                drink, price0, price1, price2, color = row[0], row[1], row[2], row[3], row[4]
                table_row = self.create_row(drink, price0, price1, price2, color)
                rows_layout.add_widget(table_row)
        return rows_layout
    
    def create_row(self, drink, price0, price1, price2, color):
        class DrinkBtn(Button):
            def __init__(self, name, price, **kwargs):
                self.name = name
                self.price = price
                super().__init__(**kwargs)
        row_layout = GridLayout(cols=4, spacing=10, size_hint_y=None, height='9mm')
        # TODO: convert below to loop in range of var data_width
        drink_price_button = DrinkBtn(text=drink + ' ' + price0 + '€',name=drink, price=float(price0.replace(',','.')), background_color=color_codes[color])
        drink_price_button.bind(on_press=self.on_press)
        row_layout.add_widget(drink_price_button)

        button_1 = DrinkBtn(text=price1+'€', size_hint_x=None, name=drink+' '+price1+'€', price=float(price1.replace(',','.')), background_color=color_codes[color])
        button_1.bind(width=lambda _, value: setattr(button_1, 'width', value))
        button_1.bind(on_press=self.on_press)
        row_layout.add_widget(button_1)

        button_2 = DrinkBtn(text=price2+'€', size_hint_x=None, name=drink+' '+price2+'€', price=float(price2.replace(',','.')), background_color=color_codes[color])
        button_2.bind(width=lambda _, value: setattr(button_2, 'width', value))
        button_2.bind(on_press=self.on_press)
        row_layout.add_widget(button_2)

        button_free = DrinkBtn(text='Free', size_hint_x=None, name=drink+' Free', price=0.0, background_color=color_codes[color])
        button_free.bind(width=lambda _, value: setattr(button_free, 'width', value))
        button_free.bind(on_press=self.on_press)
        row_layout.add_widget(button_free)
        return row_layout

    def on_press(self, instance):
        # Update cart dictionary, create new or update amount and price of existing entry
        global cart_count
        global last_item
        cart_contents.setdefault(instance.name, {'amount':0, 'price':0})
        cart_contents[instance.name]['amount']+=1
        cart_contents[instance.name]['price']+=instance.price
        cart_count = len(cart_contents)
        self.cart_btn.text = f'Cart: {cart_count}'
        last_item.text = str(instance.name)
        Clock.schedule_once(self.clear_message_text, 12)  # Schedule clear_message_text after N seconds
    def cart_btn_press(self, instance):
        # Creates Cart popup UI:
        total = 0.0
        Cart_ui = BoxLayout(orientation='vertical', spacing=5)
        scrollView = ScrollView(do_scroll_x=False, do_scroll_y=True)
        Total = Label(text=f'Total {total}€', size_hint_y=None, height='13mm')   # Add total
        cart_container = GridLayout(cols=1, spacing=6, size_hint_y=None, padding=[2,0,0,0])
        cart_container.bind(minimum_height=cart_container.setter('height'))
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
            global daily_total
            global total_daily
            nonlocal total
            if cart_contents:
                for name, j in cart_contents.items():
                    daily_total[name] = daily_total.setdefault(name, {'amount':0, 'price':0})
                    daily_total[name]['amount'] += j['amount']
                    daily_total[name]['price'] += j['price']
                total_daily+=total
                cart_contents = {}
            self.cart_btn.text = f'Cart: 0'
            self.cart.dismiss()
        def close_action(instance):
            self.cart.dismiss()
            
        if cart_contents:
            for name, val in cart_contents.items():
                # Format dictionary item row string
                name = name
                amount = str(val['amount'])
                price = str(val['price'])+'€'
                total += val['price']
                Total.text = f'Total {total}€'
                cart_container.add_widget(CartRow(name, amount, price))
            scrollView.add_widget(cart_container)
            Cart_ui.add_widget(scrollView)

        Cart_ui.add_widget(Total)
        Checkout = Button(text='Checkout',size_hint_y=1, background_color=[0,1.5,0,1])
        Checkout.bind(on_release=checkout_action)
        # Clear = Button(text='Clear', background_color=[2,0,0,1.6]) # for now disabled
        # Clear.bind(on_release=Clear_action)
        Close = Button(text='Close', background_color=[0,0,2,2])
        Close.bind(on_release = close_action)
        PP_Buttons = BoxLayout(orientation='horizontal',spacing=10, size_hint_y=None, height='9mm')
        # PP_Buttons.add_widget(Clear)
        PP_Buttons.add_widget(Checkout)
        PP_Buttons.add_widget(Close)
        Cart_ui.add_widget(PP_Buttons)
        self.cart = Popup(title='Cart', content=Cart_ui, size_hint=(0.7, None), height='120mm')
        self.cart.open()

    def daily_btn_press(self, instance):
        global daily_total
        global total_daily
        text_total = Label(text=f'Today\'s Total: {total_daily}€', size_hint_y=None, height='13mm')
        def close_popup(instance):
            instance.parent.parent.parent.parent.parent.dismiss()

        PP_content = BoxLayout(orientation='vertical')
        daily_total_popup = Popup(title='Today\'s total',  content=PP_content, size_hint=(0.7, None), height='120mm')
        log_scroll = ScrollView()
        rows_layout = GridLayout(cols=1, spacing=6, size_hint_y=None) # Holds rows of the daily log.
        rows_layout.bind(minimum_height=rows_layout.setter('height')) # Binds high
        # Defive a class for data row in daily log popup
        class CartRow(BoxLayout):
            def __init__(self, name, amount, price):
                self.name = Label(text=name, halign='left', valign='middle')
                self.name.bind(size=self.name.setter('text_size')) 
                self.amount = Label(text=str(amount), size_hint_x=0.1)
                self.price = Label(text=str(price)+'€', size_hint_x=0.3)
                super().__init__(orientation='horizontal', spacing=6, size_hint_y=None, height='9mm')
                self.add_widget(self.name)
                self.add_widget(self.amount)
                self.add_widget(self.price)

        for name, j in daily_total.items():
            # Create rows of daily log 
            row = CartRow(name, j['amount'], j['price'])
            rows_layout.add_widget(row) # add them to the layout

        log_scroll.add_widget(rows_layout)
        daily_total_popup.content.add_widget(log_scroll)
        daily_total_popup.content.add_widget(text_total)
        def submit_daily(instance):
            ''' Button to submit daily log to database and reset the daily log.'''
            global daily_total
            global total_daily
            nonlocal rows_layout
            nonlocal text_total
            if daily_total and rows_layout.children:
                daily_total = {}
                total_daily = 0.0
                rows_layout.clear_widgets()
                text_total.text = 'Today\'s total: 0.0'
            instance.parent.parent.parent.parent.dismiss()
        close_btn = Button(text="Close", size_hint=(1, None), height= "10mm",background_color=[0,0,2,2])
        submit_btn = Button(text="Submit", size_hint=(1, None), height= "10mm",background_color=[0,1.5,0,1])
        # submit_btn.bind(on_press = submit_daily)
        # create confirmatioin popup
        confirm_content = BoxLayout(orientation='horizontal', spacing=6)
        # Create the 'yes' button and bind it to the submit_daily function
        yes_button = Button(text='Yes', size_hint=(1, None), height= "10mm",background_color=[0,1.5,0,1])
        yes_button.bind(on_release=submit_daily)
        # Create the 'no' button and bind it to the popup.dismiss function
        no_button = Button(text='No', size_hint=(1, None), height= "10mm",background_color=[0,0,2,2])
        # Add the buttons to the BoxLayout
        confirm_content.add_widget(yes_button)
        confirm_content.add_widget(no_button)
        # Create the popup and set 'no' button to close the popup
        confirm_popup = Popup(title='Submit Daily?', content=confirm_content, size_hint=(None, None), size=(800, 300))
        no_button.bind(on_release=confirm_popup.dismiss)
        # Bind the submit button to open the confirm_popup
        submit_btn.bind(on_press=confirm_popup.open)
        # Create container for daily log popup
        PP_Buttons = BoxLayout(orientation='horizontal',spacing=10, size_hint_y=None, height='9mm')
        PP_Buttons.add_widget(close_btn)
        PP_Buttons.add_widget(submit_btn)
       
        close_btn.bind(on_release=close_popup)

        daily_total_popup.content.add_widget(PP_Buttons)


        daily_total_popup.open()

    def clear_message_text(self, dt):
        global last_item
        while len(last_item.text)>1:
            last_item.text = last_item.text[1:]
        last_item.text = ''

    # def clear_message_text(self, dt):
    #     def update_text(*args):
    #         if len(last_item.text) > 1:
    #             last_item.text = last_item.text[0:-1]
    #         else:
    #             last_item.text = ''
    #             return False  # stop scheduling
    #     Clock.schedule_interval(update_text, 0.02)


if __name__ == "__main__":
    MainApp().run()
