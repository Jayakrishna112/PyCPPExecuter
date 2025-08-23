# PyCPPExecuter : An Python C++ Code Executer

PyCPPExecuter is a module used for Compiling and Executing the C/C++ code and also alows you to convert the code into the Assembly Code and to the Object File, also helps in checking the syntax of the the code. PyCPPExecuter is a robust for Executing the C/C++ code.

PyCPPExecuter is open source software relised by [Jaya Krishna Marni](https://www.linkedin.com/in/jaya-krishna-marni-649148227)

Full documentation and examples available at : https://jayakrishna112.github.io/docs.PyCPPExecuter/

## Important links

- HTML documentation: https://jayakrishna112.github.io/docs.PyCPPExecuter/
- Issue tracker: https://github.com/Jayakrishna112/PyCPPExecuter/issues
- Source code repository: https://github.com/Jayakrishna112/PyCPPExecuter

### Example Usage

```python
from PyCPPExecuter import CPPExecuter
executer = CPPExecuter()
code = """#include<iostream>
int main(){
    std::cout << "Hello World!";
    return 0;
}
"""
executer.compile(code = code)
executer.execute()
```
