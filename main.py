from Dependency import find_dependecies
from colorama import Fore, init
from pathlib import Path
from CLI import parse
from Classes import print_analysis

import warnings
warnings.filterwarnings('ignore')

init(autoreset=True)

def main():
    """ Main Function"""
    args = parse()
    assert args.path , f"{Fore.LIGHTYELLOW_EX}Path argument is needed"
    
    root = Path(args.path).resolve()
    assert root.exists(), f"{Fore.LIGHTYELLOW_EX}Path not found: {Fore.GREEN}{root}"
    
    if args.mode == "one":
        assert args.file is not None, f"{Fore.LIGHTYELLOW_EX}Please provide --file / -f for 'one' mode "
        selected = [args.file]
    elif args.mode == "select":
        assert args.file is not None, f"{Fore.LIGHTYELLOW_EX}Please provide --files / -fs for 'select' mode "
        selected = args.files
    else:
        selected = None
        
    
    dependencies = find_dependecies(root, selected,verbose = args.verbose)
    print_analysis(dependencies,verbose=args.verbose)
if __name__=="__main__":
    main()