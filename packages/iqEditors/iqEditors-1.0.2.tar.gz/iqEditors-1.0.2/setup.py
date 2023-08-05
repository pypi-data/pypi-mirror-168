import setuptools

with open("README_pip.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="iqEditors",
    version="1.0.2",
    author="Alexander N Khilchenko",
    author_email="khan.programming@mail.ru",
    description="Основанные на QTextEdit продвинутые текстовые редакторы для PyQt5",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://gitflic.ru/project/iqstudio/iq-editors",
    packages=['iqEditors'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Russian",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Other Environment",
        "Topic :: Desktop Environment :: Gnome",
        "Topic :: Desktop Environment :: K Desktop Environment (KDE)",
        "Topic :: Desktop Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Typing :: Typed",
    ],
    python_requires='>=3.6',
)
