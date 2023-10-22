from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from functools import partial

import pymysql


conn = pymysql.connect(host='localhost', user='root', password='123456')
csr = conn.cursor()


def sql_command(query, type=None):
    csr.execute(query)
    if type == 'mod':
        conn.commit()


def unpack_field_tuple(tuple):
    final_tuple = ()
    for i in tuple:
        for j in i:
            final_tuple += (j,)
    return final_tuple


def unpack_tuple(tuple, index):
    final_tuple = ()
    if tuple:
        for i in tuple:
            final_tuple += (i[index],)
    return final_tuple


def modify_path(path):
    new_path = ''
    for i in path:
        if i == '\\':
            new_path += '\\\\'
        else:
            new_path += i
    return new_path


try:
    sql_command('create database a')
except:
    pass

sql_command('use a')

try:
    sql_command('create table user(userid int, username varchar(50), userpassword varchar(50), address varchar(100), mobileno varchar(20))')
except:
    pass

try:
    sql_command('create table items(itemid int, itemname varchar(50), image varchar(100), price varchar(50), details varchar(500), tags varchar(50), sellerid int, issold char(1))')
except:
    pass


# database=a
# table=user(userid int, username varchar(50), userpassword varchar(50))


class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.box_layout_outer = BoxLayout(orientation='vertical')

        # welcome
        self.title_label = Label(text='E-Commerce App')

        # username
        self.box_layout_inner_1 = BoxLayout(padding=20)
        self.username_label = Label(text='Username:')
        self.username_text_input = TextInput()
        self.box_layout_inner_1.add_widget(self.username_label)
        self.box_layout_inner_1.add_widget(self.username_text_input)

        # password
        self.box_layout_inner_2 = BoxLayout(padding=20)
        self.password_label = Label(text='Password:')
        self.password_text_input = TextInput()
        self.box_layout_inner_2.add_widget(self.password_label)
        self.box_layout_inner_2.add_widget(self.password_text_input)

        # sign up
        self.sign_up_button = Button(text='New user? Sign up', on_release=self.sign_up_button_clicked, size_hint=(0.5, 0.3), pos_hint={'center_x': 0.5})

        # submit
        self.sign_in_button = Button(text='Sign In', on_release=self.sign_in_button_clicked, size_hint=(0.6, 0.7), pos_hint={'center_x': 0.5})

        self.box_layout_outer.add_widget(self.title_label)
        self.box_layout_outer.add_widget(self.sign_up_button)
        self.box_layout_outer.add_widget(self.box_layout_inner_1)
        self.box_layout_outer.add_widget(self.box_layout_inner_2)
        self.box_layout_outer.add_widget(self.sign_in_button)

        self.add_widget(self.box_layout_outer)

    def sign_in_button_clicked(self, obj):
        username_text = self.username_text_input.text
        userpassword_text = self.password_text_input.text

        sql_command('select * from user')
        data = csr.fetchall()
        userid_tuple = unpack_tuple(data, 0)
        username_tuple = unpack_tuple(data, 1)
        password_tuple = unpack_tuple(data, 2)

        if username_text == '' or userpassword_text == '':
            self.popup_window('invalid')
        elif len(username_text) > 50 or len(userpassword_text) > 50:
            self.popup_window('greater')
        elif username_text not in username_tuple:
            self.popup_window('wrong')
        elif username_text in username_tuple:
            username_text_pos = username_tuple.index(username_text)
            if userpassword_text == password_tuple[username_text_pos]:
                screen_manager.current = 'items'
                items_screen.userid = userid_tuple[username_tuple.index(username_text)]
            else:
                self.popup_window('wrong')

    def sign_up_button_clicked(self, obj):
        self.sign_up_popup = Popup(title='Sign Up', size_hint=(0.8, 0.8))

        self.sign_up_box_layout_outer = BoxLayout(orientation='vertical')

        self.sign_up_box_layout_inner_1 = BoxLayout()
        self.sign_up_username_label = Label(text='Username:')
        self.sign_up_username_text_input = TextInput()
        self.sign_up_box_layout_inner_1.add_widget(self.sign_up_username_label)
        self.sign_up_box_layout_inner_1.add_widget(self.sign_up_username_text_input)

        self.sign_up_box_layout_inner_2 = BoxLayout()
        self.sign_up_userpassword_label = Label(text='Password:')
        self.sign_up_userpassword_text_input = TextInput()
        self.sign_up_box_layout_inner_2.add_widget(self.sign_up_userpassword_label)
        self.sign_up_box_layout_inner_2.add_widget(self.sign_up_userpassword_text_input)

        self.sign_up_box_layout_inner_3 = BoxLayout()
        self.sign_up_address_label = Label(text='Address:')
        self.sign_up_address_text_input = TextInput()
        self.sign_up_box_layout_inner_3.add_widget(self.sign_up_address_label)
        self.sign_up_box_layout_inner_3.add_widget(self.sign_up_address_text_input)

        self.sign_up_box_layout_inner_4 = BoxLayout()
        self.sign_up_mobile_no_label = Label(text='Mobile number:')
        self.sign_up_mobile_no_text_input = TextInput()
        self.sign_up_box_layout_inner_4.add_widget(self.sign_up_mobile_no_label)
        self.sign_up_box_layout_inner_4.add_widget(self.sign_up_mobile_no_text_input)

        self.sign_up_sign_up_button = Button(text='Sign Up', on_release=self.sign_up_button_2_clicked)

        self.sign_up_box_layout_outer.add_widget(self.sign_up_box_layout_inner_1)
        self.sign_up_box_layout_outer.add_widget(self.sign_up_box_layout_inner_2)
        self.sign_up_box_layout_outer.add_widget(self.sign_up_box_layout_inner_3)
        self.sign_up_box_layout_outer.add_widget(self.sign_up_box_layout_inner_4)
        self.sign_up_box_layout_outer.add_widget(self.sign_up_sign_up_button)

        self.sign_up_popup.add_widget(self.sign_up_box_layout_outer)

        self.sign_up_popup.open()

    def sign_up_button_2_clicked(self, obj):
        username_text = self.sign_up_username_text_input.text
        userpassword_text = self.sign_up_userpassword_text_input.text
        address_text = self.sign_up_address_text_input.text
        mobile_no_text = self.sign_up_mobile_no_text_input.text

        sql_command('select * from user')
        data = csr.fetchall()
        userid_tuple = unpack_tuple(data, 0)
        username_tuple = unpack_tuple(data, 1)
        userpassword_tuple = unpack_tuple(data, 2)
        address_tuple = unpack_tuple(data, 3)
        mobileno_tuple = unpack_tuple(data, 4)
        if userid_tuple:
            last_id = userid_tuple[-1]
        else:
            last_id = 0

        if username_text == '' or userpassword_text == '' or address_text == '' or mobile_no_text == '':
            self.popup_window('invalid')
        elif username_text in username_tuple:
            self.popup_window('exists')
        else:
            sql_command("insert into user values({}, '{}', '{}', '{}', {})".format(last_id + 1, username_text, userpassword_text, address_text, mobile_no_text), 'mod')
            screen_manager.current = 'items'
            items_screen.userid = last_id + 1
        self.sign_up_popup.dismiss()

    def popup_window(self, type):
        popup = Popup(title='Error', size_hint=(0.6, 0.3))
        if type == 'invalid':
            error_label = Label(text='Enter a valid username or password or address or mobile number')
        elif type == 'greater':
            error_label = Label(text='Username or password should not exceed 50 characters')
        elif type == 'wrong':
            error_label = Label(text='Wrong username or password')
        elif type == 'exists':
            error_label = Label(text='Username already exists')
        popup.add_widget(error_label)
        popup.open()


class ItemsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.userid = None
        # Clock.schedule_interval(self.get_username_password, 1)

        # graphics
        self.box_layout_outer = BoxLayout(orientation='vertical')

        # top bar
        self.box_layout_inner = BoxLayout()

        self.newitem_button = Button(text='+ New item', on_release=self.newitem_button_clicked)
        self.sign_out_button = Button(text='Sign out', on_release=self.sign_out_button_clicked)
        self.search_text_input = TextInput()
        self.search_button = Button(text='Search', on_release=self.search_button_clicked)
        self.refresh_button = Button(text='Refresh', on_release=self.refresh_button_clicked)

        self.box_layout_inner.add_widget(self.newitem_button)
        self.box_layout_inner.add_widget(self.sign_out_button)
        self.box_layout_inner.add_widget(self.search_text_input)
        self.box_layout_inner.add_widget(self.search_button)
        self.box_layout_inner.add_widget(self.refresh_button)

        # scroll
        self.scroll_layout = ScrollView()
        self.grid_layout = GridLayout(cols=1, size_hint_y=None)

        self.scroll_layout.add_widget(self.grid_layout)

        self.refresh_items('True')

        self.box_layout_outer.add_widget(self.box_layout_inner)
        self.box_layout_outer.add_widget(self.scroll_layout)

        self.add_widget(self.box_layout_outer)

    def newitem_button_clicked(self, obj):
        screen_manager.current = 'newitem'

    def sign_out_button_clicked(self, obj):
        screen_manager.current = 'login'
        login_screen.username_text_input.text = ''
        login_screen.password_text_input.text = ''
        self.userid = None

    def search_button_clicked(self, obj):
        self.search_text = self.search_text_input.text
        self.refresh_items("self.search_text in i[1] or self.search_text in i[3] or self.search_text in i[5]")

    def refresh_button_clicked(self, obj):
        self.refresh_items('True')

    def refresh_items(self, condition):
        self.scroll_layout.size_hint_y = 3
        self.scroll_layout.remove_widget(self.grid_layout)
        self.grid_layout = GridLayout(cols=1, size_hint_y=None, height=100)
        self.scroll_layout.add_widget(self.grid_layout)
        sql_command('select * from items')
        self.items = csr.fetchall()

        self.grid_layout.clear_widgets()
        for i in self.items:
            box_scroll = ItemBox(i)
            if i[7] == 'n' and eval(condition):
                self.grid_layout.add_widget(box_scroll)
                self.grid_layout.height += box_scroll.height

        # self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))


class ItemBox(BoxLayout):
    def __init__(self, details, **kw):
        super().__init__(**kw)
        image = details[2]
        # data = io.BytesIO(image)
        # data.seek(0)

        self.image_scroll = Image(source=image)
        self.name_scroll = Label(text=details[1])
        self.price_scroll = Label(text=details[3])
        self.more_scroll = Button(text='More...', on_release=partial(self.more_button_clicked, text=details))

        self.add_widget(self.image_scroll)
        self.add_widget(self.name_scroll)
        self.add_widget(self.price_scroll)
        self.add_widget(self.more_scroll)

    def more_button_clicked(self, obj, text):
        item_details_screen.details = text

        item_details_screen.image_label.source = item_details_screen.details[2]
        item_details_screen.name_label.text = item_details_screen.details[1]
        item_details_screen.price_label.text = item_details_screen.details[3]
        item_details_screen.details_label.text = item_details_screen.details[4]

        seller_id = item_details_screen.details[6]
        sql_command('select * from user where userid={}'.format(seller_id))
        data = csr.fetchall()
        item_details_screen.seller_contact_label.text = f'Address: {data[0][3]}\nPhone: {str(data[0][4])}'

        screen_manager.current = 'itemdetails'


class ItemDetailsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.grid_layout = GridLayout(cols=2, rows=6)

        self.details = ()

        self.image_label = Image()
        self.grid_layout.add_widget(self.image_label)
        self.grid_layout.add_widget(Label())

        self.name_text_label = Label(text='Name')
        self.name_label = Label()
        self.grid_layout.add_widget(self.name_text_label)
        self.grid_layout.add_widget(self.name_label)

        self.price_text_label = Label(text='Price')
        self.price_label = Label()
        self.grid_layout.add_widget(self.price_text_label)
        self.grid_layout.add_widget(self.price_label)

        self.details_text_label = Label(text='Details')
        self.details_label = Label()
        self.grid_layout.add_widget(self.details_text_label)
        self.grid_layout.add_widget(self.details_label)

        self.seller_contact_text_label = Label(text='Seller details')
        self.seller_contact_label = Label()
        self.grid_layout.add_widget(self.seller_contact_text_label)
        self.grid_layout.add_widget(self.seller_contact_label)

        self.back_button = Button(text='Back', on_release=self.back_button_clicked)
        self.grid_layout.add_widget(self.back_button)

        self.buy_button = Button(text='Buy', on_release=self.buy_button_clicked)
        self.grid_layout.add_widget(self.buy_button)

        self.add_widget(self.grid_layout)

    def back_button_clicked(self, obj):
        screen_manager.current = 'items'
        self.details = ''

    def buy_button_clicked(self, obj):
        print(self.details)
        sql_command("update items set issold='y' where itemid={}".format(self.details[0]), 'mod')
        self.details = ''


class NewitemScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.grid_layout = GridLayout(rows=7, cols=2)

        self.image_label = Image()
        self.image_button = Button(text='Add image', on_release=self.image_button_clicked)
        self.file_chooser = FileChooserIconView()
        self.image = None
        self.popup = None
        Clock.schedule_interval(self.get_selected_file, 1)

        self.name_label = Label(text='Name')
        self.name_text_input = TextInput()

        self.price_label = Label(text='Price')
        self.price_text_input = TextInput()

        self.details_label = Label(text='Details')
        self.details_text_input = TextInput()

        self.tags_label = Label(text='Tags')
        self.tags_text_input = TextInput()

        self.cancel_button = Button(text='Cancel', on_release=self.cancel_button_clicked)
        self.submit_button = Button(text='Submit', on_release=self.submit_button_clicked)

        self.grid_layout.add_widget(self.image_label)
        self.grid_layout.add_widget(self.image_button)
        self.grid_layout.add_widget(self.name_label)
        self.grid_layout.add_widget(self.name_text_input)
        self.grid_layout.add_widget(self.price_label)
        self.grid_layout.add_widget(self.price_text_input)
        self.grid_layout.add_widget(self.details_label)
        self.grid_layout.add_widget(self.details_text_input)
        self.grid_layout.add_widget(self.tags_label)
        self.grid_layout.add_widget(self.tags_text_input)
        self.grid_layout.add_widget(self.cancel_button)
        self.grid_layout.add_widget(self.submit_button)

        self.add_widget(self.grid_layout)

    def image_button_clicked(self, obj):
        self.file_chooser.selection = []
        self.popup = Popup(title='Choose image', auto_dismiss=False)
        self.file_chooser.path = r'C:\Users\gmharish\Desktop'
        self.popup.open()
        self.box = BoxLayout(orientation='vertical')
        self.popup.add_widget(self.box)
        self.box.add_widget(self.file_chooser)
        button = Button(text='Exit', on_release=self.filechooser_popup_close_button_clicked, size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        self.box.add_widget(button)

    def filechooser_popup_close_button_clicked(self, obj):
        self.popup.dismiss()
        self.box.remove_widget(self.file_chooser)

    def get_selected_file(self, dt):
        self.image = self.file_chooser.selection
        if self.image:
            # self.remove_widget(self.popup)
            self.popup.remove_widget(self.file_chooser)
            self.image_label.source = self.image[0]

    def cancel_button_clicked(self, obj):
        screen_manager.current = 'items'
        self.name_text_input.text = ''
        self.price_text_input.text = ''
        self.details_text_input.text = ''
        self.tags_text_input.text = ''
        self.image_label.source = ''
        self.file_chooser.selection = []

    def submit_button_clicked(self, obj):
        sql_command('select * from items')
        itemid_list = unpack_tuple(csr.fetchall(), 0)
        if itemid_list:
            last_id = itemid_list[-1]
        else:
            last_id = 0
        name = self.name_text_input.text
        price = self.price_text_input.text
        details = self.details_text_input.text
        tags = self.tags_text_input.text
        # print(self.image[0])
        sql_command("insert into items values({}, '{}', '{}', '{}', '{}', '{}', {}, '{}')".format(last_id + 1, name, modify_path(self.image[0]), price, details, tags, items_screen.userid, 'n'), 'mod')
        screen_manager.current = 'items'
        self.image_label.source = ''
        self.file_chooser.selection = []
        self.name_text_input.text = ''
        self.price_text_input.text = ''
        self.details_text_input.text = ''
        self.tags_text_input.text = ''


class EcommerceApp(App):
    def build(self):
        self.title = 'E-Commerce'
        return screen_manager


# fixed_size = (1000, 700)
# Window.size = fixed_size
#
#
# def resize(*args):
#     Window.size = fixed_size
#
#
# Window.bind(on_resize=resize)
login_screen = LoginScreen(name='login')
items_screen = ItemsScreen(name='items')
item_details_screen = ItemDetailsScreen(name='itemdetails')
newitem_screen = NewitemScreen(name='newitem')

screen_manager = ScreenManager()
screen_manager.add_widget(login_screen)
screen_manager.add_widget(items_screen)
screen_manager.add_widget(item_details_screen)
screen_manager.add_widget(newitem_screen)

EcommerceApp().run()

# sql_command('drop table user', 'mod')
# sql_command('drop table items', 'mod')

'''
class ProfileScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.box_layout_outer = BoxLayout(orientation='vertical')

        # back
        self.back_button = Button(text='Back', on_release=self.back_button_clicked)
        # image
        self.image_label = Label(text='image')
        # username
        self.box_layout_inner_1 = BoxLayout()
        self.name_label = Label(text='Name')
        self.name_text_input = TextInput(text=items_screen.username, multiline=False, on_text_validate=self.enter)
        self.box_layout_inner_1.add_widget(self.name_label)
        self.box_layout_inner_1.add_widget(self.name_text_input)
        # password
        self.box_layout_inner_2 = BoxLayout()
        self.password_label = Label(text='Password')
        self.password_text_input = TextInput(text=items_screen.password, multiline=False, on_text_validate=self.enter)
        self.box_layout_inner_2.add_widget(self.password_label)
        self.box_layout_inner_2.add_widget(self.password_text_input)
        # new item
        self.new_item_button = Button(text='+ New item', on_release=self.new_item_button_clicked)

        self.box_layout_outer.add_widget(self.back_button)
        self.box_layout_outer.add_widget(self.image_label)
        self.box_layout_outer.add_widget(self.box_layout_inner_1)
        self.box_layout_outer.add_widget(self.box_layout_inner_2)
        self.box_layout_outer.add_widget(self.new_item_button)

        self.add_widget(self.box_layout_outer)

    def back_button_clicked(self, obj):
        screen_manager.current = 'items'

    def new_item_button_clicked(self, obj):
        screen_manager.current = 'newitem'
'''
