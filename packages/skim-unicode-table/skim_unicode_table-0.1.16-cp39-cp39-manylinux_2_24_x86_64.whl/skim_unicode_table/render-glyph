#!/usr/bin/env python3
import cairocffi as cairo
import pangocairocffi
from pangocffi import Alignment
from sys import stdin, stdout, argv

if __name__ == "__main__":
    text = stdin.readline().strip()

    PANGO_SCALE = 1024

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 128, 128)
    context = cairo.Context(surface)
    with context:
        context.set_source_rgb(1, 1, 1)  # White
        context.paint()
    context.translate(0,0)
    layout = pangocairocffi.create_layout(context)
    layout.set_alignment(Alignment.CENTER)
    # according to https://pangocairocffi.readthedocs.io/en/latest/modules.html#pangocairocffi.set_resolution ,
    # 1 pt font = 1.3 "cairo units" (I guess pixels)
    # - so, because we want sth. approximately 100 pixels tall => 76
    # - but as it turns out, that's still not small enough for some of the chars...
    layout.set_markup(f'<span font="65" font-family="sans-serif">{text}</span>')
    ink_extents, logical_extents = layout.get_extents()
    # print("(ix,iy): {}".format((ink_extents.x/PANGO_SCALE, ink_extents.y/PANGO_SCALE)))
    # print("(iw,ih): {}".format((ink_extents.width/PANGO_SCALE, ink_extents.height/PANGO_SCALE)))
    # print("(lx,ly): {}".format((logical_extents.x, logical_extents.y)))
    # print("(lw,lh): {}".format((logical_extents.width/PANGO_SCALE, logical_extents.y/PANGO_SCALE)))
    # to center this, we want:
    # tx+ix+iw+ix+tx == 128
    # => tx = (128-2*ix-iw)/2
    context.translate(
        int(round((128-2*ink_extents.x/PANGO_SCALE-ink_extents.width/PANGO_SCALE)/2)),
        int(round((128-2*ink_extents.y/PANGO_SCALE-ink_extents.height/PANGO_SCALE)/2)),
    )
    pangocairocffi.show_layout(context, layout)
    surface.write_to_png(argv[1] if len(argv) > 1 else stdout.buffer)
