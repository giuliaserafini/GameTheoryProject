import tkinter as tk

class GatewaySelectionWindow(object):
    BOTH = ("Both", 1)
    ONLY_A = ("A", 2)
    ONLY_B = ("B", 3)

    def __init__(self, root):
        self.__main_frame = tk.Frame(root)

        self.__controls_frame = tk.Frame(self.__main_frame)

        tk.Label(self.__controls_frame, text="Width [m]:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E + tk.W)
        self.__rows_entry = tk.Entry(self.__controls_frame, width=5, justify=tk.CENTER)
        self.__rows_entry.insert(tk.END, "100")
        self.__rows_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E + tk.W)

        tk.Label(self.__controls_frame, text="Height [m]:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E + tk.W)
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
    
    def __start_stop_simulation(self):
        print(self.__start_stop_simulation["text"])

def main():
    root = tk.Tk(screenName="Gateway Selection")
    window = GatewaySelectionWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()