PsychoPy Identification Experiment
Melissa Lopez

The identification.py script is a basic script for running identification experiments. It 
can be used with any appropriate stimuli by following the instructions under the heading 
"To create your identification experiment". By default it presents each sound file 4 times 
each in 5 blocks, but this can be manipulated right at the beginning of the setup section 
using the variables "numrepeatedtrials" and "numblocks", respectively.


To create your identification experiment:
1. Create a folder called "stimuli" at the same level as the script. Copy sound files here.
2. Create a Windows-formatted CSV file called "stimuli.csv" at the same level. There should be 3 columns: 
   Filename: The list of file names from the "stimuli" folder that will be used for this experiment.
             Note: These are just the file names, not full paths.
   Value: The order number of the sound file (to be used when creating graph).
   Option1: The text stimulus to appear on the left side of the screen (e.g., ba).
   Option2: The text stimulus to appear on the right side of the screen (e.g., wa).
3. Open the script in PsychoPy's coder view and click Run.
   
To create your familiarization task:
1. Follow Step 1 from above.
2. This is slightly different from Step 2 above. Create a Windows-formatted CSV file called "stimuli_fam.csv" at the same level. There should be 4 columns: 
   Filename: The list of file names from the "stimuli" folder that will be used for this experiment.
             Note: These are just the file names, not full paths.
   Value: The order number of the sound file (to be used when creating graph).
   Option1: The text stimulus to appear on the left side of the screen (e.g., ba).
   Option2: The text stimulus to appear on the right side of the screen (e.g., wa).
   CorrectResponse: The "correct" option that will be signaled when feedback is provided.
3. Open the script in PsychoPy's coder view and click Run.

   
Output files to expect in "result_data" folder (where *N* = the participant number):
1. ppn*N*(_fam)_results.csv - This is raw results file that records each response.
2. ppn*N*(_fam)_summary_results.csv - This results file combines all of the responses and provides
                                percentages of Option1 at each Value.
3. ppn*N*_plot.png - The "identification function", i.e., a line graph of the percentages.
                     x = Value, y = % labeled as Option1
                     Note: This is not created for familiarization tasks.


Still to do:
- Adjust timing as needed. My machine has been adding ~15ms to each phase. Not sure if it's
  worth adjusting this now when it changes from machine to machine.