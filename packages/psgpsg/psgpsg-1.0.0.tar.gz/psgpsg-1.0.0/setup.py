import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="psgpsg",
    version="1.0.0",
    author="PySimpleGUI",
    author_email="PySimpleGUI@PySimpleGUI.org",
    description="Runs sg.main() using whatever default PySimpleGUI.py your system picks up.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/PySimpleGUI/PySimpleGUI",
    packages=['psgpsg'],
    install_requires=['PySimpleGUI'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Utilities",
        "Operating System :: OS Independent"
    ],
    package_data={"":["*.ico"]},
    entry_points={
        'gui_scripts': [
            'psgpsg=psgpsg.psgpsg:main_entry_point'
        ],
    },
)
