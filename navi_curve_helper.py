# coding=utf-8
import copy
import PySimpleGUI as sg
import os.path
import ast


def find_abc(x1, y1, x2, y2, x3, y3, a, b, c):
    import sympy
    d, e, f = sympy.symbols("d e f", real=True)
    eq1 = sympy.Eq(a * (x1 ** 2) + b * x1 + c + d * (x1 ** 2) + e * x1 + f, y1)
    eq2 = sympy.Eq(a * (x2 ** 2) + b * x2 + c + d * (x2 ** 2) + e * x2 + f, y2)
    eq3 = sympy.Eq(a * (x3 ** 2) + b * x3 + c + d * (x3 ** 2) + e * x3 + f, y3)
    return dict(sympy.solve([eq1, eq2, eq3])).values()


def save_values_to_file(a_stock, b_stock, c_stock,
                        ghz_low, volts_low,
                        ghz_mid, volts_mid,
                        ghz_high, volts_high,
                        new_ghz_low, new_volts_low,
                        new_ghz_mid, new_volts_mid,
                        new_ghz_high, new_volts_high):
    with open('navi_curve_helper.json', 'w') as f:
        config = {
            'a_stock': a_stock,
            'b_stock': b_stock,
            'c_stock': c_stock,
            'ghz_low': ghz_low, 'volts_low': volts_low,
            'ghz_mid': ghz_mid, 'volts_mid': volts_mid,
            'ghz_high': ghz_high, 'volts_high': volts_high,
            'new_ghz_low': new_ghz_low, 'new_volts_low': new_volts_low,
            'new_ghz_mid': new_ghz_mid, 'new_volts_mid': new_volts_mid,
            'new_ghz_high': new_ghz_high, 'new_volts_high': new_volts_high
        }
        f.write(str(config))

def read_from_file(window):
    if os.path.isfile(os.getcwd()+'/navi_curve_helper.json'):
        with open('navi_curve_helper.json') as f:
            config = ast.literal_eval(f.read())
            for key in config:
                window[key].update(config[key])


def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")



sg.theme('SystemDefault')

null_pad = ((1, 1), (1, 1))
abc_size = (90, 55)
point_size = (67, 75)

a_stock = sg.Column(layout=[[sg.Text('Curvature', pad=null_pad)],
                            [sg.InputText(key='a_stock', size=(10, 1), pad=null_pad)]],
                    pad=null_pad, size=abc_size)
b_stock = sg.Column(layout=[[sg.Text('Vertex', pad=null_pad)],
                            [sg.InputText(key='b_stock', size=(10, 1), pad=null_pad)]],
                    pad=null_pad, size=abc_size)
c_stock = sg.Column(layout=[[sg.Text('Offset', pad=null_pad)],
                            [sg.InputText(key='c_stock', size=(10, 1), pad=null_pad)]],
                    pad=null_pad, size=abc_size)

a_mod = sg.Column(layout=[[sg.Text('Curvature', pad=null_pad)],
                          [sg.InputText(key='a_mod', size=(10, 1), pad=null_pad)]], pad=null_pad, size=abc_size)
b_mod = sg.Column(layout=[[sg.Text('Vertex', pad=null_pad)],
                          [sg.InputText(key='b_mod', size=(10, 1), pad=null_pad)]], pad=null_pad, size=abc_size)
c_mod = sg.Column(layout=[[sg.Text('Offset', pad=null_pad)],
                          [sg.InputText(key='c_mod', size=(10, 1), pad=null_pad)]], pad=null_pad, size=abc_size)

note_column = sg.Column(layout=[[sg.Text('', pad=null_pad)],
                                [sg.Text('GHz', pad=null_pad)],
                                [sg.Text('Volts', pad=null_pad)]], pad=null_pad, size=point_size)

bottom_column = sg.Column(layout=[[sg.Text('Bottom', pad=null_pad)],
                                  [sg.InputText(key='ghz_low', size=(6, 1), pad=null_pad)],
                                  [sg.InputText(key='volts_low', size=(6, 1), pad=null_pad)]],
                          pad=null_pad, size=point_size)
mid_column = sg.Column(layout=[[sg.Text('Mid', pad=null_pad)],
                               [sg.InputText(key='ghz_mid', size=(6, 1), pad=null_pad)],
                               [sg.InputText(key='volts_mid', size=(6, 1), pad=null_pad)]],
                       pad=null_pad, size=point_size)
top_column = sg.Column(layout=[[sg.Text('Top', pad=null_pad)],
                               [sg.InputText(key='ghz_high', size=(6, 1), pad=null_pad)],
                               [sg.InputText(key='volts_high', size=(6, 1), pad=null_pad)]],
                       pad=null_pad, size=point_size)

note_mod_column = copy.copy(note_column)
bottom_mod_column = sg.Column(layout=[[sg.Text('Bottom', pad=null_pad)],
                                      [sg.InputText(key='new_ghz_low', size=(6, 1), pad=null_pad)],
                                      [sg.InputText(key='new_volts_low', size=(6, 1),
                                                    pad=null_pad)]], pad=null_pad, size=point_size)
mid_mod_column = sg.Column(layout=[[sg.Text('Mid', pad=null_pad)],
                                   [sg.InputText(key='new_ghz_mid', size=(6, 1), pad=null_pad)],
                                   [sg.InputText(key='new_volts_mid', size=(6, 1), pad=null_pad)]],
                           pad=null_pad, size=point_size)
top_mod_column = sg.Column(layout=[[sg.Text('Top', pad=null_pad)],
                                   [sg.InputText(key='new_ghz_high', size=(6, 1), pad=null_pad)],
                                   [sg.InputText(key='new_volts_high', size=(6, 1), pad=null_pad)]],
                           pad=null_pad, size=point_size)

layout = [[sg.Frame(layout=[[a_stock, b_stock, c_stock]],
                    title='Stock curve parameters:')],
          [sg.Frame(layout=[[note_column, bottom_column, mid_column, top_column]],
                    title='Stock voltage points:')],
          [sg.Frame(layout=[[note_mod_column, bottom_mod_column, mid_mod_column, top_mod_column]],
                    title='Modded voltage points:')],
          [sg.Frame(layout=[[a_mod, b_mod, c_mod]],
                    title='Modded curve parameters:')],
          [sg.Button('Calculate curve parameters', key='calc_abc', pad=((5, 35), (0, 0)))],
          [sg.Text('Navi Curve Helper by datspike / RTG - igor\'s LAB')]]

window = sg.Window('Navi Curve Helper', layout=layout, icon='navi_offset_curve.ico')
window.finalize()
window.TKroot.bind_all("<Key>", _onKeyRelease, "+")
read_from_file(window)
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break

    if event == 'calc_abc':
        try:
            a = float(values['a_stock'])
            b = float(values['b_stock'])
            c = float(values['c_stock'])

            # top, mid, bottom, x - GHz, y - Volts
            x1 = float(values['ghz_low'])
            y1 = float(values['volts_low'])
            x2 = float(values['ghz_mid'])
            y2 = float(values['volts_mid'])
            x3 = float(values['ghz_high'])
            y3 = float(values['volts_high'])
        except Exception:
            sg.popup('Check that you\'ve entered all the values')
            continue

        cancel = False
        l = [a,b,c,x1,y1,x2,y2,x3,y3]
        for i in l:
            if i > 3:
                sg.popup('Check that you\'ve entered all voltage/clock points in GHz and volts, e.g. 2.1 Ghz, 1.2 V')
                cancel = True
                break
        if cancel:
            continue

        try:
            d, e, f = find_abc(x1, y1, x2, y2, x3, y3, a, b, c)

            xn1 = float(values['new_ghz_low'])
            yn1 = float(values['new_volts_low'])
            xn2 = float(values['new_ghz_mid'])
            yn2 = float(values['new_volts_mid'])
            xn3 = float(values['new_ghz_high'])
            yn3 = float(values['new_volts_high'])

            save_values_to_file(a, b, c, x1, y1, x2, y2, x3, y3, xn1, yn1, xn2, yn2, xn3, yn3)

            # corrections
            yn3 = yn3 + 0.013
            yn1 = yn1 - 0.009
            a_new, b_new, c_new = find_abc(xn1, yn1, xn2, yn2, xn3, yn3, d, e, f)
        except Exception:
            sg.popup('Can\'t calculate the curve parameters, are the values you\'ve entered correct?')
            continue

        window['a_mod'].update("{:.6f}".format(a_new))
        window['b_mod'].update("{:.6f}".format(b_new))
        window['c_mod'].update("{:.6f}".format(c_new))

window.close()
