import tkinter as tk
from tkinter import messagebox
import paramiko


# Function to install software on remote hosts
def install_software(remote_hosts, username, password, software_choices, software_var):
    # Record the software selected by the user
    selected_choices = [value for name, value in software_choices if software_var[name].get()]

    # Show an error message if the user did not fill in all the fields
    if not remote_hosts or not username or not password:
        messagebox.showinfo("Ошибка", "Одно или несколько полей не было заполнено")
        return

    # Set up the SSH client and add the key to trusted
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Iterate through the specified hosts, connect to them, and execute commands
        remote_hosts = [remote_host.strip() for remote_host in remote_hosts.split()]
        for remote_host in remote_hosts:
            ssh_client.connect(remote_host, username=username, password=password)

            # Show an error if the user has not selected any software
            if not selected_choices:
                messagebox.showinfo("Ошибка", "Вы не выбрали ни одного ПО")
                return

            for choice in selected_choices:
                # Depending on the user's choice, run the installation script on the remote computer
                if choice == 1:
                    install_command = "\\\\NK\\testssh\\tor.exe /S"
                elif choice == 2:
                    install_command = "\\\\NK\\testssh\\7z2301-x64.exe /S"
                elif choice == 3:
                    install_command = "\\\\NK\\testssh\\doublecmd-1.0.11.x86_64-win64.exe /VERYSILENT"

                ssh_client.exec_command(install_command)

        messagebox.showinfo("Успех", "Установка программного обеспечения выполнена успешно")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
    finally:
        # Close the SSH connection upon completion
        ssh_client.close()


# Main function
def main():
    # Create the graphical interface
    root = tk.Tk()
    root.title("Установка программного обеспечения")

    # Window dimensions
    window_width = 600
    window_height = 600

    # Calculate the position for centering
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_offset = (screen_width - window_width) // 2
    y_offset = (screen_height - window_height) // 2

    # Set window size and position
    root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

    # Interface elements
    remote_hosts_label = tk.Label(root, text="Адрес удаленного компьютера или несколько через пробел:")
    remote_hosts_label.pack()
    remote_hosts_entry = tk.Entry(root)
    remote_hosts_entry.pack()

    username_label = tk.Label(root, text="Имя пользователя:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    # Create checkboxes for software selection
    software_choices = [
        ("Tor", 1),
        ("7-Zip", 2),
        ("Double Commander", 3),
    ]

    software_var = {}
    for name, value in software_choices:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(root, text=name, variable=var)
        checkbox.pack()
        software_var[name] = var

    # Installation button
    install_button = tk.Button(
        root, text="Установить",
        command=lambda: install_software(
            remote_hosts_entry.get(),
            username_entry.get(),
            password_entry.get(),
            software_choices,
            software_var,
        )
    )
    install_button.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
