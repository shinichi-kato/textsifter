from matplotlib import font_manager


def find_font():
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    knowns = {'Noto Sans CJK JP', 'Meiryo'}
    for k in knowns:
        if k in fonts:
            return k


FONT_FAMILY = find_font()
