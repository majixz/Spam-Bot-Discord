import discum
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import random

class DiscordMessenger:
    def __init__(self, root):
        self.root = root
        self.root.title("MaJiX's Discord Spammer")
        self.root.geometry("900x650")
        self.root.configure(bg="#5865F2")
        self.root.resizable(False, False)

        self.is_running = False
        self.should_quit = False
        self.threads = []
        self.delay_secs = 4
        self.token_clients = {}
        self.token_counters = {}

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#5865F2", foreground="white")
        style.configure("TButton", font=("Arial", 10))

        title_frame = tk.Frame(self.root, bg="#5865F2")
        title_frame.pack(pady=5)
        ttk.Label(title_frame, text="MaJiX's Discord Messenger", font=("Arial", 20, "bold")).pack()
        ttk.Label(title_frame, text="Created by MaJiX", font=("Arial", 10)).pack()

        controls = tk.Frame(self.root, bg="#5865F2")
        controls.pack(pady=5)
        ttk.Button(controls, text="Start", command=self.start_sending).grid(row=0, column=0, padx=10)
        ttk.Button(controls, text="Pause", command=self.pause_sending).grid(row=0, column=1, padx=10)
        ttk.Button(controls, text="Stop", command=self.stop_sending).grid(row=0, column=2, padx=10)
        ttk.Button(controls, text="Quit", command=self.quit_program).grid(row=0, column=3, padx=10)

        ttk.Label(self.root, text="Enter Token(s) (one per line):").pack(anchor='w', padx=10)
        self.token_input = tk.Text(self.root, height=3, width=110)
        self.token_input.pack(padx=10)

        ttk.Label(self.root, text="Channel ID(s) (comma-separated):").pack(anchor='w', padx=10)
        self.channel_entry = ttk.Entry(self.root, width=110)
        self.channel_entry.pack(padx=10)

        ttk.Label(self.root, text="Select Message Type:").pack(anchor='w', padx=10)
        self.message_mode = tk.StringVar(value="custom")
        ttk.Radiobutton(self.root, text="Custom Message", variable=self.message_mode, value="custom", command=self.toggle_message_mode).pack(anchor='w', padx=20)
        ttk.Radiobutton(self.root, text="Random Messages", variable=self.message_mode, value="random", command=self.toggle_message_mode).pack(anchor='w', padx=20)

        ttk.Label(self.root, text="Custom Message:").pack(anchor='w', padx=10)
        self.message_entry = ttk.Entry(self.root, width=110)
        self.message_entry.pack(padx=10)

        ttk.Label(self.root, text="Random Messages (each line is a new message):").pack(anchor='w', padx=10)
        self.random_message_text = tk.Text(self.root, height=3, width=110)
        self.random_message_text.pack(padx=10)
        self.random_message_text.configure(state='disabled')

        ttk.Label(self.root, text="Select Token Mode:").pack(anchor='w', padx=10)
        self.mode = tk.StringVar(value="user")
        ttk.Combobox(self.root, textvariable=self.mode, values=["user", "bot", "both"], state="readonly").pack(padx=10, fill='x')

        ttk.Label(self.root, text="Delay between messages (seconds):").pack(anchor='w', padx=10)
        self.delay = tk.DoubleVar(value=4)
        self.delay_slider = ttk.Scale(self.root, from_=4, to=300, variable=self.delay, orient='horizontal', command=self.update_delay_label)
        self.delay_slider.pack(padx=10, fill='x')
        self.delay_label = ttk.Label(self.root, text="4.0 seconds")
        self.delay_label.pack(padx=10, anchor='w')

        ttk.Label(self.root, text="Log Output:").pack(anchor='w', padx=10)
        log_frame = tk.Frame(self.root)
        log_frame.pack(padx=10, pady=5, fill='both', expand=True)

        self.log_box = tk.Text(log_frame, height=5, width=110, state='disabled', wrap='none')
        yscroll = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_box.yview)
        xscroll = ttk.Scrollbar(log_frame, orient='horizontal', command=self.log_box.xview)
        self.log_box.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.log_box.grid(row=0, column=0, sticky='nsew')
        yscroll.grid(row=0, column=1, sticky='ns')
        xscroll.grid(row=1, column=0, sticky='ew')
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

    def update_delay_label(self, val):
        val = float(val)
        self.delay_label.config(text=f"{val:.1f} seconds")

    def toggle_message_mode(self):
        mode = self.message_mode.get()
        if mode == "custom":
            self.message_entry.configure(state='normal')
            self.random_message_text.configure(state='disabled')
        else:
            self.message_entry.configure(state='disabled')
            self.random_message_text.configure(state='normal')

    def log(self, text):
        self.log_box.configure(state='normal')
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.configure(state='disabled')
        self.log_box.see(tk.END)

    def quit_program(self):
        self.should_quit = True
        self.is_running = False
        self.root.destroy()

    def send_messages_thread(self, token, channels, messages):
        client = discum.Client(token=token, log=False)
        self.token_clients[token] = client
        counter = 1

        while self.is_running and not self.should_quit:
            for channel in channels:
                if not self.is_running or self.should_quit:
                    break
                message = random.choice(messages) if self.message_mode.get() == "random" else messages[0]
                try:
                    client.sendMessage(channel, message)
                    self.log(f"Token #{token[:6]}... -> Sent #{counter}: {message}")
                    counter += 1
                    time.sleep(self.delay.get())
                except Exception as e:
                    self.log(f"Error sending message: {e}")
                time.sleep(1)

    def start_sending(self):
        self.is_running = True
        self.should_quit = False

        tokens = self.token_input.get("1.0", tk.END).strip().split("\n")
        channels = self.channel_entry.get().split(',')
        if self.message_mode.get() == "custom":
            messages = [self.message_entry.get()]
        else:
            messages = self.random_message_text.get("1.0", tk.END).strip().split("\n")

        self.threads = []
        for token in tokens:
            thread = threading.Thread(target=self.send_messages_thread, args=(token.strip(), channels, messages))
            thread.start()
            self.threads.append(thread)

        self.log("Started sending messages.")

    def pause_sending(self):
        self.is_running = False
        self.log("Paused sending messages.")

    def stop_sending(self):
        self.should_quit = True
        self.is_running = False
        self.log("Stopped sending messages.")

if __name__ == '__main__':
    root = tk.Tk()
    app = DiscordMessenger(root)
    root.mainloop()
