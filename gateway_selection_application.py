from gateway_selection import Device, Space, Gateway, DeviceType
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

class GatewaySelectionWindow(GridLayout):
    def __init__(self, **kwargs):
        super(GatewaySelectionWindow, self).__init__(**kwargs)

        self.rows = 3
        self.cols = 1
        self.row_default_height = 70.0
        self.row_force_default = True
        self.spacing = [10, 10]

        first_row = BoxLayout(orientation="horizontal")
        first_row.padding = [10, 10, 10, 10]
        first_row.spacing = [10, 10]

        self.__height_text_input = TextInput(text="10", multiline=False)
        first_row.add_widget(Label(text="Height [m]:"))
        first_row.add_widget(self.__height_text_input)

        self.__width_text_input = TextInput(text="10", multiline=False)
        first_row.add_widget(Label(text="Width [m]:"))
        first_row.add_widget(self.__width_text_input)

        self.__gateways_text_input = TextInput(text="5", multiline=False)
        first_row.add_widget(Label(text="Gateways:"))
        first_row.add_widget(self.__gateways_text_input)

        self.__a_devices_text_input = TextInput(text="10", multiline=False)
        first_row.add_widget(Label(text="A Devices:"))
        first_row.add_widget(self.__a_devices_text_input)

        self.__b_devices_text_input = TextInput(text="10", multiline=False)
        first_row.add_widget(Label(text="B Devices:"))
        first_row.add_widget(self.__b_devices_text_input)

        self.add_widget(first_row)

        second_row = BoxLayout(orientation="horizontal")
        second_row.padding = [10, 10, 10, 10]
        second_row.spacing = [10, 10]

        self.__bandwidth_text_input = TextInput(text="100", multiline=False)
        second_row.add_widget(Label(text="Bandwidth [Mbps]:"))
        second_row.add_widget(self.__bandwidth_text_input)

        self.__radius_text_input = TextInput(text="5", multiline=False)
        second_row.add_widget(Label(text="Radius [m]:"))
        second_row.add_widget(self.__radius_text_input)
    
    def center_text_input(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width) / 2.0

class GatewaySelectionApplication(App):
    def build(self):
        return GatewaySelectionWindow() 


if __name__ == "__main__":
    GatewaySelectionApplication().run()