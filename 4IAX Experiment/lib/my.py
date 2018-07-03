#!/usr/bin/env python
# -*- coding: utf-8 -*-
# "My functions" taken from PsychoPy tutorial
# See https://www.socsci.ru.nl/wilberth/psychopy/final.html

import csv
import os
import time  
from psychopy import core, visual, event

 
## Function section
def getCharacter(window, question="Press any key to continue"):
    message = visual.TextStim(window, text=question)
    message.draw()
    window.flip()
    c = event.waitKeys()
    if c:
        return c[0]
    else:
        return ''
    
def getString(window, question="Type: text followed by return"):
    string = ""
    while True:
        message = visual.TextStim(window, text=question+"\n"+string)
        message.draw()
        window.flip()
        c = event.waitKeys()
        if c[0] == 'return':
            return string
        else:
            string = string + c[0]
            
lookup = {
          'space': ' ', 
    'exclamation': '!', 
    'doublequote': '"', 
          'pound': '#', 
         'dollar': '$', 
        'percent': '%', 
      'ampersand': '&', 
     'apostrophe': '\'', 
      'parenleft': '(', 
     'parenright': ')', 
       'asterisk': '*', 
           'plus': '+', 
          'comma': ',', 
          'minus': '-', 
         'period': '.', 
          'slash': '/', 
          'colon': ':', 
      'semicolon': ';', 
           'less': '<', 
          'equal': '=', 
        'greater': '>', 
       'question': '?', 
             'at': '@', 
    'bracketleft': '[', 
      'backslash': '\\', 
   'bracketright': ']', 
    'asciicircum': '^', 
     'underscore': '_', 
      'quoteleft': '`', 
      'braceleft': '{', 
            'bar': '|', 
     'braceright': '}', 
     'asciitilde': '~', 
   'num_multiply': '*', 
        'num_add': '+', 
  'num_separator': ',', 
   'num_subtract': '-', 
    'num_decimal': '.', 
     'num_divide': '/', 
          'num_0': '0', 
          'num_1': '1', 
          'num_2': '2', 
          'num_3': '3', 
          'num_4': '4', 
          'num_5': '5', 
          'num_6': '6', 
          'num_7': '7', 
          'num_8': '8', 
          'num_9': '9', 
      'num_equal': '=', 
}

def getString2(window, question="Type: text followed by return"):
    """Return a string typed by the user, much improved version."""
    string = ''
    capitalizeNextCharacter = False
    while True:
        message = visual.TextStim(window, text=question+"\n"+string)
        message.draw()
        window.flip()
        c = event.waitKeys()[0]
        if len(c)==1:
            # add normal characters (charcters of length 1) to the string
            if capitalizeNextCharacter:
                string += c.capitalize()
                capitalizeNextCharacter = False
            else:
                string += c
        elif c == 'backspace' and len(string)>0:
            # shorten the string
            string = string[:-1]
        elif c == 'escape':
            # return no string
            return ''
        elif c == 'lshift' or  c == 'rshift':
            # pressing shift will cause precise one character to be capitalized
            capitalizeNextCharacter = True
        elif c == 'return' or c == 'num_enter':
            # return the string typed so far
            return string
        elif c in lookup.keys():
            # add special characters to the string
            string += lookup[c]
        else:
            # ignore other special characters
            pass

            
def showText(window, inputText="Text"):
    message = visual.TextStim(window, alignHoriz="center", text=inputText)
    message.draw()
    window.flip()

def openDataFile(experiment, ppn, directory):
    """open a data file for output with a filename that nicely uses the current date and time"""
    #directory= "result_data" #This is where the output data will go
    if not os.path.isdir(directory):
        os.mkdir(directory)
    filename = os.path.join(directory, "{}_{}_results.csv".format(experiment, ppn))
    datafile = open(filename, 'w', newline='')
    return datafile
    
def getStimulusInputFile(fileName):
    """Return a list of trials. Each trial is a list of values."""
    # prepare a list of rows
    rows = []
    # open the file
    inputFile = open(fileName, 'r')
    # connect a csv file reader to the file
    reader = csv.reader(inputFile, delimiter=',')
    # discard the first row, containing the column labels
    reader.next() 
    # read every row as a list of values and append it to the list of rows
    for row in reader:
        rows.append(row)
    inputFile.close()
    return rows

def getStimulusInputFileDict(fileName):
    """Return a list of trials. Each trial is a dict."""
    # prepare a list of rows
    rows = []
    # open the file
    inputFile = open(fileName, 'r')
    # connect a csv dict file reader to the file
    reader = csv.DictReader(inputFile, delimiter=',')
    # read every row as a dict and append it to the list of rows
    for row in reader:
        rows.append(row)
    inputFile.close()
    return rows
    

def debugLog(text):
    tSinceMidnight = time.time()%86400
    tSinceWholeHour = tSinceMidnight % 3600
    minutes = tSinceWholeHour / 60
    hours = tSinceMidnight / 3600
    seconds = tSinceMidnight % 60
    #print("log {:02d}:{:02d}:{:2.3f}: {}".format(int(hours), int(minutes), seconds, text))
    print("log {:02d}:{:02d}:{:f}: {}".format(int(hours), int(minutes), seconds, text))

    
#print (getStimulusInputFileLists("template_stimuli.csv"))

def displayStimulus(stimulusname, recordtime=None, waittime=None, secondstim=None, sound=None, feedback=False):
    '''Basic function for presenting stimuli.
       stimulusname = The name of the stimulus created in the setup section
       recordtime (optional) = The name of the time you are recording (e.g., time image is presented is imgTime)
       waittime (optional) = Time to hold stimulus (i.e., stimulusname) on screen
       sound (optional) = Sound to play after stimulus becomes visible'''
    global win
    if feedback == True:
        if correct[i] in stimulusname.text:
            stimulusname.color = 'green'
        else:
            secondstim.color = 'green'
    stimulusname.draw()
    if secondstim:
        secondstim.draw()
    win.flip()
    if recordtime:
        times[recordtime] = clock.getTime()
    if sound:
        sound.play()
    if waittime:
        core.wait(waittime)
