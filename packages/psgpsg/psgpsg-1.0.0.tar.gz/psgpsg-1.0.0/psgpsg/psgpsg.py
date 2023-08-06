import PySimpleGUI as sg

"""
    Calls your default PySimpleGUI's main() function.
    
    This PyPI installed program enables you to type psgpsg from the command line
    and it will run whatever version of 

    Copyright 2022 PySimpleGUI
"""

version = '1.0.0'
__version__ = version.split()[0]

'''
Change log
    1.0.0   2-Sept-2022
        Initial Release

'''



def main():
    print('Your copy of PySimpleGUI is located at:',sg.__file__)
    sg.main()

def main_entry_point():
    main()

if __name__ == '__main__':
    main_entry_point()
