from tkinter import Tk, Label, Button, filedialog
from backup import backup_manager


class BackupApp:
    def __init__(self, master):
        self.master = master
        master.title("File Backup and Recovery System")
        master.geometry("350x200")

        self.label = Label(master, text="Welcome to the Backup System!")
        self.label.pack()

        self.backup_button = Button(
            master, text="Backup Files", command=self.backup_files
        )
        self.backup_button.pack()

        self.recover_button = Button(
            master, text="Recover Files", command=self.recover_files
        )
        self.recover_button.pack()

    def backup_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Files to Backup")
        for file_path in file_paths:
            backup_manager.create_backup(file_path)

    def recover_files(self):
        from tkinter.simpledialog import askstring
        from backup.backup_manager import recover_file
        from db.database_handler import get_all_backups

        backups = get_all_backups()
        if not backups:
            print("No backups found!")
            return

        print("Available Backups:")
        for index, backup in enumerate(backups):
            print(
                f"{index + 1}. {backup['file_path']} (Backup Time: {backup['backup_time']})"
            )

        choice = askstring("Recover File", "Enter the number of the file to recover:")
        if (
            not choice
            or not choice.isdigit()
            or int(choice) < 1
            or int(choice) > len(backups)
        ):
            print("Invalid choice!")
            return

        selected_backup = backups[int(choice) - 1]

        recover_file(selected_backup)
        print(f"Recovered: {selected_backup['file_path']}")


if __name__ == "__main__":
    root = Tk()
    backup_app = BackupApp(root)
    root.mainloop()
