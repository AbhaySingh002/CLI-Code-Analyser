from pathlib import Path
from colorama import Fore,init
from Classes import analyze_file

init(autoreset=True)

def get_module_name(file:Path, root:Path)->str:
    """ Get the module name from the file path relative to the root """
    try:
        rel = file.relative_to(root).with_suffix('')
    except ValueError as e:
        raise AssertionError(f"{Fore.RED}File {Fore.GREEN}{file}{Fore.RED} is not under root {Fore.GREEN}{root} : {Fore.LIGHTCYAN_EX}{e}")
    return rel.as_posix().replace('/','.')


def find_dependecies(root: Path, selected= None, verbose =False):
    """ Finds all the dependencies among the .py s"""
    assert isinstance(root, Path), f"{Fore.LIGHTYELLOW_EX}Project_root must be the Path object"
    
    if selected:
        py_files = []
        for f in selected:
            assert isinstance(f, str), f"{Fore.LIGHTYELLOW_EX}Each selected file must be a string"
            if Path(f).is_absolute():
                full_path = Path(f)
            else:
                rel_path = f.lstrip('/')
                full_path = root/rel_path
                if not full_path.suffix == ".py":
                    full_path = full_path.with_suffix('.py')
            assert full_path.exists(), f"{Fore.LIGHTYELLOW_EX}File not found:{Fore.GREEN} {full_path}"
            py_files.append(full_path)
        
        assert py_files, f"{Fore.LIGHTYELLOW_EX}No valid files"
            
    else:
        py_files = list(root.rglob("*.py"))
        assert py_files, f"{Fore.LIGHTYELLOW_EX}No Python files found in {Fore.GREEN}{root}"
    
    
    top_module = set()
    for f in py_files:
        assert isinstance(f, Path), f"{Fore.LIGHTYELLOW_EX} Each py_file must be the Path File"
        mod = get_module_name(f,root)
        assert isinstance(mod, str), f"{Fore.LIGHTYELLOW_EX}Module name must be String"
        top = mod.split('.')[0]
        top_module.add(top)
        
    
    dependencies = {}
    for f in py_files:
        name = get_module_name(f,root)
        imports,classes, functions, module_doc = analyze_file(f,verbose)
        local_imports = [imp for imp in imports if imp in top_module]
        external_imports = [imp for imp in imports if imp not in top_module]
        dependencies[name] = {
            "path": f,
            "local_imports": local_imports,
            "external_imports": external_imports,
            "classes": classes,
            "functions": functions,
            "doc": module_doc,
        }
        assert name in dependencies, f"{Fore.LIGHTYELLOW_EX} Failed to add the dependency for {Fore.GREEN}{name}"
    
    assert dependencies, f"{Fore.LIGHTYELLOW_EX}No Dependencies Built"
    return dependencies