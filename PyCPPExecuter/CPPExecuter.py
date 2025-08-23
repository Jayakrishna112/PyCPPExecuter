import os
import sys
import subprocess
import shutil


class CPPExecuter:
    def __init__(self, lang: str = 'CPP'):
        """
        lang:str -> is the parameter which is used to specify the input language
        possible values are C, CPP
        defalut: CPP

        **Note**: please use the escape sequesce with a added forward slash
        example: "\n" as "\\n"
        """
        self.lang = lang
        path = os.path.join(os.path.dirname(
            sys.executable), 'CPPExecuter_files')
        if not os.path.exists(path):
            os.mkdir(path)
        self.cpp_code = os.path.join(path, 'cpp_code.cpp')
        self.cpp_exe = os.path.join(path, 'cpp_exe')
        self.c_code = os.path.join(path, 'c_code.c')
        self.c_exe = os.path.join(path, 'c_exe')
        # self.compile_output = os.path.join(path, 'compile_output.txt')
        # self.compile_error = os.path.join(path, 'compile_error.txt')
        # self.execution_error = os.path.join(path, 'execution_error.txt')
        # self.syntax_error = os.path.join(path, 'syntax_error.txt')
        # self.object_file_error = os.path.join(path, 'object_file_error.txt')
        # self.assembly_error = os.path.join(path, 'assembly_gen_error.txt')
        self._check()
        self.compiler = ''

    def _check(self):
        if self.lang not in ['C', 'CPP']:
            raise ValueError('The lang argument should be either C or CPP')

    def detect_compiler(self):
        if self.lang == 'CPP':
            if shutil.which('g++'):
                self.compiler = 'g++'
            elif shutil.which('clang++'):
                self.compiler = 'clang++'
        elif self.lang == 'C':
            if shutil.which('gcc'):
                self.compiler = 'gcc'
            elif shutil.which('clang'):
                self.compiler = 'clang'

    def compile(self, file_path=None, code=None, save_exe=False, path_to_exe=None, flags=''):
        """
        compile is used to compile the code specifiedd either c or c++ code

        file_path: str -> is the argument of filename or the path where source code is located
        default : None

        code: str -> is the argument of the code that need to be compiled
        default : None

        path_to_exe: str, optional-> is the path to save the .exe generated file after compiling the code
        default : None

        flags: str, optional-> is the different types of flags to be used in 'g++/gcc [flags] filename.cpp/.c'
        default : ''

        """

        if file_path is None and code is None:
            raise ValueError('Either file with code or code should be passed')

        self.detect_compiler()
        if file_path is None:
            if self.lang == 'CPP':
                with open(self.cpp_code, "w") as f:
                    f.write(code)
                self.check_code_syntax(self.cpp_code)
                run_list = [str(self.compiler), str(
                    self.cpp_code), '-o', str(self.cpp_exe)]
            elif self.lang == 'C':
                with open(self.c_code, "w") as f:
                    f.write(code)
                self.check_code_syntax(self.c_code)
                run_list = [str(self.compiler), str(
                    self.c_code), '-o', str(self.c_exe)]

        elif file_path is not None:
            self.check_code_syntax(file_path)
            if self.lang == 'CPP':
                run_list = [str(self.compiler), str(
                    file_path), '-o', str(self.cpp_exe)]
            elif self.lang == 'C':
                run_list = [str(self.compiler), str(
                    file_path), '-o', str(self.c_exe)]

        if flags != '':
            run_list.insert(2, str(flags))

        try:
            compile_result = subprocess.run(run_list,
                                            capture_output=True,
                                            text=True,
                                            check=True)
            if compile_result.returncode == 0:
                print('Compilation is successful')
        except subprocess.CalledProcessError as e:
            print('Error in the Compilation of the code: ')
            print(e.stderr)
        except Exception as e:
            print(e)

        if save_exe:
            if self.lang == 'CPP':
                with open(path_to_exe, 'w') as f:
                    with open(self.cpp_exe, 'r') as exe_file:
                        output = exe_file.read()
                        f.write(output)
            else:
                with open(path_to_exe, 'w') as f:
                    with open(self.c_exe, 'r') as exe_file:
                        output = exe_file.read()
                        f.write(output)

    def execute(self, file_path: str = None):
        """
        execute function is used to execute the previosly compiled code or the .exe file specified

        file_path: str -> optional, it is used to specify the path of the file to execute
        default: None

        """
        temp_path = None
        if file_path is not None:
            self._check_file_exists(file_path)
            temp_path = self.cpp_exe
            self.cpp_exe = file_path
        if self.lang == 'CPP':
            run_list = [str(self.cpp_exe)]
        else:
            run_list = [str(self.c_exe)]
        try:
            result = subprocess.run(run_list,
                                    check=True,
                                    text=True,
                                    shell=False)
            if temp_path:
                self.cpp_exe = temp_path
        except subprocess.CalledProcessError as e:
            print('Error while execting the executable file: ', e)
            if temp_path:
                self.cpp_exe = temp_path
        except Exception as e:
            print(e)
            if temp_path:
                self.cpp_exe = temp_path

    def check_code_syntax(self, file_path: str) -> None:
        """
        check_code_syntax is used to check the syntax of the code specified

        file_path: str -> the file path to check the syntax of the code

        """
        try:
            result = subprocess.run([str(self.compiler), '-fsyntax-only', str(file_path)],
                                    capture_output=True,
                                    text=True,
                                    check=True,
                                    shell=False)

        except subprocess.CalledProcessError as e:
            print('The code has syntax errors. Resolve them by checking the errors:')
            print(e.stderr)
        except Exception as e:
            print('Some error has occured:')
            print(e)

    def _check_file_exists(self, file_path):
        if not os.path.exists(file_path):
            raise ValueError('The specified file does not exist.')

    def create_object_file(self, file_path=None, code=None, path=None):
        """
        create_object_file is used to create the object file of the code specified

        path: str -> path to save the object file with .o extension
        default: None

        file_path: str -> The souce code file path
        default: None

        code: str -> The souce code of the program
        default: None
        """

        if path is None:
            raise ValueError('Path must be specified to save the file')
        if file_path is None and code is None:
            raise ValueError('Either a file or code must be specified')
        if file_path is not None:
            try:
                result = subprocess.run(
                    [str(self.compiler), '-c', str(file_path), '-o', str(path)],
                    shell=False,
                    check=True)
            except subprocess.CalledProcessError as e:
                print('Error while generating the object file: ', e)
            except Exception as e:
                print('Caught an exception while generating object file:', e)
            except OSError as e:
                print('OSError has occurred:', e)
        else:
            with open(self.cpp_code, 'w') as f:
                f.write(code)
            try:
                result = subprocess.run(
                    [str(self.compiler), '-c',
                     str(self.cpp_code), '-o', str(path)],
                    shell=False,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print('Error while generating the object file: ', e)
            except Exception as e:
                print('Caught an exception while generating object file:', e)

    def create_assembly_code(self, file_path=None, code=None, path=None):
        """
        create_assembly_code is used to create the assembly code of the code specified

        path: str -> path to save the object file with .s extension
        default: None

        file_path: str -> The souce code file path
        default: None

        code: str -> The souce code of the program
        default: None
        """

        if path is None:
            raise ValueError('Path must be specified to save the file')
        if file_path is None and code is None:
            raise ValueError('Either a file or code must be specified')
        if file_path is not None:
            try:
                result = subprocess.run(
                    [str(self.compiler), '-S', str(file_path), '-o', str(path)],
                    shell=False,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print('Error while generating the assembly file: ', e)
            except Exception as e:
                print('Caught an exception while generating assembly code:', e)
            except OSError as e:
                print('OSError has occurred:', e)
        else:
            with open(self.cpp_code, 'w') as f:
                f.write(code)
            try:
                result = subprocess.run(
                    [str(self.compiler), '-S',
                     str(self.cpp_code), '-o', str(path)],
                    shell=False,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print('Error while generating the assembly file: ', e)
            except Exception as e:
                print('Caught an exception while generating assembly code:', e)
