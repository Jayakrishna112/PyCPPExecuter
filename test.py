from PyCPPExecuter import CPPExecuter

executer = CPPExecuter('CPP')

code = '''
#include <iostream>

int main()
{
    std::cout << "Hello, world!" << std::endl;
    return 0;
}'''

executer.compile(code=code)

executer.execute()
