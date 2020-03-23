---
title: Bash Shortcuts
date: '2013-02-20 23:16:13 +0800'
---

# 2013-02-20  Bash Shortcuts

CTRL Key Bound

```text
Ctrl + a - Jump to the start of the line
Ctrl + b - Move back a char
Ctrl + c - Terminate the command
Ctrl + d - Delete from under the cursor
Ctrl + e - Jump to the end of the line
Ctrl + f - Move forward a char
Ctrl + k - Delete to EOL
Ctrl + l - Clear the screen
Ctrl + r - Search the history backwards
Ctrl + R - Search the history backwards with multi occurrence
Ctrl + u - Delete backward from cursor
Ctrl + xx - Move between EOL and current cursor position
Ctrl + x @ - Show possible hostname completions
Ctrl + z - Suspend/ Stop the command 
```

ALT Key Bound

```text
Alt + < - Move to the first line in the history
Alt + > - Move to the last line in the history
Alt + ? - Show current completion list
Alt + * - Insert all possible completions
Alt + / - Attempt to complete filename
Alt + . - Yank last argument to previous command
Alt + b - Move backward
Alt + c - Capitalize the word
Alt + d - Delete word
Alt + f - Move forward
Alt + l - Make word lowercase
Alt + n - Search the history forwards non-incremental
Alt + p - Search the history backwards non-incremental
Alt + r - Recall command
Alt + t - Move words around
Alt + u - Make word uppercase
Alt + backspace - Delete backward from cursor 
```

More Special Key bindings

Here 2T means Press TAB twice. And $ is the bash prompt.

```text
$ 2T - Display all available commands(common)
$ string 2T - Display all available commands starting with string.
$ /2T - Show entire directory structure including hidden ones.
$ 2T - Show only sub-directories inside including hidden ones.
$ *2T - Show only sub-directories inside excluding hidden ones.
$ ~2T - Show all present users on system from "/etc/passwd"
$ $2T - Show all sys variables
$ @2T - Show all entries from "/etc/hosts"
$ =2T - List output like ls or dir
```

