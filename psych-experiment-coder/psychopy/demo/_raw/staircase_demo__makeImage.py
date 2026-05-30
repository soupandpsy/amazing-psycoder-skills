# Source: staircase_demo (demos/staircase_demo)
# Project URL: https://gitlab.pavlovia.org/demos/staircase_demo
# Original file: Stimuli/makeImage.py
'''
a script to make grating stimuli as images to present online (untill these are 
implemented in psychoJS)
'''
from psychopy import core, visual, event

# create a window to draw in
win = visual.Window([400, 400.0], allowGUI=False)

# Create Gabor image
gabor = visual.GratingStim(win, tex="sin", mask="gauss", texRes=256, 
           size=[1.0, 1.0], sf=[10, 0], ori = 0, name='gabor1', opacity = 1)

gabor.draw()
win.flip()
#save the current image
win._getFrame().save("gratingStim%s.png"%(gabor.opacity))