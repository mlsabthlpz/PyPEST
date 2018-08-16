def pest(correct, correctness, numcorrect, expectedcorrect, double, wald,  
          pdir2, chng, same, level, reversals, numtrials, maxstep, minstep): 
    
    level2, pdir, pstep = (0, 0, 0)
        
    if correctness:
        numcorrect += 1 
    expectedcorrect += 0.69
    upperbound = expectedcorrect + wald
    lowerbound = expectedcorrect - wald
    if reversals > 1:
        wald = reversals * 0.5
    maxstep, pstep = (int(maxstep), int(pstep))
    
    pdir = -1
    if pdir2 == 0 or (numcorrect > lowerbound and numcorrect < upperbound):
        chng = 0
        numtrials += 1
        if numtrials % 8 == 0:
            reversals += 1
        pstep = maxstep / 2**reversals
        if pstep <= minstep:
            chng = 2   #L70
            double = False
            same = 0
            level2 = level + (pdir * pstep) #L80
            if level2 > 0:
                level = level2 #L90
                expectedcorrect = 0
                numcorrect = 0
                numtrials = 0
            else: 
                reversals += 1
                double = False  #L40 if applicable
                pstep = maxstep / 2**reversals #L50
                chng = 1 #L60
                if pstep < minstep: #L70 if applicable
                    chng = 2
                    double = False
                    same = 0
                level2 = level + (pdir * pstep) #L80
                if level2 > 0:
                    level = level2 #L90
                    expectedcorrect = 0
                    numcorrect = 0
                    numtrials = 0
        elif pdir2 == 0:
            pdir2 = pdir
    elif numcorrect > upperbound:    
        if pdir == pdir2:
            if pdir2 != 0: #L20
                same += 1
            pdir2 = pdir
            if same >= 3:
                double = True  #L30 if applicable
                if reversals > 0:
                    reversals -= 1
            elif same == 1 or double:
                double = False  #L40 if applicable
            pstep = maxstep / 2**reversals #L50
            chng = 1 #L60
            if pstep < minstep: #L70 if applicable
                chng = 2
                double = False
                same = 0
            level2 = level + (pdir * pstep) #L80
            if level2 > 0:
                level = level2 #L90
                expectedcorrect = 0
                numcorrect = 0
                numtrials = 0
            else: 
                reversals += 1
                double = False  #L40 if applicable
                pstep = maxstep / 2**reversals #L50
                chng = 1 #L60
                if pstep < minstep: #L70 if applicable
                    chng = 2
                    double = False
                    same = 0
                level2 = level + (pdir * pstep) #L80
                if level2 > 0:
                    level = level2 #L90
                    expectedcorrect = 0
                    numcorrect = 0
                    numtrials = 0              
        else:
            pdir2 = pdir
            reversals += 1
            same = 0
            pstep = maxstep / 2**reversals
            chng = 1 #L60
            if pstep < minstep: #L70 if applicable
                chng = 2
                double = False
                same = 0
            level2 = level + (pdir * pstep) #L80
            if level2 > 0:
                level = level2 #L90
                expectedcorrect = 0
                numcorrect = 0
                numtrials = 0
            else: 
                reversals += 1
                double = False  #L40 if applicable
                pstep = maxstep / 2**reversals #L50
                chng = 1 #L60
                if pstep < minstep: #L70 if applicable
                    chng = 2
                    double = False
                    same = 0
                level2 = level + (pdir * pstep) #L80
                if level2 > 0:
                    level = level2 #L90
                    expectedcorrect = 0
                    numcorrect = 0
                    numtrials = 0
    else:
        pdir = 1
        
    pest_dict = {'correctresponse': correct,
                 'correctness': correctness,
                 'numcorrect': numcorrect,
                 'expectedcorrect':expectedcorrect,
                 'reversals': reversals,
                 'wald': wald,
                 'change': chng,
                 'pdir2': pdir,
                 'pstep': pstep,
                 'level': level,
                 'numtrials': numtrials,
                 'double': double,
                 'same': same}
    print(pest_dict)
    return pest_dict