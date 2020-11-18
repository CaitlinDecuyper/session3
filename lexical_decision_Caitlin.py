#Lexical Decision Task - Homework Session 3 - Caitlin Decuyper

from psychopy import visual, event, sound, core
import pandas as pd
import csv
import os

path_to_repository =  "K:\\PhD\\IMPRScourses\\Python\\session3"
stimuli = pd.read_csv(os.path.join(path_to_repository, 'lexical_decision_stimuli.csv'))

window = visual.Window((800, 600), color = (1,1,1)) #creates window (size of window) with white backbroud color(R,G,B)??


instructions = visual.TextStim(window, text = 'druk z (JA) als je denkt dat wat je hoort een woord is\ndruk m (NEE) als je denkt dat het geen bestaand woord is', color = (-1,-1,-1))
fixation = visual.TextStim(window, text = '+', color = (-1,-1,-1)) # black
decision = visual.TextStim(window, text = 'JA                    NEE', color = (-1,-1,-1))

#path_to_HF_stim = "K:\\PhD\\IMPRScourses\\Python\\session3\\sounds\\LF"
path_to_sounds = "K:\\PhD\\IMPRScourses\\Python\\session3\\sounds"

results = [] # add info to empty list every trial


instructions.draw()
window.flip()
core.wait(2)

for word in stimuli['word']:

    fixation.draw()
    window.flip()
    core.wait(0.5)

    path_to_stim = os.path.join(path_to_sounds, stimuli['condition'])
    audio_stim = sound.Sound(os.path.join(path_to_stim_cond, word + '.wav'))
    audio_stim.play()
    decision.draw()
    window.flip()
    #core.wait(0.5)

    clock = core.Clock
    keys = event.waitKeys(maxWait = 5, keyList=['z','m'], timeStamped = clock, clearEvents= True)
    if keys is not None:
        key, reaction_time = keys[0] # first key press at index 0
        # key = keys[0][0]
        # reaction_time = keys[0][1]
    else: # no key was pressed
        key = None
        reaction_time = 5


# store results
results.append({
    #'image': image.image,
    'key': key,
    'reaction_time': reaction_time
    })

results = pd.DataFrame(results)
results.to_csv('results.csv') # write results to csv file

