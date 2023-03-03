import tkinter as tk
import modes
import openai_api
import threading

WINDOW_WIDTH = 875
WINDOW_HEIGHT = 550
PADDING = 17

BOX_COLOUR = 'black'
TEXT_COLOUR = 'white'
UNSELECTED_BOX_OUTLINE_COLOUR = '#660080'
SELECTED_BOX_OUTLINE_COLOUR = '#660080'

# used to check whether the thread generating the response is still running or not
# this is fundamental if we want to have buttons to stop the current generation of text and start another
# this also helps us in disabling the 'generate' button
response_generation_complete = True


def display_text(txt):
    for index, char in enumerate(txt):
        # create a delay of 200 milliseconds before displaying each character
        root.after(17 * index, append_text, char)


def append_text(char):
    output_box.insert(tk.END, char)
    output_box.tag_configure('white')


def process_input():
    global response_generation_complete

    if response_generation_complete:
        response_generation_complete = False
        process_button.config(state=tk.DISABLED)

        input_text = input_box.get("1.0", "end-1c")  # Get the text from the input box
        input_box.delete('1.0', tk.END)  # clear input box
        input_box.insert('1.0', '$ ')

        # clear output box
        output_box.delete("1.0", tk.END)

        # start displaying loading message (3 dots in this case)
        def display_dots(count):
            if not response_generation_complete:
                if count == 0:
                    output_box.delete("1.0", tk.END)
                    output_box.insert(tk.END, ".")
                elif count == 1:
                    output_box.delete("1.0", tk.END)
                    output_box.insert(tk.END, "..")
                elif count == 2:
                    output_box.delete("1.0", tk.END)
                    output_box.insert(tk.END, "...")
                elif count == 3:
                    output_box.delete("1.0", tk.END)
                    output_box.insert(tk.END, ".")
                root.after(117, display_dots, (count % 3) + 1)

        display_dots(1)

        # start a new thread to generate chatbot response
        threading.Thread(target=generate_response, args=(input_text,)).start()


def generate_response(input_text):
    global response_generation_complete
    try:
        # generate chatbot response
        output_text = openai_api.text_text(input_text)
        output_text = "> " + output_text
        response_generation_complete = True

        # display response
        output_box.configure(state='normal')
        output_box.delete("1.0", tk.END)  # Clear the output box
        display_text(output_text)

        process_button.config(state=tk.NORMAL)

    except Exception as e:
        print(e)


root = tk.Tk()
root.configure(bg='black')
root.attributes("-alpha", 0.9)
root.title("J.A.R.V.I.S")

input_label = tk.Label(root, text="> query: ")
input_label.configure(bg=BOX_COLOUR, fg=TEXT_COLOUR)
input_label.pack()

input_box = tk.Text(root, height=int(0.02 * WINDOW_HEIGHT), width=int(0.1 * WINDOW_WIDTH), wrap=tk.WORD)
input_box.configure(padx=PADDING, pady=PADDING, bg=BOX_COLOUR, fg=TEXT_COLOUR,
                    highlightbackground=UNSELECTED_BOX_OUTLINE_COLOUR, highlightcolor=SELECTED_BOX_OUTLINE_COLOUR,
                    insertbackground=TEXT_COLOUR)
input_box.insert('1.0', '$ ')
input_box.pack()

output_label = tk.Label(root, text="> answer: ")
output_label.configure(bg=BOX_COLOUR, fg=TEXT_COLOUR)
output_label.pack()

output_box = tk.Text(root, height=int(0.03 * WINDOW_HEIGHT), width=int(0.1 * WINDOW_WIDTH), wrap=tk.WORD)
output_box.configure(padx=PADDING, pady=PADDING, bg=BOX_COLOUR, fg=TEXT_COLOUR,
                     highlightbackground=UNSELECTED_BOX_OUTLINE_COLOUR, highlightcolor=SELECTED_BOX_OUTLINE_COLOUR,
                     insertbackground=TEXT_COLOUR)
output_box.pack()

process_button = tk.Button(root, text="> generate <", command=process_input)
process_button.pack()

root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

root.mainloop()
