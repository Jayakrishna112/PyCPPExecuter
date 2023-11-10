from setuptools import setup, find_packages
import platform
import os
import sys
try:
    import winreg
except ImportError:
    winreg = None


def user_path_setter(path):
    variable_name = "Min_gw_library"
    variable_value = os.path.join(path, "\\MinGW\\bin")

    key = winreg.HKEY_CURRENT_USER

    try:
        with winreg.OpenKey(key, r"Environment", 0, winreg.KEY_WRITE) as environment_key:
            winreg.SetValueEx(environment_key, variable_name,
                              0, winreg.REG_SZ, variable_value)

        print(
            f"User environment variable '{variable_name}' added with value '{variable_value}'")
    except Exception as e:
        print(f"Error adding user environment variable: {e}")


def compiler_installer():
    import git
    from tqdm import tqdm
    os_type = platform.system()
    try:
        return_code = os.system("gcc --version")
    except Exception as e:
        print('Exceptions has occured ', e)
    if return_code != 0:
        if os_type == "Windows":
            repo_url = 'https://github.com/Jayakrishna112/Min-gw.git'
            local_directory = os.path.dirname(sys.executable)
            progress_bar = None

            def progress_callback(op_code, cur_count, max_count=None, message=''):
                global progress_bar
                if progress_bar is None:
                    progress_bar = tqdm(
                        total=max_count, unit='objects', position=0, leave=True)
                progress_bar.update(cur_count - progress_bar.n)
                if op_code & git.remote.RemoteProgress.END:
                    progress_bar.close()
            try:
                repo = git.Repo.clone_from(
                    repo_url, local_directory, progress=progress_callback)
                user_path_setter(local_directory)
            except git.GitCommandError as e:
                print(f"Failed to clone the repository: {e}")
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


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='PyCPPExecuter',
    version='1.1.2',
    description="This is a module that uses python interface to execute the c/c++ programs and perform actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PyCPPExecuter',
    author="JayaKrishna",
    author_email="jayakrishnamarni1234@gmail.com",
    license="MIT",
    packages=find_packages(where="pycppexecuter"),
    install_requires=['python-git', 'tqdm'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0"],
    },
    python_requires=">=3.10"
)

compiler_installer()
