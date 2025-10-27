import argparse

def parse():
    """ Parse the CLI args """
    p = argparse.ArgumentParser(prog="CLI Code Analyzer", description="Analyzes the python scripts dependencies and structure in the projects ")
    p.add_argument("--path","-p", required=True, help="Relative/Absolute Path to the project directory")
    p.add_argument("--mode","-m", choices=["all","one","select"],default="all", help="Mode: analyze all scripts, one script, or selected scripts")
    p.add_argument("--file",'-f',help="Path to the single script (only in one mode)")
    p.add_argument("--files,'-fs", help="List of selected scripts (used in 'select' mode) with the space seperated")
    p.add_argument("--verbose","-v", action="store_true", help="With Docstrings")
    
    return p.parse_args()
