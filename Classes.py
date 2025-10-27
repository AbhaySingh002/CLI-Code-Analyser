from pathlib import Path
from colorama import Fore,init,Style
import ast

init(autoreset=True)

def analyze_file(file_path:Path, verbose=False):
    """ Create the parse tree for the script and get the all its details"""
    with open(file_path,'r',encoding='utf-8') as f:
        source = f.read()
    
    assert source or verbose, f"{Fore.LIGHTYELLOW_EX}Empty file: {file_path}"
    tree =None
    try:
        tree= ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        raise AssertionError(f"{Fore.RED}Syntax error in {Fore.GREEN}{file_path}: {Fore.LIGHTCYAN_EX}{e}")
    
    imports,classes, functions = set(),[],[]
    module_doc = ast.get_docstring(tree) if verbose else None
    
    
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node,ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
        elif isinstance(node, ast.ClassDef):
            class_info ={"name": node.name}
            if verbose:
                class_info['doc'] = ast.get_docstring(node)
            classes.append(class_info)
        elif isinstance(node, ast.FunctionDef):
            func_info = {"name": node.name}
            if verbose:
                func_info["doc"] = ast.get_docstring(node)
            functions.append(func_info) 
    
    return imports,classes, functions, module_doc

def print_analysis(dependencies:dict, verbose=False):
    """ Print the all analysis"""
    if not dependencies:
        raise AssertionError(f"{Fore.RED}No files to analyze.")
    
    print(Fore.CYAN + Style.BRIGHT + "\n📂 Python Project Dependency Analysis\n")
    
    for script ,info in dependencies.items():
        display_name = script.replace('.', '/') + '.py'
        print(Fore.YELLOW + f"▶ {display_name}")
        print(Fore.GREEN + f"  Path: {info['path']}")
        print(Fore.BLUE + f"  Local Imports: {', '.join(info['local_imports']) or 'None'}")
        print(Fore.RED + f"  External Imports: {', '.join(info['external_imports']) or 'None'}")
        
        if info["classes"]:
            print(Fore.MAGENTA + "  Classes:")
            for c in info["classes"]:
                print("   • " + c["name"])
                if verbose and c.get("doc"):
                    print(Fore.LIGHTBLACK_EX + f"      └─ Doc: {c['doc']}")
        else:
            print(Fore.MAGENTA + "  Classes: None")

        # Print functions
        if info["functions"]:
            print(Fore.CYAN + "  Functions:")
            for f in info["functions"]:
                print("   • " + f["name"])
                if verbose and f.get("doc"):
                    print(Fore.LIGHTBLACK_EX + f"      └─ Doc: {f['doc']}")
        else:
            print(Fore.CYAN + "  Functions: None")

        if verbose and info.get("doc"):
            print(Fore.LIGHTWHITE_EX + f"  Module Docstring: {info['doc']}")
        print(Style.RESET_ALL)

    print(Fore.LIGHTWHITE_EX + "\n📊 Internal Dependency Graph (simplified):")
    print(Fore.LIGHTBLACK_EX + "-" * 60)
    for script, info in dependencies.items():
        for dep in info["local_imports"]:
            assert isinstance(dep, str), "Import dep must be str"
            print(Fore.GREEN + f"{script}" + Fore.WHITE + " → " + Fore.YELLOW + f"{dep}")
    print(Style.RESET_ALL)

    print(Fore.LIGHTWHITE_EX + "\n📦 External Dependencies Summary:")
    print(Fore.LIGHTBLACK_EX + "-" * 60)
    all_external = set()
    for info in dependencies.values():
        all_external.update(info["external_imports"])
    for ext in sorted(all_external):
        print(Fore.RED + f"• {ext}")
    print(Style.RESET_ALL)
        