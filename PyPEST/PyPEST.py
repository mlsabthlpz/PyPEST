#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('Importing packages. This may take a moment...')
import sys
import os
import csv
import random
import shutil

from psychopy import core, clock, visual, event, prefs
prefs.general['audioLib'] = ['pyo']  # Change to pyo sound library
from psychopy import sound

sys.path.insert(0, 'lib')
import my
import gui
from pest import pest

def main():
    
    def display_stimulus(stimuli, recordtime=None, waittime=None, 
                          sound=None, feedback=False):
        '''This presents stimuli and records relevant experiment times.
           stimulusname = Name of stimulus object created in the setup 
                          section
           recordtime (optional) = Label for the time being recorded
           waittime (optional) = Amount of time to hold stimulus (i.e.,
                                 stimulusname) on the screen (ms)
           sound (optional) = Sound to play when stimulus becomes 
                              visible
           feedback = True if feedback is to be provided to user
        '''
        if feedback == True:
            if trial['CorrectResponse'][presentation] == '1':
                stimuli[0].color = 'green'
            else:
                stimuli[1].color = 'green'
        for stim in stimuli:
                stim.draw()
        win.flip()
        if recordtime:
            times[recordtime] = clock.getTime()
        if sound:
            sound.play()
        if waittime:
            core.wait(waittime)
   
    '''SETTINGS
    This is where the GUI that takes the experiment settings is
    initiated. It opens the GUI window for user input, saves the 
    entered information to a dictionary, and then assigns it to 
    variables used in the experiment.
    '''
    
    print('Waiting for user to input settings...')
    settings = gui.main()
    print('Loading settings...')
    for key, value in settings.items():
        print('{}: {}'.format(key,value))
    experiment = settings['Experiment Name']
    ppn = settings['Participant ID']
    outdir = settings['Output Directory']
    stimfile = settings['Input File']
    stimdir = settings['Stimulus Directory']
    
    
    for k in settings.keys():
        if 'Interval' in k:
            settings[k] = float(settings[k]) / 1000
   
    win = visual.Window(size=[800,600], fullscr=False, 
                        monitor="testMonitor", units='cm')

    print('Building experiment...')
    '''STIMULUS CREATION
    This is where the stimuli are created. First, the input file is 
    read into a list of dictionaries. Then, visual and sound
    stimuli are created. Information about correctness is saved to a
    list, a fixation cross is created to indicate the start of each 
    trial, and strings of text are created to be read by the user at 
    the start of the experiment.
    '''
    rows = []
    with open(stimfile, 'r') as input:
        reader = csv.DictReader(input, delimiter=',')
        for row in reader:
            rows.append(row)
    trialsA = [rows[i] for i in range(0, len(rows), 2)]
    trialsB = [rows[i] for i in range(1, len(rows), 2)]
    trials = [{key: (value1, value2) 
                    for key, value1, value2 
                    in zip(trialsA[i].keys(), trialsA[i].values(), trialsB[i].values())} 
                for i in range(len(trialsA))]       
    
    option1 = visual.TextStim(win, text='Pair 1\n\n<==', pos=(-8.0,0))
    option2 = visual.TextStim(win, text='Pair 2\n\n==>', pos=(8.0,0))
    
    for trial in trials:
        trial['soundstim'] = (sound.Sound(os.path.join(stimdir, 'tmp', trial['Filename'][0])), 
                              sound.Sound(os.path.join(stimdir, 'tmp', trial['Filename'][1])))

    numcorrect, expectedcorrect, reversals, same, numtrials, chng, pdir2 = (0,0,0,0,0,0,0)
    wald = 0.5
    level = settings['First Comparison']
    double = False
    randomseed = 0
    pest_dict = {'correctresponse': 0,
                 'correctness': True,
                 'numcorrect': 0,
                 'expectedcorrect': 0,
                 'reversals': 0,
                 'wald': 0.5,
                 'change': 0,
                 'pdir2': 0,
                 'pstep': 0,
                 'level': int(settings['First Comparison']),
                 'numtrials': 0,
                 'double': False,
                 'same': 0}
    if int(settings['First Comparison']) > len(trials):
        pest_dict['level'] = len(trials)
    if int(settings['Maximum Stimulus']) > len(trials):
        settings['Maximum Stimulus'] = len(trials)
    
    no_response = visual.TextStim(win, 'You did not respond within 6 ' 
    'seconds. \n\nPress the left arrow or right arrow to choose which '
    'syllable pair had two unique syllables.')

    fixation = visual.ShapeStim(win, 
        vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
        lineWidth=5,
        closeShape=False,
        lineColor='white'
    )

    welcomestr = ('In this experiment, you will hear two '
                  'pairs of syllables presented consecutively. Choose '
                  'which pair sounds like two different syllables '
                  '(i.e., not the same syllable repeated). Use the '
                  'left arrow key for {} and the right arrow key for '
                  '{}.\n\nThe correct response will appear in green ' 
                  'after you have responded.\n\nPress any key to '
                  'begin.')

    '''OUTPUT FILE
    This is where the output file is initially created using the
    experiment name and participation number. A header row is created 
    to start the file.
    '''
    datafile = os.path.join(outdir, "{}_{}_results.csv".format(experiment, ppn))
    
    print('Initiating experiment...')
    
    '''EXPERIMENT
    This is where the actual experiment begins. First, instructions are 
    provided to the user. Then the program loops through the list of 
    trials, following timed sections as detailed in the comments below.
    '''
    with open(datafile, 'w', newline='') as datafile:
        fieldnames = ['Trial Number', 'Level', 'Correct Response',
                      'User Response', 'Reaction Time', 'Filename',
                      'correctresponse', 'correctness', 'numcorrect', 'expectedcorrect', 
                      'reversals', 'wald', 'change', 'pdir2', 'pstep', 'level', 'numtrials', 
                      'double', 'same']
        writer = csv.DictWriter(datafile, fieldnames=fieldnames)
        writer.writeheader()
        
        my.getCharacter(win, 
                        welcomestr.format('Pair 1', 'Pair 2'))
        startTime = clock.getTime() # clock is in seconds
    
        trialnum = 1
        key = []
        
        while  trialnum < int(settings['Maximum Trials']):
            i = int(pest_dict['level'])-1
            presentation = random.choice([0,1]) #Choose whether to use AAAB or ABAA
            trial = trials[i]
            times = {}
            correctresult = False
            
            # Cue: Present fixation for 100 ms
            display_stimulus([fixation, option1, option2], 
                            'fixationTime', settings['Cue Interval'])
            
            # Delay: Wait for 100 ms
            display_stimulus([option1, option2], 
                            'blankTime', settings['Delay Interval'])
            
            # Stimulus/Response: Present stimulus, wait up to 6000 ms
            # for a response of left, right, or Esc key
            display_stimulus([option1, option2], 
                            'stimTime', sound=trial['soundstim'][presentation])
            key = event.waitKeys(settings['Response Interval'], 
                                ['left', 'right', 'escape'])
            times['responseTime'] = clock.getTime()
            
            # Anti-Startle: Wait for 500 ms
            display_stimulus([option1, option2], 
                             'antistartleTime', 
                             settings['Anti-Startle Interval'])
    
            # Feedback: Display feedback for 250 ms
            display_stimulus([option1, option2], 
                             'feedbackTime',
                             settings['Feedback Interval'],
                             feedback=True)
            
            # Collect data
            selection = ''
            if key:
                # Record selection
                if key[0] == 'left':
                    selection = '1'
                elif key[0] == 'right':
                    selection = '2'
                else:
                    selection = 'escape'
            else:
                selection = 'no response'
                display_stimulus([no_response], waittime=5.000)
                
            if trial['CorrectResponse'][presentation] == selection:
                correctresult = True
            
            ## PEST STUFF
            pest_result = pest(trial['CorrectResponse'][presentation],
                               correctresult, pest_dict['numcorrect'], 
                               pest_dict['expectedcorrect'], 
                               pest_dict['double'], 
                               pest_dict['wald'],  
                               pest_dict['pdir2'], 
                               pest_dict['change'], 
                               pest_dict['same'], 
                               int(pest_dict['level']),
                               pest_dict['reversals'], 
                               pest_dict['numtrials'], 
                               int(settings['Maximum Step Size']),
                               float(settings['Minimum Step Size']))   
            if pest_result['change'] == 2:
                print('Convergence!')
            else:
                comparison = int(pest_result['level'])
                if float(pest_result['level']) > int(settings['Maximum Stimulus']):
                    comparison = settings['Maximum Stimulus']
                if float(pest_result['level']) < 1:
                    comparison = 1
            print(comparison)
            
            resultdata = {'Trial Number': trialnum, 'Level': trial['Level'][presentation],
                          'Correct Response': trial['CorrectResponse'][presentation],
                          'User Response': selection, 
                          'Reaction Time': times['responseTime'] - times['stimTime'], 
                          'Filename': trial['Filename'][presentation]}
            resultdata.update(pest_result)
            
            # Write result to data file
            writer.writerow(resultdata)
            
            if selection == 'escape':
                break
            
            # Inter-trial Interval: Wait for 1000 ms
            option1.color = 'white'
            option2.color = 'white'
            display_stimulus([option1, option2], 
                             'intertrialTime',
                             settings['Inter-trial Interval'])
    
            # Move on to the next trial
            pest_dict = pest_result
            if trialnum < int(settings['Maximum Trials']):
                trialnum += 1
            else:
                break
            
    #datafile.close()

    # Show goodbye screen
    print('Results saved to {}'.format(os.path.join(outdir, 
                                   ''.join([experiment, '_', ppn, '_results.csv']))))
    my.showText(win, "You have reached the end of the experiment. Thank you for participating!")
    shutil.rmtree(os.path.join(settings['Stimulus Directory'], 'tmp'))
    core.wait(2.000)

    ## Closing Section
    win.close()
    core.quit()


if __name__ == "__main__":
    main()