#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk
from winsound import *
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=RuntimeWarning)
    from pydub import AudioSegment
import audiostim

__author__ = 'Melissa Lopez'
__version__ = '0.4.0'

def main():
    
    dirpath = os.path.abspath('.')
    settings = {}
    title = 'PEST v{} - Settings Menu'.format(__version__)
    calibration_tone = "config\PESTtone.wav"
    
    class SettingsMenu:
        def __init__(self, master):
            
            def set_defaults():
                '''Create all widgets with default values.'''
                self.build_widgets(sessioninputs, sessionframe)
                self.build_widgets(timinginputs, timingframe)
                self.build_widgets(pestinputs, pestframe)
            
            def iter_padding(frame, maxrange, padding):
                '''Pad rows from 0 to maxrange for given frame.'''
                for i in range(maxrange):
                    frame.rowconfigure(i, pad=padding)
                    
            def play():
                return PlaySound(calibration_tone, SND_FILENAME | SND_ASYNC)
                
            def stop_play():
                return PlaySound(None, SND_PURGE)
            
            self.master = master
            master.title(title)
            master.columnconfigure(0, pad=20)
            iter_padding(master, 3, 10)
            
            self.labels = {}
            self.entries = {}
            self.checked = {}
            self.buttons = {}
            self.defaults = {}
            
            instructions = ttk.Label(master, 
                text='Set values for your experiment. '
                'Hover over labels for more information.').grid(
                    row=0, column=0)
            
            self.notebook = ttk.Notebook(master)
            self.notebook.grid(row=1, column=0)
            
            timingframe = ttk.Frame(self.notebook)
            timingframe.grid(row=0, column=0)
            iter_padding(timingframe, 8, 5)
            timingframe.columnconfigure(0, pad=35)
            
            sessionframe = ttk.Frame(self.notebook)
            sessionframe.grid(row=0, column=0)
            iter_padding(sessionframe, 7, 5)
            
            pestframe = ttk.Frame(self.notebook)
            pestframe.grid(row=0, column=0)
            iter_padding(pestframe, 6, 5)
            pestframe.columnconfigure(0, pad=35)
            
            audioframe = ttk.Frame(self.notebook)
            audioframe.grid(row=0, column=0)
            iter_padding(audioframe, 5, 5)
            audioframe.columnconfigure(0, weight=1)
                        
            buttonframe = ttk.Frame(master)
            buttonframe.grid(row=2, column=0, sticky='se')
            buttonframe.rowconfigure(0, pad=10)
            
            self.notebook.add(sessionframe, text="Session Information")
            self.notebook.add(timingframe, text="Timing Values")
            self.notebook.add(pestframe, text="PEST Presentation")
            self.notebook.add(audioframe, text="Calibrate Audio")
            
            # CSV files 
            timinginputs = self.config_info(os.path.join(dirpath, 
                                        'config','timinginputs.csv'))
            sessioninputs = self.config_info(os.path.join(dirpath, 
                                        'config','sessioninputs.csv'))
            audioinputs = self.config_info(os.path.join(dirpath, 
                                        'config','audioinputs.csv'))
            pestinputs = self.config_info(os.path.join(dirpath, 
                                        'config','pestinputs.csv'))
            
            set_defaults()
            
            # Audio calibration buttons
            calibrate_instructions = ttk.Label(audioframe, 
                                       text='Click the button to play the 15-second calibration tone.\n'
                                       'Adjust the voltage to 17.8 mV to calibrate audio volume.').grid(
                                        row=0, column=0)
            self.calibrate = ttk.Button(audioframe, text='Play calibration sound',
                              command=play).grid(row=2, column=0, sticky='ns')
            self.stop_calibrate = ttk.Button(audioframe, text='Stop',
                              command=stop_play).grid(row=3, column=0, sticky='ns')
                           
            # Buttons for the bottom of the screen               
            self.reset = ttk.Button(buttonframe, text='Reset defaults',
                           command=set_defaults).grid(row=0, column=0)
            self.submit = ttk.Button(buttonframe, text='Submit & Continue', 
                   command=self.return_settings).grid(row=0, column=1,
                                                       padx=5)
            self.quit = ttk.Button(buttonframe, text='Exit', 
                              command=sys.exit).grid(row=0, column=2)
            
            
        def build_widgets(self, inputs, frame):
            '''This is where all of the widgets are created.'''
            for d in inputs:
                self.defaults[d['label']] = tk.StringVar()
                self.defaults[d['label']].set(d['text'])
                
                if d['type'] == 'entry':
                    self.labels[d['label']] = ttk.Label(frame, 
                                                       text=d['label'])
                    self.labels[d['label']].grid(row=d['row'], 
                                                 column=d['col'], 
                                                 sticky='E')
                    Tooltip(self.labels[d['label']], 
                            text=d['tooltip'], wraplength=400)
                    
                    self.entries[d['label']] = ttk.Entry(frame, 
                                textvariable=self.defaults[d['label']], 
                                width=60)
                    self.entries[d['label']].grid(row=d['row'], 
                                                  column=int(d['col'])+1)
                    
                    if d['dialog']:
                        if d['dialog'] == 'load':
                            com = self.load_file
                        elif d['dialog'] == 'load_dir':
                            com = self.load_dir
                        else:
                            com = self.save_dir
                        self.buttons[d['label']] = ttk.Button(frame, 
                                                       text='Browse...', 
                                                       command=com)
                        self.buttons[d['label']].grid(row=d['row'], 
                                                      column=int(d['col'])+2, 
                                                      sticky='w')
                elif d['type'] == 'checkbox':
                    self.checked[d['label']] = tk.IntVar()
                    self.checked[d['label']].set(1)
                    self.entries[d['label']] = ttk.Checkbutton(frame,
                                text=d['text'], variable=self.checked[d['label']])
                    self.entries[d['label']].grid(
                        row=d['row'], column=d['col'], sticky='w')
                    Tooltip(self.entries[d['label']], 
                            text=d['tooltip'], wraplength=400)
                elif d['type'] == 'textbox':
                    self.entries[d['label']] = tk.Text(frame,
                                                        height=10,
                                                        width=66)
                    self.entries[d['label']].grid(
                        row=d['row'], column=d['col'], columnspan=3, sticky='nswe')
                    self.entries[d['label']].insert('end', d['text'])
                elif d['type'] == 'message':
                    self.entries[d['label']] = tk.Message(frame, aspect=1000,
                                   text=d['text'])
                    self.entries[d['label']].grid(
                        row=d['row'], column=d['col'], columnspan=3, sticky='w')
                elif d['type'] == 'button':
                    self.buttons[d['label']] = ttk.Button(frame, 
                                                       text=d['text'], 
                                                       command=print('Under construction'))
                    self.buttons[d['label']].grid(row=d['row'], column=d['col'])
                    Tooltip(self.buttons[d['label']], 
                            text=d['tooltip'], wraplength=400)
               
        def load_file(self):
            '''Opens open file dialog and uses input to fill
               in Stimulus Directory entry widget
            '''
            infile = filedialog.askopenfilename(initialdir=dirpath,
                                                title='Open file...')
            if infile:
                self.entries['Input File'].delete(0, "end")
                self.entries['Input File'].insert(0, infile)
        
        def load_dir(self):
            '''Opens load from directory dialog and uses input to fill
               in Stimulus Directory entry widget
            '''
            dir = filedialog.askdirectory(initialdir=dirpath,
                                          title='Load stimuli from' 
                                          'directory...')
            if dir:
                self.entries['Stimulus Directory'].delete(0, "end")
                self.entries['Stimulus Directory'].insert(0, dir)
            
        def save_dir(self):
            '''Opens save to directory dialog and uses input to fill
               in Output Directory entry widget
            '''
            outdir = filedialog.askdirectory(initialdir=dirpath,
                                             title='Save to folder...')
            if outdir:
                self.entries['Output Directory'].delete(0, "end")
                self.entries['Output Directory'].insert(0, outfile)
                
        def return_settings(self):
            '''Defines function of 'Submit & Continue' button.'''
            for param in self.entries.keys():
                try:
                    settings[param] = self.entries[param].get()
                    settings['Input File'] = os.path.join(dirpath,
                                                           'experiment',
                                                           'csv_input',
                                                           '{}_stimuli.csv'.format(settings['Experiment Name'])
                                                           )
                    settings['Screen Width'] = root.winfo_screenwidth()
                    settings['Screen Height'] = root.winfo_screenheight()
                    settings['Calibration File Path'] = os.path.join(dirpath, calibration_tone)
                except AttributeError:
                    settings[param] = self.checked[param].get()
            audiostim.create_audio(settings['Experiment Name'], 
                                   settings['Stimulus Directory'],
                                   settings['Input File'],
                                   int(settings['Minimum Stimulus']))
            self.master.destroy()
        
        def config_info(self, filename):
            '''Imports CSV files that define widgets and creates
               list of dicts.
            '''
            info = []
            config_file = open(filename, 'r')
            reader = csv.DictReader(config_file, delimiter=',')
            for row in reader:
                if row['dialog'] != '':
                    if (row['label'] == 'Stimulus Directory') or \
                       (row['label'] == 'Audio Directory'):
                        row['text'] = os.path.join(dirpath, 
                                                    'experiment',
                                                    'audio')
                    elif row['label'] == 'Input File':
                        row['text'] = os.path.join(dirpath, 
                                                    'experiment',
                                                    'csv_input',
                                                    'stimuli.csv')
                    elif row['label'] == 'Output Directory':
                        row['text'] = os.path.join(dirpath, 
                                                    'experiment',
                                                    'results')
                info.append(row)
            config_file.close()
            return info

    root = tk.Tk()
    settingsgui = SettingsMenu(root)
    root.mainloop()
    return settings

class Tooltip:
    '''
    It creates a tooltip for a given widget as the mouse goes on it.

    see:

    https://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-
           in-tkinter/36221216#36221216

    http://www.daniweb.com/programming/software-development/
           code/484591/a-tooltip-class-for-tkinter

    - Originally written by vegaseat on 2014.09.09.

    - Modified to include a delay time by Victor Zaccardo on 2016.03.25.

    - Modified
        - to correct extreme right and extreme bottom behavior,
        - to stay inside the screen whenever the tooltip might go out on 
          the top but still the screen is higher than the tooltip,
        - to use the more flexible mouse positioning,
        - to add customizable background color, padding, waittime and
          wraplength on creation
      by Alberto Vassena on 2016.11.05.

      Tested on Ubuntu 16.04/16.10, running Python 3.5.2

    TODO: themes styles support
    '''

    def __init__(self, widget,
                 *,
                 bg='#FFFFEA',
                 pad=(5, 3, 5, 3),
                 text='widget info',
                 waittime=400,
                 wraplength=250):

        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)
        self.bg = bg
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        def tip_pos_calculator(widget, label,
                               *,
                               tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        bg = self.bg
        pad = self.pad
        widget = self.widget

        # creates a toplevel window
        self.tw = tk.Toplevel(widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw,
                       background=bg,
                       borderwidth=0)
        label = ttk.Label(win,
                          text=self.text,
                          justify=tk.LEFT,
                          background=bg,
                          relief=tk.SOLID,
                          borderwidth=0,
                          wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None


if __name__ == "__main__":
    main()