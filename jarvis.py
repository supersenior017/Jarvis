import tkinter as tk
import modes
import openai_api
import threading

class Jarvis(tk.Tk):

    # constants used throughout the program
    PADDING = 17
    BOX_COLOUR = 'black'
    TEXT_COLOUR = 'white'
    UNSELECTED_BOX_OUTLINE_COLOUR = '#660080'
    SELECTED_BOX_OUTLINE_COLOUR = '#660080'

    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = int(self.winfo_screenwidth() * 0.65)
        self.WINDOW_HEIGHT = int(self.winfo_screenheight() * 0.75)
        self.BOX_RELATIVE_WIDTH = 0.05 * self.WINDOW_WIDTH
        self.INPUT_BOX_RELATIVE_HEIGHT = 0.0075 * self.WINDOW_HEIGHT
        self.OUTPUT_BOX_RELATIVE_HEIGHT = 0.021 * self.WINDOW_HEIGHT

        # text widgets, labels, and buttons
        self.input_box = tk.Text(self, height=int(self.INPUT_BOX_RELATIVE_HEIGHT), width=int(self.BOX_RELATIVE_WIDTH),
                                 wrap=tk.WORD,
                                 font=('Source code pro', 20))
        self.input_box.configure(padx=self.PADDING, pady=self.PADDING, bg=self.BOX_COLOUR, fg='gray',
                                 highlightbackground=self.UNSELECTED_BOX_OUTLINE_COLOUR,
                                 highlightcolor=self.SELECTED_BOX_OUTLINE_COLOUR,
                                 insertbackground=self.TEXT_COLOUR)
        self.input_box.bind('<Shift-KeyPress>', lambda event: self.process_input())

        self.output_box = tk.Text(self, height=int(self.OUTPUT_BOX_RELATIVE_HEIGHT), width=int(self.BOX_RELATIVE_WIDTH),
                                  wrap=tk.WORD, font=('Source code pro', 20))
        self.output_box.configure(padx=self.PADDING, pady=self.PADDING, bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR,
                                  highlightbackground=self.UNSELECTED_BOX_OUTLINE_COLOUR,
                                  highlightcolor=self.SELECTED_BOX_OUTLINE_COLOUR,
                                  insertbackground=self.TEXT_COLOUR)

        self.input_label = tk.Label(self, text="> What would you like to know?", font=('Source code pro', 20))
        self.input_label.configure(bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR)

        self.output_label = tk.Label(self, text="> Answer", font=('Source code pro', 20))
        self.output_label.configure(bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR)

        self.process_button = tk.Button(self, text="> generate <", command=self.process_input)

        self.response_generation_complete = True

    def configure_main_window(self):
        # Bind the FocusIn and FocusOut events of input_box to on_entry_click and on_focus_out methods
        self.input_box.bind('<FocusIn>', self.on_entry_click)
        self.input_box.bind('<FocusOut>', self.on_focus_out)

    def configure_main_window(self):
        self.configure(bg='black')  # background color
        self.attributes("-alpha", 0.9)  # make it a bit transparent; higher value means less transparent
        self.title("J.A.R.V.I.S")

        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')

        # pack widgets inside parent widget (main_window)
        self.input_label.pack()
        self.input_box.pack()

        self.output_label.pack()
        self.output_box.pack()

        self.process_button.pack()

    def run(self):
        self.configure_main_window()
        self.mainloop()

    def display_text(self, txt):
        for index, char in enumerate(txt):
            # create a delay of 17 milliseconds before displaying each character
            self.after(10 * index, self.append_text, char)

    def append_text(self, char):
        self.output_box.insert(tk.END, char)
        self.output_box.tag_configure('white')

    def process_input(self):
        if self.response_generation_complete:
            self.response_generation_complete = False
            self.process_button.config(state=tk.DISABLED)

            input_text = self.input_box.get("1.0", "end-1c")  # Get the text from the input box
            self.input_box.delete('1.0', tk.END)  # clear input box

            # clear output box
            self.output_box.delete("1.0", tk.END)

            # start displaying loading message (3 dots in this case)
            def display_dots(count):
                if not self.response_generation_complete:
                    if count == 0:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, ".")
                    elif count == 1:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, "..")
                    elif count == 2:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, "...")
                    elif count == 3:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, ".")
                    self.after(150, display_dots, (count % 3) + 1)

            display_dots(1)

            # start a new thread to generate chatbot response
            threading.Thread(target=self.generate_response, args=(input_text,)).start()

    def generate_response(self, input_text):
        try:
            # generate chatbot response
            output_text = openai_api.text_text(input_text)
            output_text = "> " + output_text
            self.response_generation_complete = True

            # display response
            self.output_box.configure(state='normal')
            self.output_box.delete("1.0", tk.END)  # Clear the output box
            self.display_text(output_text)

            # Enable the "generate" button once the display_text method is done
            self.after(len(output_text) * 10, self.process_button.config, {'state': tk.NORMAL})

        except Exception as e:
            print(e)


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()