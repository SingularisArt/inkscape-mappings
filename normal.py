from Xlib import X, XK

# import text
# import styles
from clipboard import copy
from constants import TARGET
from editor import open_editor, commands


pressed = set()

events = []


def event_to_string(self, event):
    mods = []

    if event.state & X.ShiftMask:
        mods.append('Shift')

    if event.state & X.ControlMask:
        mods.append('Control')

    keycode = event.detail
    keysym = self.disp.keycode_to_keysym(keycode, 0)
    char = XK.keysym_to_string(keysym)

    return ''.join('{}+'.format(mod) for mod in mods) + (char if char else '?')


def replay(self):
    for event in events:
        self.inkscape.send_event(event, propagate=True)

    self.disp.flush()
    self.disp.sync()


def normal_mode(self, event, char):
    events.append(event)

    if event.type == X.KeyPress and char:
        pressed.add(event_to_string(self, event))
        return

    if event.type != X.KeyRelease:
        return

    handled = False

    if len(pressed) > 1:
        paste_style(self, pressed)
        handled = True
    elif len(pressed) == 1:
        ev = next(iter(pressed))
        handled = handle_single_key(self, ev)

    if not handled:
        replay(self)

    events.clear()
    pressed.clear()


def handle_single_key(self, ev):
    if ev == 'a':
        # Mouse
        self.press('m')
    elif ev == 's':
        # Pencil
        self.press('p')
    elif ev == 'd':
        # Delete
        self.press('Delete')
    elif ev == 'f':
        # Bezier
        self.press('b')
    elif ev == 'q':
        # 3D Boxes
        self.press('x')
    elif ev == 'w':
        # Spirals
        self.press('i')
    elif ev == 'e':
        # Ellipsis
        self.press('e')
    elif ev == 'r':
        # Rectangles
        self.press('r')
    elif ev == 't':
        # Add text
        open_editor(self, commands, compile_latex=False)
    elif ev == 'T':
        # Add compiled text
        open_editor(self, commands, compile_latex=True)
    elif ev == 'u':
        # Undo
        self.press('z', X.ControlMask)
    elif ev == 'x':
        # Snap
        self.press('percent', X.ShiftMask)
    else:
        # Not handled
        return False
    return True


def paste_style(self, combination):
    pt = 1.327
    w = 0.4 * pt
    thick_width = 0.8 * pt
    very_thick_width = 1.2 * pt
    chunky = 1.6 * pt

    style = {
        'stroke-opacity': 1,
    }

    # Line widths
    if 'h' in combination:
        style['stroke-width'] = w
    if 'j' in combination:
        w = thick_width
        style['stroke-width'] = w
    if 'k' in combination:
        w = very_thick_width
        style['stroke-width'] = w
    if 'l' in combination:
        w = chunky
        style['stroke-width'] = w

    # Line colors
    if 'a' in combination:
        style['fill'] = 'black'
        style['fill-opacity'] = 1
    if 's' in combination:
        style['fill'] = 'white'
        style['fill-opacity'] = 1
    if 'd' in combination:
        style['fill'] = 'black'
        style['fill-opacity'] = 0.2
    if 'f' in combination:
        style['stroke'] = 'blue'
        style['fill-opacity'] = 1
    if 'g' in combination:
        style['stroke'] = 'red'
        style['fill-opacity'] = 1

    # Line styles
    if 'q' in combination:
        style['stroke-dasharray'] = f'{w},{2*pt}'
    if 'w' in combination:
        style['stroke-dasharray'] = f'{3*pt},{3*pt}'

    # Line arrows
    if 'e' in combination:
        style['marker-end'] = f'url(#marker-arrow-{w})'
    if 'r' in combination:
        style['marker-start'] = f'url(#marker-arrow-{w})'
        style['marker-end'] = f'url(#marker-arrow-{w})'

    # Clear all styles
    if 'c' in combination:
        style['stroke'] = 'black'
        style['stroke-width'] = w
        style['fill'] = 'none'
        style['marker-end'] = 'none'
        style['marker-start'] = 'none'
        style['stroke-dasharray'] = 'none'

    # Start creation of the svg.
    # Later on, we'll write this svg to the clipboard, and send Ctrl+Shift+V to
    # Inkscape, to paste this style.

    svg = '''
          <?xml version="1.0" encoding="UTF-8" standalone="no"?>
          <svg>
          '''
    # If a marker is applied, add its definition to the clipboard
    # Arrow styles stolen from tikz

    if ('marker-end' in style and style['marker-end'] != 'none') or \
            ('marker-start' in style and style['marker-start'] != 'none'):
        svg += f'''
<defs id="marker-defs">
<marker
id="marker-arrow-{w}"
orient="auto-start-reverse"
refY="0" refX="0"
markerHeight="1.690" markerWidth="0.911">
  <g transform="scale({(2.40 * w + 3.87)/(4.5*w)})">
    <path
       d="M -1.55415,2.0722 C -1.42464,1.29512 0,0.1295 0.38852,0 0,-0.1295 -1.42464,-1.29512 -1.55415,-2.0722"
       style="fill:none;stroke:#000000;stroke-width:{0.6};stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:10;stroke-dasharray:none;stroke-opacity:1"
       inkscape:connector-curvature="0" />
   </g>
</marker>
</defs>
'''

    style_string = ';'.join('{}: {}'.format(key, value)
                            for key, value in sorted(style.items(),
                                                     key=lambda x: x[0]))
    svg += f'<inkscape:clipboard style="{style_string}" /></svg>'

    copy(svg, target=TARGET)
    self.press('v', X.ControlMask | X.ShiftMask)
