import sys
import json
from psychopy import visual, gui, event, core
import random
import numpy as np

TESTING = False  # turns off event marking
if not TESTING:
    try:
        from Plexon import PlexClient
        from makepulse import makepulse
    except ImportError:
        print "Plexon and/or NI-DAQ libraries not available on machine."


class Stimuli:

    def __init__(self, win, timing, colors, mode):
        self.win = win
        self.timing = timing
        self.colors = colors
        self.mode = mode
        self.fixation = visual.TextStim(self.win, text='+',
                                        alignHoriz='center',
                                        alignVert='center', units='norm',
                                        pos=(0, 0), height=0.3,
                                        color=[255, 255, 255], colorSpace='rgb255',
                                        wrapWidth=2)
        self.cue = visual.Circle(self.win, units='height', radius=0.1,
                                 fillColorSpace='rgb255', lineColorSpace='rgb255',
                                 fillColor=(0, 0, 0), pos=(0, 0), lineWidth=15)

        self.search_keymap = {'1': 'left', '2': 'right'}
        self.search = {}
        self.search['top'] = visual.Circle(self.win, units='height', radius=0.1,
                                           fillColorSpace='rgb255',
                                           lineColorSpace='rgb255',
                                           fillColor=(0, 0, 0), pos=(0, 0.2),
                                           lineWidth=15)
        self.search['bot'] = visual.Circle(self.win, units='height', radius=0.1,
                                           fillColorSpace='rgb255',
                                           lineColorSpace='rgb255',
                                           fillColor=(0, 0, 0), pos=(0, -0.2),
                                           lineWidth=15)
        line_color = (255, 255, 255)
        self.line = {}
        self.line[('top', 'left')] = visual.Line(self.win, lineColor=line_color,
                                                 units='height', start=(-0.06, 0.26),
                                                 end=(0.06, 0.14), lineWidth=15,
                                                 lineColorSpace='rgb255')
        self.line[('top', 'right')] = visual.Line(self.win, lineColor=line_color,
                                                  units='height', start=(0.06, 0.26),
                                                  end=(-0.06, 0.14), lineWidth=15,
                                                  lineColorSpace='rgb255')
        self.line[('top', 'straight')] = visual.Line(self.win, lineColor=line_color,
                                                     units='height', start=(0, 0.26),
                                                     end=(0, 0.14), lineWidth=15,
                                                     lineColorSpace='rgb255')
        self.line[('bot', 'left')] = visual.Line(self.win, lineColor=line_color,
                                                 units='height', start=(-0.06, -0.14),
                                                 end=(0.06, -0.26), lineWidth=15,
                                                 lineColorSpace='rgb255')
        self.line[('bot', 'right')] = visual.Line(self.win, lineColor=line_color,
                                                  units='height', start=(0.06, -0.14),
                                                  end=(-0.06, -0.26), lineWidth=15,
                                                  lineColorSpace='rgb255')
        self.line[('bot', 'straight')] = visual.Line(self.win, lineColor=line_color,
                                                     units='height', start=(0, -0.26),
                                                     end=(0, -0.14), lineWidth=15,
                                                     lineColorSpace='rgb255')

        self.mem_keymap = {
            '1': 'blue', '2': 'yellow', '3': 'green', '4': 'red'}
        self.memory = []
        self.memory.append(visual.TextStim(self.win, text='Which color do you remember?',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='norm',
                                           pos=(0, 0.5), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255',
                                           wrapWidth=2))
        self.memory.append(visual.Circle(self.win, units='height', radius=0.1,
                                         fillColorSpace='rgb255',
                                         lineColorSpace='rgb255',
                                         fillColor=(0, 0, 0), pos=(-0.45, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['1']]))
        self.memory.append(visual.Circle(self.win, units='height', radius=0.1,
                                         fillColorSpace='rgb255',
                                         lineColorSpace='rgb255',
                                         fillColor=(0, 0, 0), pos=(-0.15, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['2']]))
        self.memory.append(visual.Circle(self.win, units='height', radius=0.1,
                                         fillColorSpace='rgb255',
                                         lineColorSpace='rgb255',
                                         fillColor=(0, 0, 0), pos=(0.15, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['3']]))
        self.memory.append(visual.Circle(self.win, units='height', radius=0.1,
                                         fillColorSpace='rgb255',
                                         lineColorSpace='rgb255',
                                         fillColor=(0, 0, 0), pos=(0.45, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['4']]))
        self.memory.append(visual.TextStim(self.win, text='1',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(-0.45, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))
        self.memory.append(visual.TextStim(self.win, text='2',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(-0.15, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))
        self.memory.append(visual.TextStim(self.win, text='3',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(0.15, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))
        self.memory.append(visual.TextStim(self.win, text='4',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(0.45, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))
        if not TESTING:
            if self.mode == 'Plexon':
                self.plexon = PlexClient.PlexClient()
                self.plexon.InitClient()
                if not self.plexon.IsSortClientRunning():
                    raise Exception('Please start Sort Client to use Plexon.')
                print 'Using Plexon'
            elif self.mode == 'NI-DAQ':
                print 'Using NI-DAQ'
            elif self.mode == 'Photodiode':
                print 'Using Photodiode'
            else:
                raise Exception('Event marking mode unknown')
            # self.mark_event(channel) to mark events
            # channel 1: cue presentation
            # channel 2: search presentation
            # channel 3: WM presentation
            # channel 4: Subject response

    def mark_event(self, channel):
        """
        Mark event using the predetermined method. Return time it took to run
        in order to account for non-instantaneous marking on the photodiode.
        """
        timer = core.Clock()
        if not TESTING:
            if self.mode == 'Plexon':
                self.plexon.MarkEvent(channel)
            elif self.mode == 'NI-DAQ':
                if channel == 2 or channel == 3:
                    makepulse()
            elif self.mode == 'Photodiode':
                self.flicker(channel)
        return timer.getTime()

    def flicker(self, value):
        """
        Send a binary signal (value) to the photodiode by flickering a white
        circle in the bottom right hand corner.
        """
        circle = visual.Circle(self.win, units='height', radius=0.1,
                               fillColorSpace='rgb255',
                               lineColorSpace='rgb255',
                               fillColor=(0, 0, 0), pos=(0.78, -0.4),
                               lineColor=(0, 0, 0))
        value = np.binary_repr(value)
        # zero pad to 8 bits and add stop and start bits
        value = '1' + (8 - len(value)) * '0' + value + '1'
        # draw bits
        for bit in value:
            if bit == '1':
                circle.fillColor = (255, 255, 255)
                circle.draw()
            if bit == '0':
                circle.fillColor = (0, 0, 0)
                circle.draw()
            self.win.flip(clearBuffer=False)
        # clear circle on both buffers
        circle.fillColor = (0, 0, 0)
        circle.draw()
        self.win.flip(clearBuffer=False)
        circle.draw()

    def draw_fixation(self):
        self.fixation.draw()
        self.win.flip()
        core.wait(self.timing['fixation'])
        self.win.flip()

    def draw_cue(self, color):
        text = visual.TextStim(self.win, text='Remember this color!',
                               font='Helvetica', alignHoriz='center',
                               alignVert='center', units='norm',
                               pos=(0, 0.5), height=0.1,
                               color=[255, 255, 255], colorSpace='rgb255',
                               wrapWidth=2)
        self.cue.lineColor = self.colors[color]
        draw_objs = [text, self.cue]
        map(autoDraw_on, draw_objs)
        self.win.flip()
        offset = self.mark_event(1)
        core.wait(self.timing['cue'] - offset)
        cue_off = core.getTime()
        map(autoDraw_off, draw_objs)
        self.win.flip()
        self.win.flip()
        core.wait(self.timing['delay'])
        return cue_off

    def do_search(self, trial):
        self.draw_fixation()
        draw_objs = []
        # draw lines and circles
        if trial['target_pos'] == 'top':
            self.search['top'].lineColor = self.colors[
                trial['search_colors'][0]]
            draw_objs.append(self.search['top'])
            self.search['bot'].lineColor = self.colors[
                trial['search_colors'][1]]
            draw_objs.append(self.search['bot'])
            draw_objs.append(self.line[('bot', 'straight')])
        else:
            self.search['top'].lineColor = self.colors[
                trial['search_colors'][1]]
            draw_objs.append(self.search['top'])
            self.search['bot'].lineColor = self.colors[
                trial['search_colors'][0]]
            draw_objs.append(self.search['bot'])
            draw_objs.append(self.line[('top', 'straight')])
        draw_objs.append(self.line[(trial['target_pos'], trial['target_type'])])

        map(autoDraw_on, draw_objs)
        search_start = core.getTime()
        self.win.flip()
        offset = self.mark_event(2)
        key = event.waitKeys(
            maxWait=self.timing['search'] - offset, keyList=self.search_keymap.keys() + ['escape'])
        if key is None:
            pass
        elif key[0] == 'escape':
            if not TESTING and self.mode == 'Plexon':
                self.plexon.CloseClient()
            core.quit()
        else:
            map(autoDraw_off, draw_objs)
            self.win.flip()
            self.win.flip()
            resp_time = core.getTime()
            offset = self.mark_event(4)
            return (self.search_keymap[key[0]], search_start, resp_time, resp_time)
        map(autoDraw_off, draw_objs)
        off_time = core.getTime()
        self.win.flip()
        self.win.flip()
        key = event.waitKeys(
            maxWait=self.timing['blank'], keyList=self.search_keymap.keys() + ['escape'])
        if key is None:
            return ('timeout', search_start, off_time, core.getTime())
        elif key[0] == 'escape':
            if not TESTING and self.mode == 'Plexon':
                self.plexon.CloseClient()
            core.quit()
        else:
            resp_time = core.getTime()
            offset = self.mark_event(4)
            return (self.search_keymap[key[0]], search_start, off_time, resp_time)

    def do_memory(self):
        map(autoDraw_on, self.memory)
        start_time = core.getTime()
        self.win.flip()
        offset = self.mark_event(3)
        key = event.waitKeys(
            maxWait=self.timing['WM'] - offset, keyList=self.mem_keymap.keys() + ['escape'])
        map(autoDraw_off, self.memory)
        self.win.flip()
        self.win.flip()
        if key is None:
            return ('timeout', start_time, core.getTime())
        elif key[0] == 'escape':
            if not TESTING and self.mode == 'Plexon':
                self.plexon.CloseClient()
            core.quit()
        else:
            resp_time = core.getTime()
            offset = self.mark_event(4)
            return (self.mem_keymap[key[0]], start_time, resp_time)

    def text_keypress(self, text):
        display_text = visual.TextStim(self.win, text=text,
                                       font='Helvetica', alignHoriz='center',
                                       alignVert='center', units='norm',
                                       pos=(0, 0), height=0.1,
                                       color=[255, 255, 255], colorSpace='rgb255',
                                       wrapWidth=2)
        display_text.draw()
        self.win.flip()
        key = event.waitKeys()
        if key[0] == 'escape':
            if not TESTING and self.mode == 'Plexon':
                self.plexon.CloseClient()
            core.quit()
        self.win.flip()

    def text(self, text):
        display_text = visual.TextStim(self.win, text=text,
                                       font='Helvetica', alignHoriz='center',
                                       alignVert='center', units='norm',
                                       pos=(0, 0), height=0.1,
                                       color=[255, 255, 255], colorSpace='rgb255',
                                       wrapWidth=2)
        display_text.draw()
        self.win.flip()


def get_settings():
    dlg = gui.Dlg(title='Choose Settings')
    dlg.addField('Experiment Name:', 'WM_Search')
    dlg.addField('Subject ID:', '0000')
    dlg.addField('Number of blocks:', 10)
    dlg.addField('Speed Factor:', 1.0)
    dlg.addField('Event Marking Mode:', choices=('Plexon', 'NI-DAQ', 'Photodiode'))
    dlg.show()
    if dlg.OK:
        return dlg.data
    else:
        sys.exit()


def get_window():
    return visual.Window(
        winType='pyglet', monitor="testMonitor", units="pix", screen=1,
        fullscr=True, colorSpace='rgb255', color=(0, 0, 0))

def autoDraw_on(stim):
    stim.autoDraw = True
    return stim

def autoDraw_off(stim):
    stim.autoDraw = False
    return stim

def run():
    (expname, sid, numblocks, speed, mode) = get_settings()
    win = get_window()
    win.flip()
    timing = {'fixation': 0.5,
              'cue': 1.0,
              'delay': 2,
              'search': 0.3,
              'WM': 3 / speed,
              'blank': 2 / speed,
              'intertrial': 0.5 / speed}
    colors = {'red': (227, 2, 24),
              'green': (95, 180, 46),
              'blue': (48, 62, 152),
              'yellow': (251, 189, 18)}
    stim = Stimuli(win, timing, colors, mode)

    stim.text_keypress('You will be presented with a circle which you will ' +
                       'need to remember the color of.\n\n\n'
                       'Hit any key to continue.')
    stim.text_keypress('Then you will be presented with a series of ' +
                       'searches where you will need to press the key ' +
                       'corresponding to the way the tilted line is tilted.\n\n\n'
                       'Hit any key to continue.')
    stim.text_keypress('At the end, you will be asked to pick the color ' +
                       'that you were asked to remember out of four ' +
                       'possibilities.\n\n\n'
                       'Hit any key to continue.')
    # the first color is the search target, second is the distractor
    trial_types = [('red', 'blue'), ('red', 'green'), ('red', 'yellow'),
                   ('blue', 'red'), ('blue', 'green'), ('blue', 'yellow'),
                   ('green', 'red'), ('green', 'blue'), ('green', 'yellow'),
                   ('yellow', 'red'), ('yellow', 'green'), ('yellow', 'blue')]
    block_list = []

    # construct blocks
    for block_num in range(numblocks):
        block = {}
        block['speed_factor'] = speed
        block['block_num'] = block_num
        block['cue_color'] = random.choice(colors.keys())
        random.shuffle(trial_types)
        trial_list = []
        # construct trials
        for trial_num in range(len(trial_types)):
            trial = {}
            trial['trial_num'] = trial_num
            trial['target_type'] = random.choice(['left', 'right'])
            trial['search_colors'] = trial_types[trial_num]
            target_col = trial['search_colors'][0]
            distract_col = trial['search_colors'][1]
            if block['cue_color'] == target_col:
                trial['validity'] = 'valid'
            elif block['cue_color'] == distract_col:
                trial['validity'] = 'invalid'
            else:
                trial['validity'] = 'neutral'
            trial['target_pos'] = random.choice(['top', 'bot'])
            trial_list.append(trial)
        block['trials'] = trial_list
        block_list.append(block)

    # run trials
    for block_num in range(len(block_list)):
        block = block_list[block_num]
        block['fixation_on'] = core.getTime()
        stim.draw_fixation()
        block['fixation_off'] = core.getTime()
        block['cue_on'] = core.getTime()
        block['cue_off'] = stim.draw_cue(block['cue_color'])
        for trial_num in range(len(block['trials'])):
            trial = block['trials'][trial_num]
            resp, start_time, off_time, end_time = stim.do_search(trial)
            block['trials'][trial_num]['search_response'] = resp
            block['trials'][trial_num]['search_start_time'] = start_time
            block['trials'][trial_num]['search_off_time'] = off_time
            block['trials'][trial_num]['search_resp_time'] = end_time
            corr = (resp == trial['target_type'])
            block['trials'][trial_num]['search_correct'] = corr
            if not corr:
                if resp == 'timeout':
                    stim.text('Timeout')
                else:
                    stim.text('Incorrect')
            core.wait(timing['intertrial'])
        chosen_col, start_time, end_time = stim.do_memory()
        block_list[block_num]['mem_response'] = chosen_col
        block_list[block_num]['mem_response_start'] = start_time
        block_list[block_num]['mem_response_resp'] = end_time
        corr = (chosen_col == block['cue_color'])
        block_list[block_num]['mem_correct'] = corr
        if corr:
            stim.text('Correct!')
        elif chosen_col == 'timeout':
            stim.text('Timeout')
        else:
            stim.text('Incorrect')
        core.wait(timing['intertrial'])
        with open(expname + '_' + sid + '.json', 'a') as f:
            f.write(json.dumps(block))
            f.write('\n')
        if block_num < len(block_list) - 1:
            stim.text_keypress('Press any button when ready to continue.')
        else:
            stim.text_keypress('Congratulations! You have finished.')

if __name__ == '__main__':
    run()
