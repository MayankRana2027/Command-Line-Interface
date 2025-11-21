main.py - Application entry point
Simple launcher that initializes the GUI
Run this file to start the application

environment.py - Environment management
Handles environment variables
Manages command history
Stores command aliases

commands.py - Command implementations
Contains all command logic (help, echo, cd, ls, etc.)
Each command is a separate method
Easy to add new commands

executor.py - Command executor
Parses command lines
Tokenizes input (handles quotes)
Routes commands to appropriate handlers
Manages command aliases

gui.py - GUI interface
Handles all tkinter UI components
Manages input/output display
Handles command history navigation
Manages color-coded output
