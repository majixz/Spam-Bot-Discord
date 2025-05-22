# MaJiX's Discord Spammer

A GUI-based tool to send automated messages to Discord channels using user or bot tokens. Built with Python and Tkinter, this tool allows you to configure tokens, channel IDs, message modes (custom or random), and delays, all from a single interface.

⚠️ **Warning:** This tool uses `discum` for user-token-based messaging, which violates [Discord's Terms of Service](https://discord.com/terms). Use it at your own risk. Only bot tokens should be used for legitimate automation.

## 🔧 Features

- Multiple token support (user, bot, or both)  
- Multiple channel targeting  
- Custom or random messages (one per line)  
- Adjustable delay between messages  
- Message log display  
- Start, Pause, Stop, and Quit controls  
- Delay slider (4 to 300 seconds)  
- Scrollable message log  

## 💻 Requirements

- Python 3.7+  
- `discum` (`pip install discum`)  
- `tkinter` (usually comes with Python)  

## 🚀 How to Run

1. Install dependencies:  
   ```bash
   pip install discum
Run the script:
Fill out the fields in the GUI:

Token(s): One per line (Bot/User)

Channel ID(s): Comma-separated list

Message Mode: Custom or Random (one per line)

Token Mode: user / bot / both

Delay: Slider from 4–300 sec

Click Start to begin sending.

🧠 Notes
Messages are sent one at a time per token

Delays are enforced between messages

Logs track every message per token

Fixed window size: 900x650

🛑 Legal Disclaimer
This project is for educational purposes only. Automating Discord user accounts is against their Terms of Service. Use of self-bots or user tokens may result in account bans. Use only bot tokens created via the Discord Developer Portal for legit automation.
