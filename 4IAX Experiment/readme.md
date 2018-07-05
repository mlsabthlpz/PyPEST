### PsychoPy 4IAX Experiment
Melissa Lopez

The 4IAX.py script is a script for running 4IAX perception experiments. It 
can be used with any appropriate stimuli by following the instructions under the heading CREATE YOUR 4IAX EXPERIMENT.

#### PROGRAM FILE STRUCTURE
4IAX Experiment/

    config/ - Directory containing CSV files that provide parameters/defaults for GUI
    experiment/ - Directory containing experimenter files
        audio/ - Default directory for audio stimuli
        csv_input/ - Default directory for CSVs containing stimulus information
        results/ - Default directory for output CSV files
    lib/ - Directory containing supporting modules/scripts
        gui.py - Python script to generate user interface
        my.py - Python script containing useful functions for PsychoPy (from PsychoPy tutorial)
    4IAX.py - the program that you will run in PsychoPy


#### CREATE YOUR 4IAX EXPERIMENT
1. Place all audio files for your experiment in the same folder. You can use any folder you like; however, it may be easiest for organization if you use the default folder: 4IAX Experiment/experiment/stimuli.
2. Create a Windows-formatted CSV file containing the three columns listed below. Again, this can be placed anywhere; however, the default location is within 4IAX Experiment/experiment/csv_input). 
      1. Filename: The list of file names from the "stimuli" folder that will be used for this experiment.
         NOTE: These should just be the file names, not full paths.
      2. QuadValue: The value you give for each quad. You can use whatever system you want to classify your quads as long as all files in the quad have the same value.
      3. CorrectResponse: The "correct" option that will be signaled when feedback is provided.
3. Open the 4IAX.py script in PsychoPy's coder view and click Run.
4. After packages are loaded, a window will appear which asks you to provide some settings. You can hover over the labels of these parameters for more information. For the Stimulus Directory and Input File, be sure to set the path to the actual locations of the files you created in Steps 1 and 2 (the locations mentioned in this document are entered by default).

#### FAMILIARIZATION TASK
The familiarization task is more or less the same as the actual experiment. You may use the 4IAX script as usual with a few small changes:
    1. Make a unique CSV file that only lists the stimuli you require for familiarization, and be sure that the audio files exist.
    2. In the settings menu, make an Experiment Name that indicates that this is a familiarization task (e.g., include "familiarization" or "fam").
    3. Make sure that the Stimulus Directory and Input File paths point to the location of your files.

#### OUTPUT FILES   
Output file to expect in 4IAX Experiment/experiment/results folder or other folder selected in settings menu (where *N* = the participant number):
1. {EXPERIMENTNAME}_*N*_results.csv - This is a raw results file that records each response.

#### TO DO
- Add validation to the settings GUI (e.g., make sure all the time intervals are numbers, etc.)
- Finish a tab in the GUI that allows users to create stimuli and input files given a folder of WAV files that contain single sounds.
