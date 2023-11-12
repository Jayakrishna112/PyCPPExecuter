import os
import winreg


def add_to_user_path(new_path):
    key_path = r"Environment"
    key = winreg.HKEY_CURRENT_USER

    try:
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as environment_key:
            current_path, _ = winreg.QueryValueEx(environment_key, "Path")
            new_path_list = [new_path] + current_path.split(os.pathsep)
            new_path_string = os.pathsep.join(new_path_list)

            winreg.SetValueEx(environment_key, "Path", 0,
                              winreg.REG_EXPAND_SZ, new_path_string)

        print(f"Added '{new_path}' to the user PATH variable.")
    except Exception as e:
        print(f"Error modifying user PATH variable: {e}")


new_path_to_add = r"C:\Users\user\anaconda3\envs\myidea\Min-gw\Min-gw-main\bin"
add_to_user_path(new_path_to_add)
