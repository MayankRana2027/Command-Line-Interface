"""
Command implementations for CCLI
Contains all command execution logic
"""

import os
import shutil
import datetime
from pathlib import Path
import time
import getpass
import platform

class Commands:
    """Collection of all CCLI commands"""
    
    def __init__(self, env, output_callback):
        self.env = env
        self.output = output_callback
    
    def help(self, args):
        """Display help information"""
        help_text = """Available Commands:

FILE OPERATIONS:
  echo [TEXT]              - Display text
  cd [DIRECTORY]           - Change directory
  pwd                      - Print working directory
  ls / dir [PATH]          - List directory contents
  mkdir [DIR]              - Create directory
  rmdir [DIR]              - Remove directory
  touch [FILE]             - Create file
  rm / del [FILE]          - Remove file
  rename/mv [OLD] [NEW]    - Rename/move file
  cp/copy [SRC] [DEST]     - Copy file or directory
  find/search [PATH] [PAT] - Search for files by pattern
  size [PATH]              - Show file/directory size
  
TEXT OPERATIONS:
  read/cat/type [FILE]     - Read file contents
  write [FILE] [TEXT]      - Write to file
  append [FILE] [TEXT]     - Append text to file
  head [FILE] [N]          - Show first N lines (default 10)
  tail [FILE] [N]          - Show last N lines (default 10)
  wc [FILE]                - Word count (lines, words, chars)
  grep [PATTERN] [FILE]    - Search for pattern in file
  replace [FILE] [OLD] [N] - Replace old with new in file
  diff [FILE1] [FILE2]     - Compare two files
  cmp [FILE1] [FILE2]      - Compare files byte by byte
  
SYSTEM:
  tree [PATH]              - Display directory tree
  date                     - Show current date/time
  env [VAR] [VALUE]        - Show/set environment variables
  whoami                   - Show current user
  uname                    - Show system information
  
UTILITIES:
  calc [EXPRESSION]        - Calculate mathematical expression
  sleep [SECONDS]          - Pause for specified seconds
  history                  - Show command history
  last                     - Execute last command
  clear / cls              - Clear screen
  exit                     - Exit CCLI

"""
        self.output(help_text, 'info')
    
    def echo(self, args):
        """Echo text to output"""
        self.output(' '.join(args) + '\n', 'output')
    
    def cd(self, args):
        """Change directory"""
        if not args:
            self.output("Usage: cd DIRECTORY\n", 'error')
            return
        
        path = ' '.join(args).strip('"')
        try:
            os.chdir(path)
            self.env.current_dir = os.getcwd()
            self.output(f"Changed directory to: {self.env.current_dir}\n", 'success')
        except FileNotFoundError:
            self.output(f"cd: directory does not exist: {path}\n", 'error')
        except NotADirectoryError:
            self.output(f"cd: not a directory: {path}\n", 'error')
        except Exception as e:
            self.output(f"cd: {str(e)}\n", 'error')
    
    def pwd(self, args):
        """Print working directory"""
        self.output(f"{os.getcwd()}\n", 'output')
    
    def ls(self, args):
        """List directory contents"""
        try:
            path = args[0] if args else '.'
            items = os.listdir(path)
            if items:
                items.sort()
                for item in items:
                    full_path = os.path.join(path, item)
                    if os.path.isdir(full_path):
                        self.output(f"[DIR]  {item}\n", 'directory')
                    else:
                        self.output(f"[FILE] {item}\n", 'output')
            else:
                self.output("Directory is empty\n", 'info')
        except Exception as e:
            self.output(f"ls: {str(e)}\n", 'error')
    
    def mkdir(self, args):
        """Create directory"""
        if not args:
            self.output("Usage: mkdir DIRECTORY\n", 'error')
            return
        
        try:
            os.makedirs(args[0], exist_ok=True)
            self.output(f"Directory created: {args[0]}\n", 'success')
        except Exception as e:
            self.output(f"mkdir: {str(e)}\n", 'error')
    
    def rmdir(self, args):
        """Remove directory"""
        if not args:
            self.output("Usage: rmdir DIRECTORY\n", 'error')
            return
        
        try:
            if os.path.isdir(args[0]):
                shutil.rmtree(args[0])
                self.output(f"Directory deleted: {args[0]}\n", 'success')
            else:
                self.output(f"rmdir: not a directory: {args[0]}\n", 'error')
        except Exception as e:
            self.output(f"rmdir: {str(e)}\n", 'error')
    
    def touch(self, args):
        """Create empty file"""
        if not args:
            self.output("Usage: touch FILENAME\n", 'error')
            return
        
        try:
            Path(args[0]).touch()
            self.output(f"File created: {args[0]}\n", 'success')
        except Exception as e:
            self.output(f"touch: {str(e)}\n", 'error')
    
    def rm(self, args):
        """Remove file"""
        if not args:
            self.output("Usage: rm FILENAME\n", 'error')
            return
        
        try:
            if os.path.isfile(args[0]):
                os.remove(args[0])
                self.output(f"File deleted: {args[0]}\n", 'success')
            elif os.path.isdir(args[0]):
                self.output(f"rm: is a directory: {args[0]} (use rmdir)\n", 'error')
            else:
                self.output(f"rm: file does not exist: {args[0]}\n", 'error')
        except Exception as e:
            self.output(f"rm: {str(e)}\n", 'error')
    
    def rename(self, args):
        """Rename or move file"""
        if len(args) < 2:
            self.output("Usage: rename OLD_NAME NEW_NAME\n", 'error')
            return
        
        try:
            os.rename(args[0], args[1])
            self.output(f"Renamed: {args[0]} -> {args[1]}\n", 'success')
        except Exception as e:
            self.output(f"rename: {str(e)}\n", 'error')
    
    def read(self, args):
        """Read file contents"""
        if not args:
            self.output("Usage: read FILENAME\n", 'error')
            return
        
        try:
            with open(args[0], 'r') as f:
                content = f.read()
                self.output(content + '\n', 'output')
        except Exception as e:
            self.output(f"read: {str(e)}\n", 'error')
    
    def write(self, args):
        """Write to file"""
        if len(args) < 2:
            self.output("Usage: write FILENAME CONTENT\n", 'error')
            return
        
        try:
            with open(args[0], 'w') as f:
                f.write(' '.join(args[1:]) + '\n')
            self.output(f"Content written to: {args[0]}\n", 'success')
        except Exception as e:
            self.output(f"write: {str(e)}\n", 'error')
    
    def head(self, args):
        """Show first N lines of file"""
        if not args:
            self.output("Usage: head FILENAME [N]\n", 'error')
            return
        
        lines = 10
        if len(args) > 1:
            try:
                lines = int(args[1])
            except ValueError:
                self.output("head: invalid line count\n", 'error')
                return
        
        try:
            with open(args[0], 'r') as f:
                for i, line in enumerate(f):
                    if i >= lines:
                        break
                    self.output(line, 'output')
        except Exception as e:
            self.output(f"head: {str(e)}\n", 'error')
    
    def tail(self, args):
        """Show last N lines of file"""
        if not args:
            self.output("Usage: tail FILENAME [N]\n", 'error')
            return
        
        lines = 10
        if len(args) > 1:
            try:
                lines = int(args[1])
            except ValueError:
                self.output("tail: invalid line count\n", 'error')
                return
        
        try:
            with open(args[0], 'r') as f:
                all_lines = f.readlines()
                for line in all_lines[-lines:]:
                    self.output(line, 'output')
        except Exception as e:
            self.output(f"tail: {str(e)}\n", 'error')
    
    def tree(self, args):
        """Display directory tree"""
        path = args[0] if args else '.'
        
        def print_tree(directory, prefix='', depth=0):
            if depth > 3:
                return
            
            try:
                items = sorted(os.listdir(directory))
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    item_path = os.path.join(directory, item)
                    
                    connector = '└── ' if is_last else '├── '
                    self.output(f"{prefix}{connector}{item}\n", 'output')
                    
                    if os.path.isdir(item_path):
                        extension = '    ' if is_last else '│   '
                        print_tree(item_path, prefix + extension, depth + 1)
            except PermissionError:
                pass
        
        self.output(f"{os.path.abspath(path)}\n", 'output')
        print_tree(path)
    
    def date(self, args):
        """Show current date and time"""
        now = datetime.datetime.now()
        self.output(f"{now.strftime('%A, %B %d, %Y %I:%M:%S %p')}\n", 'output')
    
    def history(self, args):
        """Show command history"""
        if not self.env.command_history:
            self.output("No command history available.\n", 'info')
            return
        
        for i, cmd in enumerate(self.env.command_history, 1):
            self.output(f"{i}: {cmd}\n", 'output')
    
    def last(self, args):
        """Execute last command"""
        last_cmd = self.env.get_last_command()
        if last_cmd and last_cmd != 'last':
            self.output(f"Executing: {last_cmd}\n", 'info')
            return last_cmd
        else:
            self.output("No previous command to execute.\n", 'info')
            return None
    
    def clear(self, args):
        """Clear screen"""
        return 'CLEAR'
    
    def copy(self, args):
        """Copy file or directory"""
        if len(args) < 2:
            self.output("Usage: cp SOURCE DESTINATION\n", 'error')
            return
        
        try:
            src = args[0]
            dst = args[1]
            
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                self.output(f"File copied: {src} -> {dst}\n", 'success')
            elif os.path.isdir(src):
                shutil.copytree(src, dst)
                self.output(f"Directory copied: {src} -> {dst}\n", 'success')
            else:
                self.output(f"cp: source does not exist: {src}\n", 'error')
        except Exception as e:
            self.output(f"cp: {str(e)}\n", 'error')
    
    def find(self, args):
        """Find files by pattern"""
        if not args:
            self.output("Usage: find [PATH] PATTERN\n", 'error')
            return
        
        if len(args) == 1:
            path = '.'
            pattern = args[0]
        else:
            path = args[0]
            pattern = args[1]
        
        try:
            matches = []
            for root, dirs, files in os.walk(path):
                for name in files + dirs:
                    if pattern.lower() in name.lower():
                        full_path = os.path.join(root, name)
                        matches.append(full_path)
            
            if matches:
                for match in matches:
                    self.output(f"{match}\n", 'output')
                self.output(f"\nFound {len(matches)} match(es)\n", 'info')
            else:
                self.output(f"No matches found for: {pattern}\n", 'info')
        except Exception as e:
            self.output(f"find: {str(e)}\n", 'error')
    
    def size(self, args):
        """Show file or directory size"""
        if not args:
            self.output("Usage: size PATH\n", 'error')
            return
        
        def get_size(path):
            total = 0
            if os.path.isfile(path):
                return os.path.getsize(path)
            elif os.path.isdir(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            total += os.path.getsize(fp)
                return total
            return 0
        
        def format_size(size):
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} PB"
        
        try:
            path = args[0]
            size = get_size(path)
            self.output(f"{path}: {format_size(size)} ({size:,} bytes)\n", 'output')
        except Exception as e:
            self.output(f"size: {str(e)}\n", 'error')
    
    def wc(self, args):
        """Word count"""
        if not args:
            self.output("Usage: wc FILENAME\n", 'error')
            return
        
        try:
            with open(args[0], 'r') as f:
                content = f.read()
                lines = content.count('\n')
                words = len(content.split())
                chars = len(content)
                
                self.output(f"Lines: {lines}, Words: {words}, Characters: {chars}\n", 'output')
        except Exception as e:
            self.output(f"wc: {str(e)}\n", 'error')
    
    def grep(self, args):
        """Search for pattern in file"""
        if len(args) < 2:
            self.output("Usage: grep PATTERN FILENAME\n", 'error')
            return
        
        pattern = args[0]
        filename = args[1]
        
        try:
            with open(filename, 'r') as f:
                matches = []
                for i, line in enumerate(f, 1):
                    if pattern.lower() in line.lower():
                        matches.append((i, line.rstrip()))
                
                if matches:
                    for line_num, line in matches:
                        self.output(f"{line_num}: {line}\n", 'output')
                    self.output(f"\nFound {len(matches)} match(es)\n", 'info')
                else:
                    self.output(f"No matches found for: {pattern}\n", 'info')
        except Exception as e:
            self.output(f"grep: {str(e)}\n", 'error')
    
    def append(self, args):
        """Append text to file"""
        if len(args) < 2:
            self.output("Usage: append FILENAME CONTENT\n", 'error')
            return
        
        try:
            with open(args[0], 'a') as f:
                f.write(' '.join(args[1:]) + '\n')
            self.output(f"Content appended to: {args[0]}\n", 'success')
        except Exception as e:
            self.output(f"append: {str(e)}\n", 'error')
    
    def replace(self, args):
        """Replace text in file"""
        if len(args) < 3:
            self.output("Usage: replace FILENAME OLD_TEXT NEW_TEXT\n", 'error')
            return
        
        filename = args[0]
        old_text = args[1]
        new_text = args[2]
        
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            count = content.count(old_text)
            if count > 0:
                content = content.replace(old_text, new_text)
                with open(filename, 'w') as f:
                    f.write(content)
                self.output(f"Replaced {count} occurrence(s) of '{old_text}' with '{new_text}'\n", 'success')
            else:
                self.output(f"Text not found: {old_text}\n", 'info')
        except Exception as e:
            self.output(f"replace: {str(e)}\n", 'error')
    
    def env(self, args):
        """Show or set environment variables"""
        if not args:
            for key, value in self.env.variables.items():
                self.output(f"{key}={value}\n", 'output')
        elif len(args) == 1:
            value = self.env.get_variable(args[0])
            if value:
                self.output(f"{args[0]}={value}\n", 'output')
            else:
                self.output(f"Variable not set: {args[0]}\n", 'info')
        else:
            self.env.set_variable(args[0], ' '.join(args[1:]))
            self.output(f"Variable set: {args[0]}={' '.join(args[1:])}\n", 'success')
    
    def whoami(self, args):
        """Show current user"""
        try:
            username = getpass.getuser()
            self.output(f"{username}\n", 'output')
        except Exception as e:
            self.output(f"whoami: {str(e)}\n", 'error')
    
    def uname(self, args):
        """Show system information"""
        try:
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            
            self.output(f"System: {system}\n", 'output')
            self.output(f"Release: {release}\n", 'output')
            self.output(f"Version: {version}\n", 'output')
            self.output(f"Machine: {machine}\n", 'output')
        except Exception as e:
            self.output(f"uname: {str(e)}\n", 'error')
    
    def calc(self, args):
        """Calculate mathematical expression"""
        if not args:
            self.output("Usage: calc EXPRESSION\n", 'error')
            return
        
        expression = ' '.join(args)
        try:
            allowed_chars = set('0123456789+-*/().% ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                self.output(f"{expression} = {result}\n", 'output')
            else:
                self.output("calc: invalid characters in expression\n", 'error')
        except Exception as e:
            self.output(f"calc: {str(e)}\n", 'error')
    
    def sleep(self, args):
        """Sleep for specified seconds"""
        if not args:
            self.output("Usage: sleep SECONDS\n", 'error')
            return
        
        try:
            seconds = float(args[0])
            self.output(f"Sleeping for {seconds} seconds...\n", 'info')
            time.sleep(seconds)
            self.output("Done!\n", 'success')
        except ValueError:
            self.output("sleep: invalid number\n", 'error')
        except Exception as e:
            self.output(f"sleep: {str(e)}\n", 'error')
    
    def alias(self, args):
        """Create or show aliases"""
        if not args:
            if self.env.aliases:
                for name, command in self.env.aliases.items():
                    self.output(f"{name}='{command}'\n", 'output')
            else:
                self.output("No aliases defined\n", 'info')
        elif len(args) == 1:
            command = self.env.get_alias(args[0])
            if command:
                self.output(f"{args[0]}='{command}'\n", 'output')
            else:
                self.output(f"Alias not found: {args[0]}\n", 'info')
        else:
            name = args[0]
            command = ' '.join(args[1:])
            self.env.set_alias(name, command)
            self.output(f"Alias created: {name}='{command}'\n", 'success')
    
    def diff(self, args):
        """Compare two files"""
        if len(args) < 2:
            self.output("Usage: diff FILE1 FILE2\n", 'error')
            return
        
        try:
            with open(args[0], 'r') as f1, open(args[1], 'r') as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
                
                differences = []
                max_lines = max(len(lines1), len(lines2))
                
                for i in range(max_lines):
                    line1 = lines1[i].rstrip() if i < len(lines1) else None
                    line2 = lines2[i].rstrip() if i < len(lines2) else None
                    
                    if line1 != line2:
                        if line1 is None:
                            self.output(f"{i+1}a: + {line2}\n", 'success')
                            differences.append(i)
                        elif line2 is None:
                            self.output(f"{i+1}d: - {line1}\n", 'error')
                            differences.append(i)
                        else:
                            self.output(f"{i+1}c: - {line1}\n", 'error')
                            self.output(f"{i+1}c: + {line2}\n", 'success')
                            differences.append(i)
                
                if not differences:
                    self.output("Files are identical\n", 'info')
                else:
                    self.output(f"\n{len(differences)} difference(s) found\n", 'info')
        except Exception as e:
            self.output(f"diff: {str(e)}\n", 'error')
    
    def cmp(self, args):
        """Compare files byte by byte"""
        if len(args) < 2:
            self.output("Usage: cmp FILE1 FILE2\n", 'error')
            return
        
        try:
            with open(args[0], 'rb') as f1, open(args[1], 'rb') as f2:
                byte1 = f1.read(1)
                byte2 = f2.read(1)
                pos = 1
                
                while byte1 and byte2:
                    if byte1 != byte2:
                        self.output(f"Files differ at byte {pos}\n", 'error')
                        return
                    byte1 = f1.read(1)
                    byte2 = f2.read(1)
                    pos += 1
                
                if byte1 or byte2:
                    self.output("Files have different lengths\n", 'error')
                else:
                    self.output("Files are identical\n", 'success')
        except Exception as e:
            self.output(f"cmp: {str(e)}\n", 'error')