import argparse
import socket
import os
from vfs import VirtualFileSystem  # Изменён импорт
from commands import execute_command
import sys


def run_shell(vfs, start_script):
    # Выполнение команд из стартового скрипта
    if start_script and os.path.isfile(start_script):
        with open(start_script, 'r') as script:
            for line in script:
                execute_command(vfs, line.strip())

    # Запуск CLI
    while True:
        prompt = f"{socket.gethostname()}:{vfs.current_path}$ "
        try:
            command = input(prompt).strip()
            if command == "exit":
                print("Exiting shell...")
                break
            execute_command(vfs, command)
        except EOFError:  # Завершение при Ctrl+D
            print("\nExiting shell...")
            break


def main():
    parser = argparse.ArgumentParser(description="Virtual File System Shell Emulator")
    parser.add_argument("hostname", help="Hostname for prompt", nargs='?', default='mycomputer')
    parser.add_argument("vfs_zip", help="Path to the VFS ZIP file", nargs='?',
                        default='/Users/shadow/Documents/RTU_MIREA/2Курс/Configura/1/virtual_fs.zip')  # Изменено на ZIP
    parser.add_argument("start_script", help="Path to the startup script", nargs='?', default='start_script.txt')

    args = parser.parse_args()

    # Проверяем существование ZIP файла
    if not os.path.isfile(args.vfs_zip):
        print(f"Error: File {args.vfs_zip} does not exist.")
        sys.exit(1)

    # Создаём виртуальную файловую систему
    vfs = VirtualFileSystem(args.vfs_zip)

    # Запускаем оболочку
    run_shell(vfs, args.start_script)


if __name__ == "__main__":
    main()