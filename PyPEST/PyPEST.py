#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
PyPEST allows users to run perception experiments using the Parameter
Estimation by Sequential Testing (PEST) procedure. Users should first
download PsychoPy, then open and run this script through the Coder
view. See 'Using PyPEST.docx' for more information.
'''

print('Importing packages. This may take a moment...')
import sys
import os
import csv
import random
import shutil
import datetime

sys.path.insert(0, 'lib')
import my
import gui
from pest_redux import pest

from psychopy import core, clock, visual, event, prefs, monitors
prefs.general['audioLib'] = ['pyo']  # Change to pyo sound library
from psychopy import sound

__author__ = 'Melissa Lopez'
__version__ = '0.4.0'

def main():
    
    def display_stimulus(stimuli, recordtime=None, waittime=None, 
                          sound=None, feedback=False):
        '''This presents stimuli and records relevant experiment times.
           stimuli = Name of stimulus object created in the setup 
                          section
           recordtime (optional) = Label for the time being recorded
           waittime (optional) = Amount of time to hold stimulus (i.e.,
                                 stimulusname) on the screen (s)
           sound (optional) = Sound to play when stimulus becomes 
                              visible
           feedback = True if feedback is to be provided to user
        '''
        if feedback == True:
            if trial['CorrectResponse'][presentation] == '1':
                stimuli[0] = option1_waves
                #stimuli[0].color = 'green'
            else:
                stimuli[1] = option2_waves
                #stimuli[1].color = 'green'
        for stim in stimuli:
                stim.draw()
        win.flip()
        if recordtime:
            times[recordtime] = clock.getTime()
        if sound:
            sound.play()
        if waittime:
            core.wait(waittime)
    
    def display_welcome(screen_number):
        screen_text = visual.TextStim(win, text=welcome_str[screen_number], 
                                      wrapWidth=25, pos=(0,0))
        welcome_img[screen_number].append(screen_text)
        display_stimulus(welcome_img[screen_number])
        c = event.waitKeys()
        if c:
            return c[0]
        else:
            return ''
    
    def complete_results(convergence):
        endTime = clock.getTime()
        experiment_info = [{'Trial Number': '', 'Level': ''}]
        for key, value in settings.items():
            experiment_info.append({'Trial Number': key, 'Level': value})
        if convergence == 'converged':
            converge_str = 'Convergence at level {} after {} trials!'.format(comparison, trialnum)
        elif convergence == 'escaped':
            converge_str = 'User ended experiment after {} trials.'.format(trialnum)
        else:
            converge_str = 'No convergence after {} trials.'.format(trialnum)
        experiment_info.extend([{'Trial Number': 'Convergence', 'Level': converge_str},
                               {'Trial Number': 'Experiment Run Time (seconds)', 'Level': (endTime-startTime)}])
        writer.writerows(experiment_info)
        print(converge_str)
   
    '''SETTINGS
    This is where the GUI that takes the experiment settings is
    initiated. It opens the GUI window for user input, saves the 
    entered information to a dictionary, and then assigns it to 
    variables used in the experiment.
    '''
    
    print('Waiting for user to input settings...')
    settings = gui.main()
    print('Loading settings...')
    settings['Experiment Date/Time'] = str(datetime.datetime.now())
    for key, value in settings.items():
        print('{}: {}'.format(key,value))
    experiment = settings['Experiment Name']
    ppn = settings['Participant ID']
    outdir = settings['Output Directory']
    stimfile = settings['Input File']
    stimdir = settings['Stimulus Directory']
    feedback = settings['Feedback']
    
    for k in settings.keys():
        if 'Interval' in k:
            settings[k] = float(settings[k]) / 1000
    
    win = visual.Window(size=(settings['Screen Width'], settings['Screen Height']), 
                        fullscr=False, monitor='testMonitor', units='cm')

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
    
    option1 = visual.ImageStim(win, image='img/speaker-silent.jpg', pos=(-8.0,0))
    option2 = visual.ImageStim(win, image='img/speaker-silent.jpg', pos=(8.0,0))
    option1_border = visual.ImageStim(win, image='img/speaker-silent-border.jpg', pos=(-8.0,0))
    option2_border = visual.ImageStim(win, image='img/speaker-silent-border.jpg', pos=(8.0,0))
    option1_waves = visual.ImageStim(win, image='img/speaker.jpg', pos=(-8.0,0))
    option2_waves = visual.ImageStim(win, image='img/speaker.jpg', pos=(8.0,0))
    
    #option1 = visual.TextStim(win, text='Pair 1\n\n   <==', pos=(-6.0,0))
    #option2 = visual.TextStim(win, text='Pair 2\n\n==>', pos=(6.0,0))
    
    for trial in trials:
        trial['soundstim'] = (sound.Sound(os.path.join(stimdir, 'tmp', trial['Filename'][0])), 
                              sound.Sound(os.path.join(stimdir, 'tmp', trial['Filename'][1])))
        trial['basefile'] = trial['Original Base Filename'][0]
        trial['compfile'] = trial['Original Comparison Filename'][1]
    
    # PEST defaults
    if int(settings['Maximum Stimulus']) > len(trials):
        settings['Maximum Stimulus'] = len(trials)
    if int(settings['Maximum Step Size']) > len(trials):
        settings['Maximum Step Size'] = len(trials)
    if int(settings['First Comparison']) > len(trials):
        settings['First Comparison'] = len(trials)
    
    pest_dict = {'Expected Correct Response': 0,
                 'User Correct': True,
                 'Number Correct': 0,
                 'Expected Number Correct': 0,
                 'Reversals': 0,
                 'Wald': 0.5,
                 'Change Level': 0,
                 'Next Direction': -1,
                 'Step Size': int(settings['Maximum Step Size'])/2,
                 'Next Level': int(settings['First Comparison']),
                 'Number of Trials at Stimulus Level': 0,
                 'Double': False,
                 'Same Direction': 0,
                 'Doubled at Last Reversal': False}
    
    # Various pieces for presentation
    if settings['Response Box']:
        response_input = ['LEFT button', 'RIGHT button', 'red stop button in the PsychoPy Coder window']
    else:
        response_input = ['LEFT arrow key', 'RIGHT arrow key', 'Esc key']
    
    no_response = visual.TextStim(win, 'You did not respond quickly enough.' 
    '\n\nPress the ' + response_input[0] + ' or ' + response_input[1] +
    ' to choose which syllable pair had two unique syllables.')

    welcome_str = ['Welcome! In this experiment, you will hear two '
          'pairs of syllables presented consecutively. You will choose '
          'which pair sounds like two *different* syllables.\n\n\n\n\n\n\n'
          'Press any key to continue.\n', 
          'You will use the {} for {} and the {} for {}. You will see a black border '
          'around your choice (see Pair 1 below).\n\n\n\n\n\n\n'
          'Press any key to continue.\n'.format(response_input[0], 'Pair 1',
                                              response_input[1], 'Pair 2'), 
          'The speaker for the correct option will display sound waves as shown below for Pair 2.'
          '\n\n\n\n\n\n\n\nPress any key to continue.\n',
          'You may exit the experiment during any trial by pressing the {}.\n\n\n\n\n\n\n'
          'Press any key to begin the experiment.\n'.format(response_input[2])]
    welcome_img = [[option1, option2], [option1_border, option2],
                   [option1, option2_waves], [option1, option2]]
          
    goodbyestr = visual.TextStim(win, text='You made it to the end!\nGreat work!', pos=(0,5.0))
    goodbyeimg = visual.ImageStim(win, image='img/greatjob.png', pos=(0,-3.0))
    goodbyeimg.size /= 2
          
    fixation = visual.ImageStim(win, image='img/get-ready.jpg')
    
    cheertext = ['Awesome job! Keep up the good work!',
                 'You are doing great!',
                 'Keep going! You can do it!',
                 'You are a great listener!']
    cheerimg = ['img/girl-waving.png', 'img/girl-riding-a-scooter.png',
                'img/girl-jumping-rope.png', 'img/girl-holding-magnifying-glass.png']
    cheerstim = []
    for txt, img in list(zip(cheertext, cheerimg)):
        cheerstim.append([visual.TextStim(win, text=txt, pos=(0,5.0)), 
                          visual.ImageStim(win, image=img, pos=(0,-3.0))])

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
        fieldnames = ['Trial Number', 'Level', 'Base Filename', 'Comparison Filename', 
                      'Correct Response', 'User Response', 'Reaction Time', 'Filename',
                      'Expected Correct Response', 'User Correct', 'Number Correct', 
                      'Expected Number Correct', 'Reversals', 'Wald', 'Change Level',
                      'Next Direction', 'Step Size', 'Next Level', 'Number of Trials at Stimulus Level',
                      'Double', 'Same Direction', 'Doubled at Last Reversal']
        writer = csv.DictWriter(datafile, fieldnames=fieldnames)
        writer.writeheader()
        
        display_welcome(0)
        display_welcome(1)
        if feedback==True:
            display_welcome(2)
        display_welcome(3)
        
        startTime = clock.getTime() # clock is in seconds
        trialnum = 1
        key = []
        comparison = int(pest_dict['Next Level'])
        cheernum = 0
        
        mouse = event.Mouse(win=win)
        
        while  trialnum <= int(settings['Maximum Trials']):
            i = comparison - 1
            presentation = random.choice([0,1]) #Choose whether to use AAAB or ABAA
            trial = trials[i]
            times = {}
            correctresult = False
            
            # Cue: Present fixation image
            display_stimulus([fixation, option1_waves, option2_waves], 
                            'fixationTime', settings['Cue Interval'])
            
            # Delay: Wait before presenting stimulus
            display_stimulus([option1, option2], 
                            'blankTime', settings['Delay Interval'])
            
            # Stimulus/Response: Present stimulus, wait
            # for a response of left, right, or Esc key / mouse button click
            if settings['Response Box']:
                display_stimulus([option1, option2], 
                                'stimTime',
                                sound=trial['soundstim'][presentation])
                display_stimulus([option1_waves, option2], waittime=0.790)
                display_stimulus([option1, option2], waittime=0.500)
                display_stimulus([option1, option2_waves], waittime=0.790)
                wait = settings['Response Interval']
                timer = core.Clock()
                clicked = False
                mouse.clickReset()
                key = []
                while not clicked and timer.getTime() < wait:
                    display_stimulus([option1, option2])
                    button = mouse.getPressed()
                    if sum(button):
                        if button[0] == 1:
                            key.append('left')
                        elif button[2] == 1:
                            key.append('right')
                        else:
                            key.append('escape')
                        clicked = True

            else:            
                display_stimulus([option1, option2], 
                                'stimTime', sound=trial['soundstim'][presentation])
                display_stimulus([option1_waves, option2], waittime=0.790)
                display_stimulus([option1, option2], waittime=0.500)
                display_stimulus([option1, option2_waves], waittime=0.790)
                display_stimulus([option1, option2])
                key = event.waitKeys(settings['Response Interval'], 
                                    ['left', 'right', 'escape'])
            times['responseTime'] = clock.getTime()
            
            
            # Anti-Startle: Wait for 0 ms
            if key:
                if key[0] == 'left':
                    option1_response = option1_border
                    option2_response = option2
                elif key[0] == 'right':
                    option2_response = option2_border
                    option1_response = option1
                else:
                    option1_response = option1
                    option2_response = option2
            else:
                option1_response = option1
                option2_response = option2
            display_stimulus([option1_response, option2_response], 
                             'antistartleTime', 
                             settings['Anti-Startle Interval'])
            core.wait(0.250)
    
            # Feedback: Display feedback for 250 ms
            display_stimulus([option1, option2], 
                             'feedbackTime',
                             settings['Feedback Interval'],
                             feedback=feedback)
            
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
                               correctresult, 
                               pest_dict['Number Correct'], 
                               pest_dict['Expected Number Correct'], 
                               pest_dict['Double'], 
                               pest_dict['Wald'],  
                               pest_dict['Next Direction'], 
                               pest_dict['Change Level'], 
                               pest_dict['Same Direction'], 
                               int(pest_dict['Next Level']),
                               pest_dict['Reversals'], 
                               pest_dict['Number of Trials at Stimulus Level'], 
                               int(settings['Maximum Step Size']),
                               float(settings['Minimum Step Size']),
                               pest_dict['Step Size'],
                               int(settings['Maximum Stimulus']),
                               int(settings['Minimum Stimulus']),
                               pest_dict['Doubled at Last Reversal'],
                               trialnum)   
            
            resultdata = {'Trial Number': trialnum, 'Level': trial['Level'][presentation],
                          'Base Filename': trial['basefile'], 'Comparison Filename': trial['compfile'],
                          'Correct Response': trial['CorrectResponse'][presentation],
                          'User Response': selection, 
                          'Reaction Time': times['responseTime'] - times['stimTime'], 
                          'Filename': trial['Filename'][presentation]}
            resultdata.update(pest_result)
            
            # Write result to data file
            writer.writerow(resultdata)

            comparison = int(pest_result['Next Level'])
            if pest_result['Change Level'] == 2:
                complete_results('converged')
                break
            
            if selection == 'escape':
                complete_results('escaped')
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
                if (trialnum % 20) == 0:
                    if cheernum < 4:
                        display_stimulus(cheerstim[cheernum], waittime=3.000)
                        cheernum += 1
                    else:
                        display_stimulus(cheerstim[cheernum], waittime=3.000)
                        cheernum = 0
                trialnum += 1
            else:
                complete_results('no convergence')
                break

    # Show goodbye screen
    print('Results saved to {}'.format(os.path.join(outdir, 
                                   ''.join([experiment, '_', ppn, '_results.csv']))))
    my.showText(win, "You finished the experiment! Great work!")
    display_stimulus([goodbyestr, goodbyeimg])
    shutil.rmtree(os.path.join(settings['Stimulus Directory'], 'tmp'))
    core.wait(2.000)

    ## Closing Section
    win.close()
    core.quit()


if __name__ == "__main__":
    main()