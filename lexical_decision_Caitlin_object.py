#Lexical Decision Task - Homework Session 4 - Caitlin Decuyper
#Object Oriented Programming version of experiment session 3


from psychopy import visual, event, sound, core
import pandas as pd
import csv
import os
import numpy as np

path_to_repository =  "K:\\PhD\\IMPRScourses\\Python\\session4"
path_to_sounds = "K:\\PhD\\IMPRScourses\\Python\\session4\\sounds"
stimuli = pd.read_csv(os.path.join(path_to_repository, 'lexical_decision_stimuli.csv'))
#stimuli = pd.read_csv(os.path.join(path_to_repository, 'lexical_decision_stimuli_test.csv')) #file with only 5 trials

# Change the non-word condition name of the loaded CSV file
stimuli['freq_category'] = stimuli['freq_category'].replace(['none'], 'NW')



class Experiment:
    def __init__(self, window_size, text_color, background_color):
        self.text_color = text_color
        self.window = visual.Window(window_size, color=background_color)
        self.fixation = visual.TextStim(self.window, text='+', color=text_color)
        self.clock = core.Clock()
        #self.decision = visual.TextStim(self.window, text='JA                    NEE', color = text_color)

    # Show the given message on the experiment window and wait until a key is pressed.
    def show_message(self, message):
        stimulus = visual.TextStim(self.window, text=message, color=self.text_color)
        stimulus.draw()
        self.window.flip()
        event.waitKeys()

    # Show a fixation cross on the experiment window for the given amount of time.
    def show_fixation(self, time=0.5):
        self.fixation.draw()
        self.window.flip()
        core.wait(time)

    #def show_decision(self, time=2):
        #self.decision.draw()
        #self.window.flip()
        #core.wait(time)


# This class defines a single trial of an experiment.
class AudioTrial:
    def __init__(self, experiment, name, audio, fixation_time=0.5, max_key_wait=5, keys=['z', 'm']):
        self.name = name
        self.experiment = experiment
        self.audio = audio
        self.fixation_time = fixation_time
        self.max_key_wait = max_key_wait
        self.keys = keys

    # Runs the current trial.
    def run(self):
        # Show the trial
        self.experiment.show_fixation(self.fixation_time)
        self.experiment.window.flip()

        self.audio.play()
        #self.experiment.show_decision() # left this out, got weird with timing audio/button press
        self.experiment.window.flip()

        # Wait for user input
        start_time = self.experiment.clock.getTime()  # You could also start a new clock for each user input
        keys = event.waitKeys(maxWait=self.max_key_wait, keyList=self.keys, timeStamped=self.experiment.clock,
                              clearEvents=True)
        if keys is not None:
            key, end_time = keys[0]
        else:  # If no keys were pressed:
            key = None
            end_time = self.experiment.clock.getTime()

        # Return the results
        return {
            'trial': self.name,
            'key': key,
            'start_time': start_time,
            'end_time': end_time
        }


# initialize the experiment
experiment = Experiment((800, 600), (-1, -1, -1), (1, 1, 1)) #defined in class Experiment; fill in screen size, text color, background color


trials = []
for i in range(len(stimuli)):
    audio = sound.Sound(path_to_sounds + '/' + stimuli['freq_category'][i] + '/' + stimuli['word'][i])
    trial = AudioTrial(experiment, stimuli['freq_category'][i] + '/' + stimuli['word'][i] + '_audio', audio)
    trials.append(trial)

trials = np.random.permutation(trials)

# instructions (defined in Experiment, screen and color: default ok; fill in text; stays on screen until button press)
experiment.show_message('druk z als je denkt dat wat je hoort een woord is,\ndruk m als je denkt dat het geen bestaand woord is\n\ndruk op een knop om te beginnen')

# run through all the trials and save results
results = []
for trial in trials:
    result = trial.run()
    results.append(result)

# Create a dataframe based on the results, and store them to a csv file
results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']  # Calculate all the reaction times
results.to_csv('results.csv')






