import tkinter as tk
import re
from tkinter import filedialog
from tkinter import ttk
import textwrap

def wrap_text(text, width=100):
    """Wrap text to a specific width."""
    return "\n".join(textwrap.fill(line, width) for line in text.split("\n"))

def send_message(event=None):
    """Handle sending a message."""
    user_message = user_entry.get()
    if user_message.strip():
        wrapped_user_message = wrap_text(user_message)
        
        # Display user's message
        chatbox.configure(state=tk.NORMAL)
        chatbox.insert(tk.END, f"You: {wrapped_user_message}\n", "user")
        chatbox.configure(state=tk.DISABLED)
        user_entry.delete(0, tk.END)

        # Auto-scroll to the bottom
        chatbox.see(tk.END)

        # Simulate AI response
        ai_response = "This is a response from the AI backend."
        wrapped_ai_response = wrap_text(ai_response)
        chatbox.configure(state=tk.NORMAL)
        chatbox.insert(tk.END, f"AI: {wrapped_ai_response}\n", "ai")
        chatbox.configure(state=tk.DISABLED)

        # Auto-scroll to the bottom
        chatbox.see(tk.END)


def upload_image():
    """Handle uploading an image."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        # Simulate displaying uploaded image in chat
        chatbox.configure(state=tk.NORMAL)
        chatbox.insert(tk.END, "You uploaded an image.\n", "user")
        chatbox.insert(tk.END, "AI: Image received. Analyzing...\n", "ai")
        chatbox.configure(state=tk.DISABLED)

        # Auto-scroll to the bottom
        chatbox.see(tk.END)


def submit_preferences():
    """Handle preferences submission."""
    zip_code = zip_entry.get()
    selected_language = language_dropdown.get()

    # Validate ZIP code
    if not re.fullmatch(r"\d{5}", zip_code):
        error_label.config(text="Please enter a valid 5-digit ZIP code.")
        return
    if not selected_language.strip():
        error_label.config(text="Please select a language.")
        return

    # Hide preferences frame and show chat frame
    error_label.config(text="")
    preferences_frame.pack_forget()
    chat_frame.pack(fill=tk.BOTH, expand=True)


# Initialize main window
root = tk.Tk()
root.title("Plant Doctor Chatbot")
root.geometry("800x600")
root.configure(bg="lightgreen")


# Preferences Frame
preferences_frame = tk.Frame(root, bg="lightgreen")
preferences_frame.pack(fill=tk.BOTH, expand=True)

welcome_label = tk.Label(preferences_frame, text="Welcome to Plant Doctor", font=("Arial", 24, "bold"), bg="lightgreen")
welcome_label.pack(pady=20)

description_label = tk.Label(preferences_frame, text="Set your preferences to get started", font=("Arial", 14), bg="lightgreen")
description_label.pack(pady=10)

zip_label = tk.Label(preferences_frame, text="Zip Code:", font=("Arial", 12), bg="lightgreen")
zip_label.pack(pady=5)
zip_entry = tk.Entry(preferences_frame, font=("Arial", 12))
zip_entry.pack(pady=5)

language_label = tk.Label(preferences_frame, text="Language Preference:", font=("Arial", 12), bg="lightgreen")
language_label.pack(pady=5)

# Dropdown menu for language selection
languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Hindi", "Arabic"]
language_dropdown = ttk.Combobox(preferences_frame, values=languages, font=("Arial", 12), state="readonly")
language_dropdown.pack(pady=5)

start_button = tk.Button(preferences_frame, text="Start", font=("Arial", 14), bg="darkgreen", fg="white", command=submit_preferences)
start_button.pack(pady=20)

error_label = tk.Label(preferences_frame, text="", font=("Arial", 10), fg="red", bg="lightgreen")
error_label.pack()



# Chat Frame
chat_frame = tk.Frame(root, bg="lightgreen")

# Chatbox and Scrollbar
chatbox = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12), bg="gray", fg="white")
chatbox.tag_config("user", foreground="blue", justify="right")
chatbox.tag_config("ai", foreground="darkgreen", justify="left")
chatbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

scrollbar = tk.Scrollbar(chat_frame, command=chatbox.yview)
chatbox['yscrollcommand'] = scrollbar.set
scrollbar.grid(row=0, column=1, sticky="ns")

chat_frame.grid_rowconfigure(0, weight=1)
chat_frame.grid_columnconfigure(0, weight=1)

# Input Frame
input_frame = tk.Frame(chat_frame, bg="lightgreen")
input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

camera_icon_button = tk.Button(input_frame, text="📷", font=("Arial", 12), bg="white", state=tk.DISABLED)
camera_icon_button.pack(side=tk.LEFT, padx=5)

upload_button = tk.Button(input_frame, text="🖼️", font=("Arial", 12), command=upload_image, bg="white")
upload_button.pack(side=tk.LEFT, padx=5)

user_entry = tk.Entry(input_frame, font=("Arial", 12))
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
user_entry.bind("<Return>", send_message)

send_button = tk.Button(input_frame, text="Send", font=("Arial", 12), bg="darkgreen", fg="white", command=send_message)
send_button.pack(side=tk.RIGHT, padx=5)

# Footer
footer_label = tk.Label(root, text="© 2025 Plant Doctor. All rights reserved.", font=("Arial", 10), bg="darkgreen", fg="white")
footer_label.pack(side=tk.BOTTOM, fill=tk.X)

# Mainloop
root.mainloop()
