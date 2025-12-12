import os
import sys


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
        self.compile_output = os.path.join(path, 'compile_output.txt')
        self.compile_error = os.path.join(path, 'compile_error.txt')
        self.execution_error = os.path.join(path, 'execution_error.txt')
        self.syntax_error = os.path.join(path, 'syntax_error.txt')
        self.object_file_error = os.path.join(path, 'object_file_error.txt')
        self.assembly_error = os.path.join(path, 'assembly_gen_error.txt')
        self._check()

    def _check(self):
        if self.lang not in ['C', 'CPP']:
            raise ValueError('The lang argument should be either C or CPP')

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

        if self.lang == 'CPP':
            if file_path is None:
                with open(self.cpp_code, "w") as f:
                    f.write(code)
                self.check_code_syntax(self.cpp_code)
                command = f'g++ {self.cpp_code} {flags} -o {self.cpp_exe} >{self.compile_output} 2> {self.compile_error}'
            else:
                self._check_file_exists(file_path)
                self.check_code_syntax(file_path)
                command = f'g++ {file_path} {flags} -o {self.cpp_exe} >{self.compile_output} 2> {self.compile_error}'
        else:
            if file_path is None:
                with open(self.c_code, "w") as f:
                    f.write(code)
                self.check_code_syntax(self.c_code)
                command = f'gcc {self.c_code} {flags} -o {self.c_exe} >{self.compile_output} 2> {self.compile_error}'
            else:
                self._check_file_exists(file_path)
                self.check_code_syntax(file_path)
                command = f'gcc {file_path} {flags} -o {self.c_exe} >{self.compile_output} 2> {self.compile_error}'

        try:
            return_code = os.system(command)
            if return_code != 0:
                with open(self.compile_error, 'r') as f:
                    print(f.read())
            else:
                print('Compilation is successful')
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
            command = f'{self.cpp_exe} 2> {self.execution_error}'
        else:
            command = f'{self.c_exe} 2> {self.execution_error}'
        try:
            return_code = os.system(command)
            if return_code != 0:
                with open(self.execution_error, 'r') as f:
                    print(f.read())
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
        if self.lang == 'CPP':
            return_code = os.system(
                f'g++ -fsyntax-only {file_path} 2> {self.syntax_error}')
            if return_code:
                with open(self.syntax_error, 'r') as f:
                    print(
                        'The code has syntax errors. Resolve them by checking the errors:')
                    print(f.read())
        else:
            return_code = os.system(
                f'gcc -fsyntax-only {file_path} 2> {self.syntax_error}')
            if return_code:
                with open(self.syntax_error, 'r') as f:
                    print(
                        'The code has syntax errors. Resolve them by checking the errors:')
                    print(f.read())

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
                return_code = os.system(
                    f'g++ -c {file_path} -o {path} 2>{self.object_file_error}')
                if return_code != 0:
                    with open(self.object_file_error, 'r') as f:
                        error = f.read()
                    raise Exception(error)
            except Exception as e:
                print('Caught an exception while generating object file:', e)
            except OSError as e:
                print('OSError has occurred:', e)
        else:
            with open(self.cpp_code, 'w') as f:
                f.write(code)
            try:
                return_code = os.system(
                    f'g++ -c {self.cpp_code} -o {path} 2>{self.object_file_error}')
                if return_code != 0:
                    with open(self.object_file_error, 'r') as f:
                        error = f.read()
                    raise Exception(error)
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
                return_code = os.system(
                    f'g++ -S {file_path} -o {path} 2>{self.object_file_error}')
                if return_code != 0:
                    with open(self.object_file_error, 'r') as f:
                        error = f.read()
                    raise Exception(error)
            except Exception as e:
                print('Caught an exception while generating assembly code:', e)
            except OSError as e:
                print('OSError has occurred:', e)
        else:
            with open(self.cpp_code, 'w') as f:
                f.write(code)
            try:
                return_code = os.system(
                    f'g++ -S {self.cpp_code} -o {path} 2>{self.assembly_error}')
                if return_code != 0:
                    with open(self.assembly_error, 'r') as f:
                        error = f.read()
                    raise Exception(error)
            except Exception as e:
                print('Caught an exception while generating assembly code:', e)
