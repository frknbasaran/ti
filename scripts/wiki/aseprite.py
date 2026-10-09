"""Minimal .aseprite reader: renders one frame (visible normal layers, cel and layer
opacity) to a PIL image. Enough for the game's character sheets; blend modes other
than normal are drawn as normal. Format reference:
https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md
"""
import struct
import zlib

from PIL import Image


def read(path):
    data = open(path, 'rb').read()
    (_size, magic, nframes, width, height, depth, flags) = struct.unpack_from('<IHHHHHI', data, 0)
    if magic != 0xA5E0:
        raise ValueError(f'{path}: not an aseprite file')
    transparent = data[28]
    off = 128
    layers, frames, tags, palette = [], [], [], {}
    for _ in range(nframes):
        frame_bytes, frame_magic, old_chunks = struct.unpack_from('<IHH', data, off)
        if frame_magic != 0xF1FA:
            raise ValueError(f'{path}: bad frame header')
        new_chunks = struct.unpack_from('<I', data, off + 12)[0]
        pos = off + 16
        cels = []
        for _ in range(new_chunks or old_chunks):
            chunk_size, chunk_type = struct.unpack_from('<IH', data, pos)
            body = pos + 6
            if chunk_type == 0x2004:  # layer
                lflags, ltype, child, _dw, _dh, blend, opacity = struct.unpack_from('<HHHHHHB', data, body)
                name_len = struct.unpack_from('<H', data, body + 16)[0]
                name = data[body + 18: body + 18 + name_len].decode('utf-8', 'replace')
                layers.append(dict(flags=lflags, type=ltype, child=child, opacity=opacity, name=name))
            elif chunk_type == 0x2005:  # cel
                layer, x, y, opacity, cel_type = struct.unpack_from('<HhhBH', data, body)
                q = body + 16
                if cel_type == 1:
                    cels.append(dict(layer=layer, link=struct.unpack_from('<H', data, q)[0]))
                elif cel_type in (0, 2):
                    w, h = struct.unpack_from('<HH', data, q)
                    raw = data[q + 4: pos + chunk_size]
                    if cel_type == 2:
                        raw = zlib.decompress(raw)
                    cels.append(dict(layer=layer, x=x, y=y, opacity=opacity, w=w, h=h, pixels=raw))
            elif chunk_type == 0x2019:  # palette
                _n, first, last = struct.unpack_from('<III', data, body)
                q = body + 20
                for i in range(first, last + 1):
                    eflags, r, g, b, a = struct.unpack_from('<HBBBB', data, q)
                    q += 6
                    if eflags & 1:
                        q += 2 + struct.unpack_from('<H', data, q)[0]
                    palette[i] = (r, g, b, a)
            elif chunk_type == 0x2018:  # tags
                count = struct.unpack_from('<H', data, body)[0]
                q = body + 10
                for _ in range(count):
                    start, end = struct.unpack_from('<HH', data, q)
                    q += 17
                    name_len = struct.unpack_from('<H', data, q)[0]
                    tags.append(dict(name=data[q + 2: q + 2 + name_len].decode('utf-8', 'replace'),
                                     start=start, end=end))
                    q += 2 + name_len
            pos += chunk_size
        frames.append(cels)
        off += frame_bytes
    return dict(w=width, h=height, depth=depth, flags=flags, transparent=transparent,
                layers=layers, frames=frames, tags=tags, palette=palette)


def _cel_image(doc, cel):
    w, h, px = cel['w'], cel['h'], cel['pixels']
    if doc['depth'] == 32:
        return Image.frombytes('RGBA', (w, h), px[: w * h * 4])
    if doc['depth'] == 16:
        return Image.frombytes('LA', (w, h), px[: w * h * 2]).convert('RGBA')
    out = bytearray()
    for index in px[: w * h]:
        out += b'\0\0\0\0' if index == doc['transparent'] else bytes(doc['palette'].get(index, (0, 0, 0, 0)))
    return Image.frombytes('RGBA', (w, h), bytes(out))


def _visible(doc, index):
    layers = doc['layers']
    if not layers[index]['flags'] & 1:
        return False
    level = layers[index]['child']
    for j in range(index - 1, -1, -1):  # parent groups must be visible too
        if level == 0:
            break
        if layers[j]['child'] < level:
            if not layers[j]['flags'] & 1:
                return False
            level = layers[j]['child']
    return True


def render(doc, frame_index):
    canvas = Image.new('RGBA', (doc['w'], doc['h']), (0, 0, 0, 0))
    cels = {c['layer']: c for c in doc['frames'][frame_index]}
    for index, layer in enumerate(doc['layers']):
        if layer['type'] != 0 or index not in cels or not _visible(doc, index):
            continue
        cel = cels[index]
        if 'link' in cel:
            cel = next((c for c in doc['frames'][cel['link']] if c['layer'] == index and 'pixels' in c), None)
            if cel is None:
                continue
        img = _cel_image(doc, cel)
        opacity = cel['opacity'] / 255.0
        if doc['flags'] & 1:
            opacity *= layer['opacity'] / 255.0
        if opacity < 1:
            img.putalpha(img.getchannel('A').point(lambda v: int(round(v * opacity))))
        layer_img = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        layer_img.paste(img, (cel['x'], cel['y']))
        canvas = Image.alpha_composite(canvas, layer_img)
    return canvas


def idle_frame(doc, phase=1):
    """First frame of the idle animation ("Idle_<phase>", then "Idle"), else frame 0."""
    names = [f'idle_{phase}', 'idle']
    for wanted in names:
        for tag in doc['tags']:
            if tag['name'].strip().lower() == wanted:
                return tag['start']
    return 0


def export(path, out_png, phase=1, frame=None):
    doc = read(path)
    image = render(doc, idle_frame(doc, phase) if frame is None else frame)
    box = image.getbbox()
    if box:
        image = image.crop(box)
    image.save(out_png, optimize=True)
    return image.size
