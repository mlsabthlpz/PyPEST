#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('Importing packages. This may take a moment...')
import sys
import os
import csv
import random

from psychopy import core, clock, visual, event, prefs
prefs.general['audioLib'] = ['pyo']  # Change to pyo sound library
from psychopy import sound

sys.path.insert(0, 'lib')
import my
import gui


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
            if correct[i] == '1':
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
    
    def pest():
        
        numcorrect += 1 if selection == correct[i] else 0
        
        if reversals > 1:
            wald = reversals / 2
        
        pdir = -1
        if pdir2 == 0:
            same_level()
        elif numcorrect > (expectedcorrect + wald):
            change_direction()
        elif numcorrect > (expectedcorrect - wald):
            same_level()
        else:
            pdir = 1
            
        def change_direction(): #L10
            if pdir == pdir2:
                same_direction()
            pdir2 = pdir
            reversals += 1
            same = 0
            pstep = int(settings['Maximum Step Size']) / 2**reversals
        
        def same_direction(): #L20
            if pdir2 != 0:
                same += 1
            pdir2 = pdir
            if same == 1:
                not_doubled()
            if same >= 3:
                limit_steps()
        
        def limit_steps(): #L30
            double = True
            if reverals > 0:
                reversals -= 1
            something()
        
        def not_doubled(): #L40
            double = False
        
        def something(): #L50
            pstep = settings['Maximum Step Size'] / 2**reversals
        
        def change_level(): #L60
            chng = 1
            if pstep < settings['Minimum Step Size']:
                converge()
            else:
                set_level()
                
        def converge(): #L70
            '''Convergence'''
            chng = 2
            double = False
            same = 0
            
        def set_level(): #L80
            level2 = level + (pdir * pstep)
            if level2 > 0:
                not_sure()
            reversals += 1
            not_doubled() 
        
        def not_sure(): #L90
            level = level2
            expectedcorrect = 0
            numcorrect = 0
            trials = 0
            print('to do: fill this in')
        
        def same_level(): #L100
            chng = 0
            if trials % 8 == 0:
                reversals += 1
            pstep = int(settings['Maximum Step Size']) / 2**reversals
            if pstep <= settings['Minimum Step Size']:
                converge()
   
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
    read into a list of dictionaries, and trials are repeated according
    to the entered settings and randomized. Then, visual and sound
    stimuli are created. Information about correctness is saved to a
    list, a fixation cross is created to indicate the start of each 
    trial, and strings of text are created to be read by the user at 
    the start of the experiment.
    '''
    trials = my.getStimulusInputFileDict(stimfile)
    random.shuffle(trials)
    
    option1 = visual.TextStim(win, text='Pair 1\n\n<==', pos=(-8.0,0))
    option2 = visual.TextStim(win, text='Pair 2\n\n==>', pos=(8.0,0))
    soundfile = [sound.Sound(os.path.join(stimdir, 
                                          trial['Filename'])) 
                                          for trial in trials]

    correct = [trial['CorrectResponse'] for trial in trials]
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
    datafile = my.openDataFile(experiment, ppn, outdir)
    writer = csv.writer(datafile, delimiter=',')
    writer.writerow([
        'Trial Number', 
        'Quad Value',
        'Correct Response',
        'User Response',
        'Reaction Time',
        'Filename'
        ])
    
    print('Initiating experiment...')
    '''EXPERIMENT
    This is where the actual experiment begins. First, instructions are 
    provided to the user. Then the program loops through the list of 
    trials, following timed sections as detailed in the comments below.
    '''
    my.getCharacter(win, 
                    welcomestr.format('Pair 1', 'Pair 2'))
    startTime = clock.getTime() # clock is in seconds

    trialnum = 1
    key = []
    numcorrect = 0
    expectedcorrect = 0.69
    wald = 0.5
    pdir2 = 0
    chng = 0
    same = 0
    level = settings['First Comparison']
    reversals = 0
    randomseed = 0
    for i in range(len(trials)):
        trial = trials[i]
        times = {}
        
        # Cue: Present fixation for 100 ms
        display_stimulus([fixation, option1, option2], 
                        'fixationTime', settings['Cue Interval'])
        
        # Delay: Wait for 100 ms
        display_stimulus([option1, option2], 
                        'blankTime', settings['Delay Interval'])
        
        # Stimulus/Response: Present stimulus, wait up to 6000 ms
        # for a response of left, right, or Esc key
        display_stimulus([option1, option2], 
                        'stimTime', sound=soundfile[i])
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
            # Tell user that a response is needed
            selection = 'no response'
            display_stimulus([no_response], waittime=5.000)
        
        ## PEST STUFF
        pest()   
        if chng == 2:
            print('Convergence!')
        else:
            comparison = int(settings['First Comparison'])
            if level > int(settings['Maximum Stimulus']):
                comparison = settings['Maximum Stimulus']
            if level < 1:
                comparison = 1
        
        # Write result to data file
        if key is None:
            key=[]
            key.append("no key")
        writer.writerow([
            trialnum,
            trial['QuadValue'],
            trial['CorrectResponse'],
            selection,
            times['responseTime'] - times['stimTime'],
            trial['Filename']
            ])
        
        if key[0]=='escape':
            break
        
        # Inter-trial Interval: Wait for 1000 ms
        option1.color = 'white'
        option2.color = 'white'
        display_stimulus([option1, option2], 
                         'intertrialTime',
                         settings['Inter-trial Interval'])

        # Move on to the next trial
        trialnum += 1
            
    datafile.close()

    # Show goodbye screen
    print('Results saved to {}'.format(os.path.join(outdir, 
                                   ''.join([experiment, '_', ppn, '_results.csv']))))
    my.showText(win, "Thank you for participating!")
    core.wait(2.000)

    ## Closing Section
    win.close()
    core.quit()


if __name__ == "__main__":
    main()