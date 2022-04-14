import subprocess
from rofi import Rofi
from pathlib import Path
import importlib.util as util


def open_editor(commands, filename):
    """
    example arguments:
        commands: -u /home/user/.config/nvim/minimal-tex-init.lua
        filename: /tmp/lua_ELyKNz.tex
    """

    with open(filename, 'w') as file:
        file.write('$$')

    subprocess.Popen([
        'xfce4-terminal', '--disable-server', '-e',
        'nvim {} {}'.format(filename, commands)
    ]).wait()


def latex_document(latex):
    return r"""
    \documentclass{article}

    \usepackage[utf8]{inputenc}
    \usepackage[T1]{fontenc}
    \usepackage{textcomp}
    \usepackage{amsmath, amssymb}

    \begin{document}
    """ + latex + r"\end{document}"


def import_file(name, path):
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HOME = Path('~').expanduser()
rofi = Rofi()

config = {
    'rofi_theme': None,
    'font': 'Hack Nerd Font',
    'font_size': '12',
    'open_editor': open_editor,
    'latex_document': latex_document,
    'home': HOME,
    'rofi': rofi,
}

CONFIG_PATH = Path('~/.config/inkscape-shortcut-manager').expanduser()
# TODO: Add support for config file at ~/.config/inkscape-mappings/config.py
