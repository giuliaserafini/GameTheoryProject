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

        tk.Label(self.__controls_frame, text="Height [m]:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__rows_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__rows_entry.insert(tk.END, "100")
        self.__rows_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Width [m]:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__columns_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__columns_entry.insert(tk.END, "100")
        self.__columns_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Gateways:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__gateways_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__gateways_entry.insert(tk.END, "50")
        self.__gateways_entry.grid(row=0, column=5, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="A Devices:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__a_devices_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__a_devices_entry.insert(tk.END, "100")
        self.__a_devices_entry.grid(row=0, column=7, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="B Devices:").grid(row=0, column=8, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__b_devices_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__b_devices_entry.insert(tk.END, "100")
        self.__b_devices_entry.grid(row=0, column=9, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Bandwidth [Mbps]:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__bandwidth_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__bandwidth_entry.insert(tk.END, "100")
        self.__bandwidth_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Radius [m]:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__radius_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__radius_entry.insert(tk.END, "25")
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

        self.__controls_frame.pack(expand=tk.TRUE, fill=tk.BOTH, side=tk.TOP)
        self.__main_frame.pack(expand=tk.TRUE, fill=tk.BOTH)

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
        self.__space_canvas.configure(scrollregion=self.__space_canvas.bbox("all"))

    def __on_vertical(self, event):
        self.__space_canvas.yview_scroll(-1 * event.delta, 'mm')

    def __on_horizontal(self, event):
        self.__space_canvas.xview_scroll(-1 * event.delta, 'mm')

    def __build_space(self, parameters):
        canvas_width = 45 * parameters["columns"]
        canvas_height = 45 * parameters["rows"]
        

        self.__space_canvas = tk.Canvas(self.__main_frame, bg="black", width=canvas_width, height=canvas_height, scrollregion=(0, 0, canvas_width, canvas_width))

        self.__canvas_frame = tk.Frame(self.__space_canvas, bg="white", width=canvas_width, height=canvas_height)
        self.__canvas_frame.pack(expand=tk.TRUE, fill=tk.BOTH, side=tk.TOP)
        self.__space_canvas.bind("<Configure>", self.__update_scrollregion)
        #self.__space_canvas.bind_all('<MouseWheel>', self.__on_vertical)
        #self.__space_canvas.bind_all('<Shift-MouseWheel>', self.__on_horizontal)
        
        horizontal_scroll_bar = tk.Scrollbar(self.__main_frame, orient=tk.HORIZONTAL)
        horizontal_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
        horizontal_scroll_bar.config(command=self.__space_canvas.xview)

        vertical_scroll_bar = tk.Scrollbar(self.__main_frame, orient=tk.VERTICAL)
        vertical_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        vertical_scroll_bar.config(command=self.__space_canvas.yview)

        self.__gateways = [Gateway(parameters["bandwidth"], radius=parameters["radius"]) for _ in range(parameters["gateways"])]
        self.__a_devices = [Device(DeviceType.TYPE_A) for _ in range(parameters["a_devices"])]
        self.__b_devices = [Device(DeviceType.TYPE_B) for _ in range(parameters["b_devices"])]
        self.__space = Space(parameters["rows"], parameters["columns"])
        self.__image = ImageTk.PhotoImage(Image.open("square.png"))
        for element in self.__gateways + self.__a_devices + self.__b_devices:
            (x, y) = self.__space.add_element(element)
            x_canvas = x * 45 + 2.5
            y_canvas = y * 45 + 2.5
            tk.Label(self.__canvas_frame, image=self.__image).pack()
            #self.__space_canvas.create_image(x_canvas, y_canvas, image=self.__image)
                  

        self.__space_canvas.create_window(0, 0, window=self.__canvas_frame, anchor='nw')
        self.__space_canvas.config(width=canvas_width, height=canvas_height)
        self.__space_canvas.config(xscrollcommand=horizontal_scroll_bar.set, yscrollcommand=vertical_scroll_bar.set)
        self.__space_canvas.pack(expand=tk.TRUE, fill=tk.BOTH, side=tk.LEFT)

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
            self.__toggle_controls()
            self.__start_stop_simulation["text"] = "Start simulation"


def main():
    root = tk.Tk()
    root.title("Gateway selection")
    window = GatewaySelectionWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()