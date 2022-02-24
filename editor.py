import os
import tempfile
import threading
import subprocess
from Xlib import X
from config import config
from clipboard import copy
from constants import TARGET


running = threading.Event()


def open_editor(self, commands, compile_latex):
# def open_editor(commands, compile_latex):
    temp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False,
                                            suffix='.tex')

    config['open_editor'](commands, temp_file.name)

    latex = ""

    with open(temp_file.name, 'r') as reading_temp_file:
        latex = reading_temp_file.read().strip()

    os.remove(temp_file.name)

    if latex != '$$':
        if not compile_latex:
            svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <svg>
              <text
                 style="font-size:{config['font_size']}px; font-family:'{config['font']}';-inkscape-font-specification:'{config['font']}, Normal';fill:#000000;fill-opacity:1;stroke:none;"
                 xml:space="preserve"><tspan sodipodi:role="line" >{latex}</tspan></text>
            </svg>"""
            copy(svg, target=TARGET)
        elif compile_latex:
            copy(latex, target=TARGET)
    elif latex == '$$' or not latex:
        config['rofi'].error('No latex code found')


commands = '-u {}/.config/nvim/minimal-tex-init.lua'.format(config['home'])
