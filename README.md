# passwordboy

A simple, CLI password manager.

It doesn't interface with your browser, so it can't autofill logins for you. But, if you're worried about giving your passwords to a third party and trusting them not to lose 'em (which, if stored locally, may already be a solved issue), then this guy is neat.

Honestly, you're probably better served looking into browser-based plugins. But I use this, and I had fun making it.

This program is meant to be placed somewhere in your system's path, takes simple commands like "passwordboy add Gmail [account] [password]" and interfaces with its own textfile-based, insecure database to add, remove, read and modify your various account details. You can create notes for accounts, and keep the answers to security questions, too (thank god those are finally going out of style). The program attempts to make it easy (aside of entering your passwords *for* you) to open up any account you might barely remember.

An important note: this program works for me because malicious hackers don't know I have it. If it ever becomes popular (it won't), don't use it. It's not secure. It's better than post-it notes only because it's an automated filing system, and might actually be worse because it's on your machine, open to the Internet.
