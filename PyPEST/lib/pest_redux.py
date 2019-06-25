def pest(correct, response_is_correct, numcorrect, expectedcorrect, double, wald,  
          previous_direction, change_level, same_direction, previous_level, 
          reversals, numtrials_at_stim_level, maxstep, minstep, previous_step,
          maxstim, minstim, double_at_last_reversal, trialnum): 
    
    ## Determine direction of next move, change stimulus level if the number correct 
    ## falls outside of wald range from expected correct value (i.e., +/- 0.5)
    
    # Determine number correct and expected correct range
    if response_is_correct:
        numcorrect += 1
    expectedcorrect += 0.69
    lowerbound = expectedcorrect - wald
    upperbound = expectedcorrect + wald
    
    # Decide if levels should be changed
    if numcorrect > upperbound:
        next_direction = -1
        change_level = 1
    elif numcorrect < lowerbound:
        next_direction = 1
        change_level = 1
    else: # same level because it's within the range
        next_direction = previous_direction
        change_level = 0
    
    ## Determine step size for the next trial
    
    # Default step size to next trial is the same as previous trial
    next_step = previous_step
    
    # Track direction for doubling/reversals to determine step size
    if change_level == 1:
        
        # Change levels in the same direction as before
        if next_direction == previous_direction:
            # Do not change levels if it would go beyond available trials
            if previous_level == minstim or (previous_level == maxstim and next_direction == 1):
                change_level == 0
                numtrials_at_stim_level += 1
             
            # Count number of steps in the same direction, double 
            # step size if appropriate, & reset count totals for new level
            else:
                same_direction += 1
                double = False
                if same_direction >= 3: # the old PEST used >=3, but >3 would actually mean the 4th step.
                    if double_at_last_reversal == True: 
                        double = False
                    else:
                        double = True
                        next_step = next_step * 2
                numtrials_at_stim_level = 0
                expectedcorrect = 0
                numcorrect = 0
        
        # Reverse direction and halve step size
        elif next_direction != previous_direction:
            if double == True:
                double_at_last_reversal = True
            else:
                double_at_last_reversal = False
            double = False
            reversals += 1
            same_direction = 0
            next_step = next_step / 2
            numtrials_at_stim_level = 0
            expectedcorrect = 0
            numcorrect = 0
    
    # If not changing levels, keep track of number of trials at the
    # current stimulus level
    else:
        numtrials_at_stim_level += 1
    
    # After several trials at a given level with no movement, reverse direction    
    if numtrials_at_stim_level > 0 and numtrials_at_stim_level % 8 == 0:
        reversals += 1
        same_direction = 0
        if next_direction == 1:
            next_direction = -1
        else:
            next_direction = 1
        next_step = next_step / 2
    
    ## Determine level and adjust so that steps and levels are within 
    ## user-specified parameters (i.e., Max/Min Stimulus, Max/Min Step Size)
    
    true_step = next_step # Keep track of decimals when halving
    next_step = int(next_step) # Use whole number for actual step size
    
    # Don't go outside parameters for step size
    if next_step > maxstep:
        next_step = maxstep
        true_step = maxstep
    elif next_step < minstep or next_step < 1: 
        change_level = 2
    
    # If changing levels, determine the next level given step size and direction
    if change_level > 0:
        next_level = previous_level + (next_direction * next_step)
    else:
        next_level = previous_level
        
    # Don't go outside parameters for level
    if next_level > maxstim:
        next_level = maxstim
    elif next_level <= minstim:
        next_level = minstim
        
    # Dictionary will be returned to move on to the next trial.
    pest_dict = {'Expected Correct Response': correct, #correctresponse
                 'User Correct': response_is_correct, #correctness
                 'Number Correct': numcorrect, #numcorrect
                 'Expected Number Correct':expectedcorrect, #expected correct
                 'Reversals': reversals, #reversals
                 'Wald': wald, #wald
                 'Change Level': change_level, #change
                 'Next Direction': next_direction, #pdir2
                 'Step Size': true_step, #pstep
                 'Next Level': next_level, #level
                 'Number of Trials at Stimulus Level': numtrials_at_stim_level, #numtrials
                 'Double': double, #double
                 'Same Direction': same_direction, #same
                 'Doubled at Last Reversal': double_at_last_reversal} #double_last_reversal
    print(pest_dict)
    return pest_dict