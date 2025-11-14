"""
Command executor for CCLI
Handles command parsing and execution
"""

import time
from commands import Commands

class CommandExecutor:
    """Parses and executes commands"""
    
    def __init__(self, env, output_callback):
        self.env = env
        self.output = output_callback
        self.commands = Commands(env, output_callback)
    
    def execute(self, command_line):
        """Execute a command line"""
        if not command_line.strip():
            return
        
        tokens = self.tokenize(command_line)
        if not tokens:
            return
        
        cmd = tokens[0].lower()
        args = tokens[1:]
        
        # Check for alias
        if cmd in self.env.aliases:
            alias_cmd = self.env.aliases[cmd]
            command_line = alias_cmd + ' ' + ' '.join(args)
            tokens = self.tokenize(command_line)
            cmd = tokens[0].lower()
            args = tokens[1:]
        
        # Command mapping
        command_map = {
            'help': self.commands.help,
            'echo': self.commands.echo,
            'cd': self.commands.cd,
            'pwd': self.commands.pwd,
            'ls': self.commands.ls,
            'dir': self.commands.ls,
            'mkdir': self.commands.mkdir,
            'rmdir': self.commands.rmdir,
            'touch': self.commands.touch,
            'rm': self.commands.rm,
            'del': self.commands.rm,
            'rename': self.commands.rename,
            'mv': self.commands.rename,
            'read': self.commands.read,
            'cat': self.commands.read,
            'type': self.commands.read,
            'write': self.commands.write,
            'head': self.commands.head,
            'tail': self.commands.tail,
            'tree': self.commands.tree,
            'date': self.commands.date,
            'history': self.commands.history,
            'last': self.commands.last,
            'clear': self.commands.clear,
            'cls': self.commands.clear,
            'cp': self.commands.copy,
            'copy': self.commands.copy,
            'find': self.commands.find,
            'search': self.commands.find,
            'size': self.commands.size,
            'wc': self.commands.wc,
            'grep': self.commands.grep,
            'append': self.commands.append,
            'replace': self.commands.replace,
            'env': self.commands.env,
            'whoami': self.commands.whoami,
            'uname': self.commands.uname,
            'calc': self.commands.calc,
            'sleep': self.commands.sleep,
            'alias': self.commands.alias,
            'diff': self.commands.diff,
            'cmp': self.commands.cmp,
        }
        
        if cmd in command_map:
            try:
                start_time = time.time()
                result = command_map[cmd](args)
                return result
            except Exception as e:
                self.output(f"Error: {str(e)}\n", 'error')
        else:
            self.output(f"Unknown command: {cmd}. Type 'help' for available commands.\n", 'error')
    
    def tokenize(self, command_line):
        """Tokenize a command line respecting quotes"""
        tokens = []
        current = ''
        in_quotes = False
        
        for char in command_line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current:
                    tokens.append(current)
                    current = ''
            else:
                current += char
        
        if current:
            tokens.append(current)
        
        return tokens