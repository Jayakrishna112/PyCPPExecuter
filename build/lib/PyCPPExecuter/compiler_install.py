import platform
import os
import sys
try:
    import winreg
except ImportError:
    winreg = None


def user_path_setter(path):
    key_path = r"Environment"
    key = winreg.HKEY_CURRENT_USER

    try:
        path = os.path.join(path, r'Min-gw-main\bin')
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as environment_key:
            current_path, _ = winreg.QueryValueEx(environment_key, "Path")
            new_path_list = current_path.split(os.pathsep) + [path]
            new_path_string = os.pathsep.join(new_path_list)

            winreg.SetValueEx(environment_key, "Path", 0,
                              winreg.REG_EXPAND_SZ, new_path_string)

        print('Please Restart Your System')
    except Exception as e:
        print(f"Error modifying user PATH variable: {e}")


def compiler_installer():
    os_type = platform.system()
    try:
        return_code = os.system("gcc --version")
    except Exception as e:
        print('Exceptions has occured ', e)
    if return_code != 0:
        if os_type == "Windows":
            os.system("pip install requests")
            os.system("pip install tqdm")
            import requests
            from tqdm import tqdm
            import zipfile
            zip_url = 'https://github.com/Jayakrishna112/Min-gw/archive/refs/heads/main.zip'
            path = os.path.dirname(sys.executable)
            zip_file = os.path.join(path, 'Min-gw.zip')
            try:
                response = requests.get(zip_url, stream=True)
            except requests.exceptions.RequestException as e:
                print('Error downloading with error: %s' % e)
            total_size = int(response.headers.get('content-length', 0))
            unit_size = 1024
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            with open(zip_file, 'wb') as out_file:
                for data in response.iter_content(unit_size):
                    progress_bar.update(len(data))
                    out_file.write(data)
            progress_bar.close()
            extract_to = os.path.join(path, 'Min-gw')
            os.makedirs(os.path.dirname(extract_to), exist_ok=True)

            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            os.remove(zip_file)
            user_path_setter(extract_to)
        elif os_type == "Linux":
            try:
                status = os.system('sudo apt update')
                if status == 0:
                    status = os.system('sudo apt install gcc')
                if status == 0:
                    status = os.system('sudo apt-get g++')
            except Exception as e:
                print('Error in installing gcc compiler and error is', e)
        elif os_type == "Darwin":
            try:
                commands = ['/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', 'brew update',
                            'brew install gcc', 'brew link gcc', 'brew link g++']
                for command in commands:
                    status = os.system(command)
                    if status != 0:
                        break
            except Exception as e:
                print(e)
