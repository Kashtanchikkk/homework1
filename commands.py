import os
from pathlib import Path
from vfs import VirtualFileSystem


def execute_command(vfs, command):
    parts = command.split()

    if len(parts) == 0:
        return

    cmd = parts[0]

    if cmd == "ls":
        print("\n".join(vfs.list_files()))
    elif cmd == "cd":
        if len(parts) > 1:
            vfs.change_directory(parts[1])
        else:
            print("cd: missing operand")
    elif cmd == "tail":
        if len(parts) > 1:
            file_path = Path(vfs.current_path) / parts[1]
            if os.path.isfile(file_path):
                content = vfs.read_file(parts[1])
                lines = content.splitlines()
                print("\n".join(lines[-10:]))
            else:
                print(f"tail: {parts[1]}: No such file")
        else:
            print("tail: missing operand")
    elif cmd == "rm":
        if len(parts) > 1:
            vfs.remove_file(parts[1])
        else:
            print("rm: missing operand")
    elif cmd == "uname":
        print("emulator")
    elif cmd == "exit":
        print("Exiting emulator...")
        exit(0)
    else:
        print(f"{cmd}: command not found")
