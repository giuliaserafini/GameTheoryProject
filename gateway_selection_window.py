import tkinter as tk
import tkinter.messagebox as mb
from PIL import Image, ImageTk
from gateway_selection import Device, Space, Gateway, DeviceType

class GatewaySelectionWindow(object):
    BOTH = ("Both", 1)
    ONLY_A = ("A", 2)
    ONLY_B = ("B", 3)

    def __init__(self, root):
        self.__main_frame = tk.Frame(root)
        self.__controls_frame = tk.Frame(self.__main_frame)

        self.__images = {
            "black_gateway" : ImageTk.PhotoImage(Image.open("./icons/black_gateway.gif")),
            "red_gateway" : ImageTk.PhotoImage(Image.open("./icons/red_gateway.gif")),
            "blue_sensor" : ImageTk.PhotoImage(Image.open("./icons/blue_sensor.gif")),
            "red_sensor" : ImageTk.PhotoImage(Image.open("./icons/red_sensor.gif")),
            "yellow_sensor" : ImageTk.PhotoImage(Image.open("./icons/yellow_sensor.gif"))
        }
        
        self.__build_first_controls_row()
        self.__build_second_controls_row()

        self.__controls_frame.pack(expand=tk.TRUE, fill=tk.BOTH, side=tk.TOP)
        self.__main_frame.pack(expand=tk.TRUE, fill=tk.BOTH)

        self.istances = []

    def __build_first_controls_row(self):
        tk.Label(self.__controls_frame, text="Height [m]:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E + tk.W)
        
        self.__rows_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__rows_entry.insert(tk.END, "10")
        self.__rows_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Width [m]:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__columns_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__columns_entry.insert(tk.END, "10")
        self.__columns_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Gateways:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__gateways_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__gateways_entry.insert(tk.END, "5")
        self.__gateways_entry.grid(row=0, column=5, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="A Devices:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__a_devices_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__a_devices_entry.insert(tk.END, "10")
        self.__a_devices_entry.grid(row=0, column=7, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="B Devices:").grid(row=0, column=8, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__b_devices_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__b_devices_entry.insert(tk.END, "10")
        self.__b_devices_entry.grid(row=0, column=9, padx=5, pady=5, sticky=tk.E + tk.W)

    def __build_second_controls_row(self):
        tk.Label(self.__controls_frame, text="Bandwidth [Mbps]:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__bandwidth_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__bandwidth_entry.insert(tk.END, "100")
        self.__bandwidth_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Radius [m]:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__radius_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__radius_entry.insert(tk.END, "5")
        self.__radius_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Strategies:").grid(row=1, column=4, padx=5, pady=5, sticky=tk.E + tk.W)

        self.__strategies_variable = tk.IntVar()

        both_radio_button = tk.Radiobutton(self.__controls_frame, text=GatewaySelectionWindow.BOTH[0], variable=self.__strategies_variable, value=GatewaySelectionWindow.BOTH[1], justify=tk.LEFT)
        both_radio_button.select()
        both_radio_button.grid(row=1, column=5, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Radiobutton(self.__controls_frame, text=GatewaySelectionWindow.ONLY_A[0], variable=self.__strategies_variable, value=GatewaySelectionWindow.ONLY_A[1], justify=tk.LEFT).grid(row=1, column=6, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Radiobutton(self.__controls_frame, text=GatewaySelectionWindow.ONLY_B[0], variable=self.__strategies_variable, value=GatewaySelectionWindow.ONLY_B[1], justify=tk.LEFT).grid(row=1, column=7, padx=5, pady=5, sticky=tk.E + tk.W)
        
        self.__start_stop_simulation = tk.Button(self.__controls_frame, text="Start simulation", command=self.__start_stop_simulation)
        self.__start_stop_simulation.grid(row=1, column=8, columnspan=2, padx=5, pady=5, sticky=tk.E + tk.W)

    def __validate_entry(self, entry, name):
        try:
            entry_value = int(entry.get())
            if entry_value <= 0:
                raise ValueError()
            return entry_value
        except ValueError as parameterException:
            raise ValueError("The {} must be a non-negative number.".format(name), entry)
    
    def __validate_parameters(self):
        parameters = {}
        parameters["rows"] = self.__validate_entry(self.__rows_entry, "height")
        parameters["columns"] = self.__validate_entry(self.__columns_entry, "width")
        parameters["gateways"] = self.__validate_entry(self.__gateways_entry, "gateways")
        parameters["a_devices"] = self.__validate_entry(self.__a_devices_entry, "A devices")
        parameters["b_devices"] = self.__validate_entry(self.__b_devices_entry, "B devices")
        parameters["bandwidth"] = self.__validate_entry(self.__bandwidth_entry, "bandwidth")
        parameters["radius"] = self.__validate_entry(self.__radius_entry, "radius")
        parameters["strategies"] = self.__strategies_variable.get()
        return parameters

    def __toggle_controls(self):
        for control in self.__controls_frame.winfo_children():
            if isinstance(control, tk.Entry) or isinstance(control, tk.Radiobutton):
                if control["state"] == tk.NORMAL:
                    control["state"] = tk.DISABLED
                else:
                    control["state"] = tk.NORMAL
    
    def __update_scrollregion(self, event):
        self.__space_canvas.configure(scrollregion=(0, 0, self.__canvas_width, self.__canvas_height))

    def __build_space(self, parameters):
        cell_size = 40
        self.__canvas_width = cell_size * parameters["columns"]
        self.__canvas_height = cell_size * parameters["rows"]
        
        self.__space_canvas = tk.Canvas(self.__main_frame, width=self.__canvas_width, height=self.__canvas_height, scrollregion=(0, 0, self.__canvas_width, self.__canvas_height))

        self.__horizontal_scroll_bar = tk.Scrollbar(self.__main_frame, orient=tk.HORIZONTAL)
        self.__horizontal_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.__horizontal_scroll_bar.config(command=self.__space_canvas.xview)

        self.__vertical_scroll_bar = tk.Scrollbar(self.__main_frame, orient=tk.VERTICAL)
        self.__vertical_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__vertical_scroll_bar.config(command=self.__space_canvas.yview)

        self.__gateways = [Gateway(parameters["bandwidth"], radius=parameters["radius"]) for _ in range(parameters["gateways"])]
        self.__a_devices = [Device(DeviceType.TYPE_A) for _ in range(parameters["a_devices"])]
        self.__b_devices = [Device(DeviceType.TYPE_B) for _ in range(parameters["b_devices"])]
        self.__space = Space(parameters["rows"], parameters["columns"])
        
        self.__positions = {}
        
        for element in self.__gateways + self.__a_devices + self.__b_devices:
            (x, y) = self.__space.add_element(element)
            self.__positions[element] = (x, y)
            if isinstance(element, Device):
                if element.type == DeviceType.TYPE_A:
                    self.__space_canvas.create_image(x * cell_size, y * cell_size, image=self.__images["blue_sensor"], anchor=tk.NW)
                else:
                    self.__space_canvas.create_image(x * cell_size, y * cell_size, image=self.__images["red_sensor"], anchor=tk.NW)
            elif isinstance(element, Gateway):
                x_center = x * cell_size + (cell_size / 2.0)
                y_center = y * cell_size + (cell_size / 2.0)
                r = element.radius * cell_size
                #x1 = max(x_center - r, 0)
                #x2 = min(x_center + r, canvas_width)
                #y1 = max(y_center - r, 0)
                #y2 = min(y_center + r, canvas_height)
                #self.__space_canvas.create_arc(x_center - r, y_center - r, x_center + r, y_center + r)
                self.__space_canvas.create_oval(x_center - r, y_center - r, x_center + r, y_center + r)
                #self.__space_canvas.create_oval(x1, y1, x2, y2)
                self.__space_canvas.create_image(x * cell_size, y * cell_size, image=self.__images["black_gateway"], anchor=tk.NW)
        
        for i in range(parameters["rows"]):
            for j in range(parameters["columns"]):
                box = (i * cell_size, j * cell_size, (i + 1) * cell_size, (j + 1) * cell_size)
                self.__space_canvas.create_rectangle(box)
                  
        self.__space_canvas.bind("<Configure>", self.__update_scrollregion)
        self.__space_canvas.configure(scrollregion=(0, 0, self.__canvas_width, self.__canvas_height))#self.__space_canvas.bbox("all"))
        self.__space_canvas.configure(width=self.__canvas_width, height=self.__canvas_height)
        self.__space_canvas.config(xscrollcommand=self.__horizontal_scroll_bar.set, yscrollcommand=self.__vertical_scroll_bar.set)
        self.__space_canvas.pack(expand=tk.TRUE, fill=tk.NONE, anchor=tk.CENTER, side=tk.TOP)

    def __start_stop_simulation(self):
        if self.__start_stop_simulation["text"] == "Start simulation":
            try:
                parameters = self.__validate_parameters()

                self.__toggle_controls()
                self.__build_space(parameters)

                self.__start_stop_simulation["text"] = "Stop simulation"
            except ValueError as parameterException:
                mb.showerror("Input parameter error!", parameterException.args[0])
                parameterException.args[1].delete(0, tk.END)
        else:
            self.__space_canvas.destroy()
            self.__horizontal_scroll_bar.destroy()
            self.__vertical_scroll_bar.destroy()
            self.__toggle_controls()
            self.__start_stop_simulation["text"] = "Start simulation"


def main():
    pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gateway selection")
    window = GatewaySelectionWindow(root)
    root.mainloop()