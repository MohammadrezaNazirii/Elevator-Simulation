import tkinter as tk
from tkinter import simpledialog
from Main_Back import *

inp = []
floor = 0
t_quantum = 0
algo = 0
output = []
index = 0
next_val = 0

class MovingRectangleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Moving Rectangle App")

        # Canvas
        self.canvas = tk.Canvas(master, width=900, height=210, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, rowspan=11)  # Move canvas to column 0

        self.rectangle = self.canvas.create_rectangle(40, 100, 100, 140, fill="red")

        # Frame for the toolbar
        self.toolbar_frame = tk.Frame(master)
        self.toolbar_frame.grid(row=11, column=0, columnspan=2, padx=10, pady=10,
                                sticky="ew")  # Move toolbar to the bottom

        # Radio buttons
        self.label_radio = tk.Label(self.toolbar_frame, text="Select an option:")
        self.label_radio.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        self.radio_var = tk.StringVar()
        self.radio_var.set("FCFS")
        self.radio1 = tk.Radiobutton(self.toolbar_frame, text="FCFS", variable=self.radio_var, value="FCFS")
        self.radio2 = tk.Radiobutton(self.toolbar_frame, text="SJF", variable=self.radio_var, value="SJF")
        self.radio3 = tk.Radiobutton(self.toolbar_frame, text="RR", variable=self.radio_var, value="RR")
        self.radio4 = tk.Radiobutton(self.toolbar_frame, text="SRF", variable=self.radio_var, value="SRF")
        self.radio1.grid(row=0, column=1, pady=5, sticky=tk.W)
        self.radio2.grid(row=0, column=2, pady=5, sticky=tk.W)
        self.radio3.grid(row=0, column=3, pady=5, sticky=tk.W)
        self.radio4.grid(row=0, column=4, pady=5, sticky=tk.W)

        # Entry widgets for additional values
        self.label3 = tk.Label(self.toolbar_frame, text="Floor:")
        self.label3.grid(row=5, column=0, pady=5, sticky=tk.W)
        self.entry3 = tk.Entry(self.toolbar_frame, width=10)
        self.entry3.grid(row=5, column=1, pady=5, sticky=tk.W)

        self.label4 = tk.Label(self.toolbar_frame, text="TQ:")
        self.label4.grid(row=5, column=3, pady=5, sticky=tk.W)
        self.entry4 = tk.Entry(self.toolbar_frame, width=10)
        self.entry4.grid(row=5, column=4, pady=(10, 5), sticky=tk.W)

        self.save_button1 = tk.Button(self.toolbar_frame, text="SET", command=self.save_values1)
        self.save_button1.grid(row=5, column=7, pady=(10, 5), sticky=tk.W)

        self.label1 = tk.Label(self.toolbar_frame, text="in:")
        self.label1.grid(row=8, column=0, pady=5, sticky=tk.W)
        self.entry1 = tk.Entry(self.toolbar_frame, width=10)
        self.entry1.grid(row=8, column=1, pady=5, sticky=tk.W)

        self.label2 = tk.Label(self.toolbar_frame, text=" des:    ")
        self.label2.grid(row=8, column=3, pady=5, sticky=tk.W)
        self.entry2 = tk.Entry(self.toolbar_frame, width=10)
        self.entry2.grid(row=8, column=4, pady=5, sticky=tk.W)

        self.label6 = tk.Label(self.toolbar_frame, text="      Time:")
        self.label6.grid(row=8, column=6, pady=5, sticky=tk.W)
        self.entry6 = tk.Entry(self.toolbar_frame, width=10)
        self.entry6.grid(row=8, column=7, pady=5, sticky=tk.W)

        # Buttons
        self.save_button = tk.Button(self.toolbar_frame, text="Save Values", command=self.save_values)
        self.save_button.grid(row=8, column=10, columnspan=2, pady=10, sticky=tk.W)

        self.move_button = tk.Button(self.toolbar_frame, text="RUN", command=self.start_animation)
        self.move_button.grid(row=12, column=0, columnspan=2, pady=5, sticky=tk.W)

        self.move_button = tk.Button(self.toolbar_frame, text="Initialize", command=self.get_output)
        self.move_button.grid(row=9, column=0, columnspan=2, pady=5, sticky=tk.W)

        self.animation_speed = 19  # Adjust the speed of animation (in milliseconds)

    def save_values1(self):
        global floor, t_quantum, algo

        floor = int(self.entry3.get())
        t_quantum = int(self.entry4.get())
        algo = self.radio_var.get()

        initialize(algo, floor, t_quantum)


        for i in range(floor):
            self.text_position = (40 + i * 60, 70)
            self.canvas.create_text(self.text_position, text="|", anchor=tk.W, fill="black", tag="text_tag")
            self.text_position = (40 + i * 60, 50)
            self.canvas.create_text(self.text_position, text=str(i), anchor=tk.W, fill="black", tag="text_tag")

    def get_output(self):
        global output

        get_inputs(inp)

        output = run()

    def get_next(self):
        global index

        return_val = output[index] + 1 if output[index] >= 0 else output[index]

        index += 1

        return return_val

    def start_animation(self):

        global index, next_val

        previous_val = next_val
        next_val = self.get_next()

        if next_val == -0.5:
            print('Elevator should stop for passenger.')
        elif next_val <= -1:
            print(f'Elevator stops for {-next_val} seconds.')
        else:
            if next_val == previous_val:
                print('Do nothing.')
            else:
                self.animate_rectangle(40 + next_val * 60)

    def animate_rectangle(self, end_pos):
        current_position = self.canvas.coords(self.rectangle)
        if current_position[2] < end_pos:
            x = 1
        else:
            x = -1
        new_x1 = current_position[0] + x * 2
        new_y1 = current_position[1]
        new_x2 = current_position[2] + x * 2
        new_y2 = current_position[3]

        self.canvas.coords(self.rectangle, new_x1, new_y1, new_x2, new_y2)

        if x == -1:
            if new_x2 > end_pos:
                self.master.after(self.animation_speed, self.animate_rectangle, end_pos)
        else:
            if new_x2 < end_pos:
                self.master.after(self.animation_speed, self.animate_rectangle, end_pos)

    def save_values(self):
        value1 = int(self.entry1.get())
        value2 = int(self.entry2.get())
        value3 = int(self.entry6.get())

        inp.append([value3, value1, value2])

        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry6.delete(0, tk.END)



if __name__ == "__main__":
    root = tk.Tk()
    app = MovingRectangleApp(root)
    root.mainloop()
