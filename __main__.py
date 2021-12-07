import argparse, os, sys
from .config import ignore_list
from .diagram import DirStrucTree


def parse_args():
    
    description = '''Small tool to generate directory structure diagrams in the form of a tree chart.\n
    Output is in the form of the mermaid markdown language (see https://mermaid-js.github.io/mermaid/#/). 
    The root argument is the folder from which the diagram should be created. This is also the save path.'''

    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('-r', '--root', help='The root path of the folder where the diagram should start.')
    parser.add_argument('-i','--include_to_readme', default = False, type=bool, help='If the diagramm should be included in a README.md. Currently only .md is supported. Default = True')
    parser.add_argument('-d','--direction', default = "LR", help='Diagram flow. LR (Left right), TD (Top Down) and RL are supported. Default = LR')
    parser.add_argument('-md','--maxdepth', default = 4, type=int, help='Maximal folder depth. Default = 4')
    parser.add_argument('-il','--ignorelist',  nargs="+", default = [], help='List with files/folders to be ignores. Default = see config.py')

    args = parser.parse_args()
    
    return args


def main():
    
    inputs=parse_args()
    
    if not inputs.ignorelist:
        ignorelist = ignore_list
    else: 
        ignorelist = inputs.ignorelist
    
    root = inputs.root
    max_depth = inputs.maxdepth 
    
    if root is None:
        root = os.getcwd()
    else:
        if os.path.isdir(root) is False:
            print("Folder path '{}' does not exist. Exiting ...".format(root))
            sys.exit()


    if max_depth == 0:
        max_depth = 1

    DirStrucTree(root,
            ignorelist,
            files=True,
            include_to_readme=inputs.include_to_readme,
            direction=inputs.direction,
            max_folder_depth=max_depth)

    return 0


if __name__ == "__main__":
    main()
