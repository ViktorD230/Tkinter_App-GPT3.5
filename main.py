from tkinter import *
import customtkinter
import openai
import os
import pickle

# Initiate App
root = customtkinter. CTk()
root.title("ChatGPT Bot")
root.geometry('600x500')
root.iconbitmap('openai_logo_icon_248315.ico')

# Set Color Scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

chat_history = []

# Submit to ChatGPT
def speak():
    if chat_entry.get():
        filename = "api_key"

        try:
            if os.path.isfile(filename):
                input_file = open(filename, "rb")
                stuff = pickle.load(input_file)

                openai.api_key = stuff
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": chat_entry.get()}
                    ]
                )
                # Update chat history
                user_message = chat_entry.get()
                chat_history.append({"role": "user", "content": user_message})
                chat_history.append({"role": "assistant", "content": response.choices[0].message["content"]})

                # Display chat history in my_text
                display_chat_history()

        except Exception as e:
            my_text.insert(END, f"\n\n There was an error\n\n{e}")
    else:
        my_text.insert(END, "\n\nHey! You Forgot To Type Anything!")

# Clear The Screans
def clear():
    # Clear The Main Text Box
    my_text.delete(1.0, END)
    # Clear the query entry widget
    chat_entry.delete(0, END)

# Do API Stuff
def key():
    filename = "api_key"

    try:
        if os.path.isfile(filename):
            input_file = open(filename, "rb")
            stuff = pickle.load(input_file)
            api_entry.insert(END, stuff)
        else:
            input_file = open(filename, "wb")
            input_file.close()
    except Exception as e:
        my_text.insert(END, f"\n\n There was an error\n\n{e}")

    root.geometry("600x650")
    api_frame.pack(pady=30)


# Save The API Key
def save_key():
    try:
        filename = "api_key"
        output_file = open(filename, "wb")
        pickle.dump(api_entry.get(), output_file)

        api_entry.delete(0, END)
        api_frame.pack_forget()
        root.geometry("600x500")
    except Exception as e:
        my_text.insert(END, f"\n\n There was an error\n\n{e}")


# Display chat history
def display_chat_history():
    my_text.delete(1.0, END)
    for message in chat_history:
        role = message["role"]
        content = message["content"]
        my_text.insert(END, f"\n[{role}]: {content}")
    my_text.insert(END, "\n\n")

# Create Text Frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add Text Widget To Get ChatGPT Response
my_text = Text(text_frame,
               bg="#343638",
               width=65,
               bd=1,
               fg="#d6d6d6",
               relief="flat",
               wrap=WORD,
               selectbackground="#1f538d")
my_text.grid(row=0, column=0)

# Create Scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
       command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

# Add the scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

# Entry Widget To Type Stuff to ChatGPT
chat_entry = customtkinter.CTkEntry(root,
        placeholder_text="Type Something To ChatGPT...",
        width=535,
        height=50,
        border_width=1)
chat_entry.pack(pady=10)

# Create Button Frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

# Create Submit Buttons
submit_button = customtkinter.CTkButton(button_frame,
        text="Speak To ChatGPT",
        command=speak)
submit_button.grid(row=0, column=0, padx=25)

# Create Clear Buttons
clear_button = customtkinter.CTkButton(button_frame,
        text="Clear Response",
        command=clear)
clear_button.grid(row=0, column=1, padx=35)

# Create API Buttons
api_button = customtkinter.CTkButton(button_frame,
        text="Update API Key",
        command=key)
api_button.grid(row=0, column=2, padx=25)

# Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
        placeholder_text="Enter Your API Key",
        width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API Button
api_save_button = customtkinter.CTkButton(api_frame,
        text="Save Key",
        command=save_key)
api_save_button.grid(row=0, column=1, padx=10)



root.mainloop()
