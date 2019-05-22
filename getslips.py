#Alan Long 6/14/16
#Last edited: Alan Long 7/31/18

#7/31/18 CONFIRMED WORKING

#This code finds slips which have a rate of change above a certain threshold
#and determines their starting and ending times. It accepts four inputs, data
#is an array of the data to be analyzed, time an array corresponding time to the data,
#threshhold is a float that determines the slope needed to be considered a slip, and min_slip
# is a float that determines the minimum drop necessary to be considered an avalanche.
#It returns two arrays, slip_begins is the starts of the slips and slip_ends are the ends.

#This code is based on the code of Jordan and Jim, but mostly Jim.

import numpy as np
##from statsmodels.nonparametric.smoothers_lowess import lowess


def get_slips(data, time, threshhold, mindrop):

    #First we smooth the data. We use the Lowess method
    #The factor of -1 is so that we deal with positive numbers
    #for drop rates, it's not strictly neccessary but makes things nicer.
##    smoothed = np.array(-1*lowess(data, time, is_sorted=True, frac=0.025, it=0))
##    smoothed=np.transpose(smoothed[:,1])
    smoothed=np.append(-1*np.array(data),-1*data[len(data)-1])
    time=np.append(np.array(time),time[len(time)-1])
    #We now take a numeric derivative and get an average 
    deriv=np.diff(smoothed)/np.diff(time)
    diff_avg=(smoothed[len(smoothed)-1]-smoothed[0])/(time[len(time)-1]-time[0])

    #diff reduces the list length by 1 so we need a new time list, we average
    #between times to do so.
##    time2=(np.array(time)[0:len(time)-2]+np.array(time)[1:len(time)-1])/2
    
    #We now set the minimum slip rate for it to be considered an avalanche
    if threshhold==-1:
        min_diff = 0.;
    else:
        min_diff = diff_avg + np.std(deriv)*threshhold;
    
    #Now we see if a slip is occurring, i.e. if the derivative is above the
    #minimum value. We then take the diff of the bools to get the starts and ends. +1= begin, -1=end.
    slips=np.diff([int(i>=min_diff) for i in deriv])
    index_begins=[i+1  for i in range(len(slips)) if slips[i]==1]
    index_ends=[i+1 for i in range(len(slips)) if slips[i]==-1]
    #We must consider the case where we start or end on an avalanche, this
    #checks if this is case and if so makes the start or end of the data
    #a start or end of an avalanche
    if max(index_begins)>max(index_ends):
        index_ends.append(len(time))
    if min(index_begins)>min(index_ends):
        index_begins.insert(0,0)
    #Now we see if the drops were large enough to be considered an avalanche
    index_av_begins=[index_begins[i] for i in range(len(index_begins)) if mindrop<smoothed[index_ends[i]]-smoothed[index_begins[i]]]
    index_av_ends=[index_ends[i] for i in range(len(index_begins)) if mindrop<smoothed[index_ends[i]]-smoothed[index_begins[i]]]

    #Finally we use these indices to get the start and end times and sizes of the events
    time_begins=time[index_av_begins]
    time_ends=time[index_av_ends]
    slip_durations= time_ends-time_begins
    slip_sizes=-smoothed[index_av_begins]+smoothed[index_av_ends]-diff_avg*slip_durations*int(threshhold!=-1)
    
    
    
    return [time_begins, time_ends,slip_sizes,slip_durations]









    
    
