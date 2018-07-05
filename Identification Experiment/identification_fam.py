#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import core, clock, visual, event, sound
import csv, random
import my # import functions in my.py from psychopy tutorial
import os
import pandas as pd
# import seaborn
import matplotlib.pyplot as plt

def displayStimulus(stimulusname, recordtime=None, waittime=None, secondstim=None, sound=None, feedback=False):
    '''Basic function for presenting stimuli.
       stimulusname = The name of the stimulus created in the setup section
       recordtime (optional) = The name of the time you are recording (e.g., time image is presented is imgTime)
       waittime (optional) = Time to hold stimulus (i.e., stimulusname) on screen
       sound (optional) = Sound to play after stimulus becomes visible'''
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

## Setup Section
win = visual.Window(size=[800,600], fullscr=False, monitor="testMonitor", units='cm')
numblocks = 1 # this is the number of blocks a participant will complete
numrepeatedtrials = 5 # this is the number of times each sound file will be played per block

# read stimulus file into list of dicts, then shuffle
trials = []
stimlist = my.getStimulusInputFileDict('stimuli_fam.csv')
for i in range(0, numrepeatedtrials): # this adds repeated trials for a given block
    trials += stimlist
random.shuffle(trials)

#create lists/stimuli for stimulus elements
option1 = [visual.TextStim(win, text=trial['Option1'] + '\n\n<==' , pos=(-8.0,0)) for trial in trials]
option2 = [visual.TextStim(win, text=trial['Option2'] + '\n\n==>', pos=(8.0,0)) for trial in trials]
soundfile = [sound.Sound(value="stimuli/{}".format(trial['Filename'])) for trial in trials]

#feedback
correct = [trial['CorrectResponse'] for trial in trials]
no_response = visual.TextStim(win, "You did not respond within 6 seconds. Press the left arrow or right arrow to respond after the sound has played.")

#fixation cross
fixation = visual.ShapeStim(win, 
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
    lineWidth=5,
    closeShape=False,
    lineColor='white'
)

welcomestr = ("Welcome! For this task, choose which sound you hear. "
              "Use the left arrow key for \"{}\" and the right arrow key for \"{}\".\n\n"
              "The correct response will be highlighted in green after you submit your response.\n\n"
              "Press any key to begin.")

interblockstr = ("You will now begin Block {}.\n\n"
                 "Press any key to continue.")

# create dictionaries to collect data about percentages
soundvalues = {stimdict['Value']:[0,0] for stimdict in stimlist}
#print(soundvalues)

# open data output file
directory = "result_data" # This is where all of the output data will go
ppn = my.getString(win, "Please enter a participant number:")
datafile = my.openDataFile(ppn + "fam")
# connect it with a csv writer
writer = csv.writer(datafile, delimiter=",")
# create output file header
writer.writerow([
    "Trial Number", 
    "Sound Value",
    "Selection",
    "Filename"
    ])
    
## Experiment Section
# show welcome screen
my.getCharacter(win, welcomestr.format(trials[0]['Option1'], trials[0]['Option2'], numblocks))
startTime = clock.getTime() # clock is in seconds

blocknum = 0
trialnum = 0
key = []
randomseed = 0
while blocknum < numblocks:
    for i in range(len(trials)):
        trial = trials[i]
        times = {}
        
        # Cue: present fixation for 100 ms
        displayStimulus(fixation, 'fixationTime', 0.100)
        
        # Delay: blank screen for 100 ms
        win.flip()
        times['blankTime'] = clock.getTime()
        core.wait(0.100)
        
        # Stimulus/Response: present stimulus image and wait up to 6 seconds or for a response of y, n, or Esc key
        displayStimulus(option1[i], recordtime='stimTime', secondstim=option2[i], sound=soundfile[i])
        key = event.waitKeys(6.000, ['left', 'right', 'escape'])
        times['responseTime'] = clock.getTime()
        
        # Anti-Startle: blank screen for 50 ms
        win.flip()
        times['antistartleTime'] = clock.getTime()
        core.wait(0.050)
        
        # Feedback: feedback display for 250 ms
        displayStimulus(option1[i], recordtime='feedbackTime', secondstim=option2[i], waittime=(0.250), feedback=True)
            
        # collect data
        soundvalues[trial['Value']][1] += 1
        selection = ""
        if key:
            if key[0] == "left":
                # record selection
                selection = trial['Option1']
                # add data to soundvalues dict
                soundvalues[trial['Value']][0] += 1
            elif key[0] == "right":
                selection = trial['Option2']
            else:
                selection = "escape"
        else:
            selection = "no response"
            displayStimulus(no_response, waittime=1.000) # Included 1 sec for this part so users could see the instructions briefly
            
        # Inter-trial Interval: blank screen for 100-5000 ms
        win.flip()
        times['intertrialTime'] = clock.getTime()
        core.wait(1.000)
        
        # write result to data file
        if key==None:
            key=[]
            key.append("no key")
        
        #print("sound: {}, blocknum: {}, key pressed: {}={}".format(trial['Filename'], blocknum, key[0], selection))
        
        writer.writerow([
            trialnum,
            trial['Value'],
            selection,
            trial['Filename']
            ])
            
        trialnum += 1
        if key[0]=='escape':
            break
    blocknum += 1
    if key[0]=='escape':
        break
    # randomize subsequent blocks
    randomseed = random.random()
    random.seed(randomseed)
    random.shuffle(trials)
    random.seed(randomseed)
    random.shuffle(soundfile)
    # intermission screen
    if blocknum < numblocks:
        my.getCharacter(win, interblockstr.format(blocknum + 1))
datafile.close()

# FINAL PERCENTAGES
# open data output file
percentages = my.openDataFile(ppn + "_fam_summary")
# connect it with a csv writer
writer = csv.writer(percentages, delimiter=",")
# create output file header
writer.writerow([
    "Sound Value",
    "Number Labeled {}".format(trials[0]['Option1']),
    "Total Seen",
    "Percent Labeled {}".format(trials[0]['Option1'])
    ])
    
for keyvalue in sorted(soundvalues.keys()):
    writer.writerow([
                keyvalue,
                soundvalues[keyvalue][0],
                soundvalues[keyvalue][1],
                float(soundvalues[keyvalue][0])/float(soundvalues[keyvalue][1]) * 100 if soundvalues[keyvalue][1] > 0 else 0
                ])
percentages.close()

# show goodbye screen
my.showText(win, "Thank you for participating!")
core.wait(2.000)

## Closing Section
win.close()
print("Note: No line graph created for familiarization task.")
core.quit()