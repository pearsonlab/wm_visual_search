import sys
import json
from psychopy import visual, gui, event, core
import random


class Stimuli:

    def __init__(self, win, timing, colors):
        self.win = win
        self.timing = timing
        self.colors = colors
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
                                         fillColor=(0, 0, 0), pos=(-0.6, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['1']]))
        self.memory.append(visual.Circle(self.win, units='height', radius=0.1,
                                         fillColorSpace='rgb255',
                                         lineColorSpace='rgb255',
                                         fillColor=(0, 0, 0), pos=(-0.2, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['2']]))
        self.memory.append(visual.Circle(self.win, units='height', radius=0.1,
                                         fillColorSpace='rgb255',
                                         lineColorSpace='rgb255',
                                         fillColor=(0, 0, 0), pos=(0.2, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['3']]))
        self.memory.append(visual.Circle(self.win, units='height', radius=0.1,
                                         fillColorSpace='rgb255',
                                         lineColorSpace='rgb255',
                                         fillColor=(0, 0, 0), pos=(0.6, 0),
                                         lineWidth=15,
                                         lineColor=self.colors[self.mem_keymap['4']]))
        self.memory.append(visual.TextStim(self.win, text='1',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(-0.6, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))
        self.memory.append(visual.TextStim(self.win, text='2',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(-0.2, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))
        self.memory.append(visual.TextStim(self.win, text='3',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(0.2, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))
        self.memory.append(visual.TextStim(self.win, text='4',
                                           font='Helvetica', alignHoriz='center',
                                           alignVert='center', units='height',
                                           pos=(0.6, 0), height=0.1,
                                           color=[255, 255, 255], colorSpace='rgb255'))

    def draw_fixation(self):
        self.fixation.draw()
        self.win.flip()
        core.wait(self.timing['fixation'])

    def draw_cue(self, color):
        visual.TextStim(self.win, text='Remember this color!',
                        font='Helvetica', alignHoriz='center',
                        alignVert='center', units='norm',
                        pos=(0, 0.5), height=0.1,
                        color=[255, 255, 255], colorSpace='rgb255',
                        wrapWidth=2).draw()
        self.cue.lineColor = self.colors[color]
        self.cue.draw()
        self.win.flip()
        core.wait(self.timing['cue'])
        self.win.flip()
        core.wait(self.timing['delay'])

    def do_search(self, trial):
        self.draw_fixation()
        # draw lines and circles
        if trial['target_pos'] == 'top':
            self.search['top'].lineColor = self.colors[
                trial['search_colors'][0]]
            self.search['top'].draw()
            self.search['bot'].lineColor = self.colors[
                trial['search_colors'][1]]
            self.search['bot'].draw()
            self.line[('bot', 'straight')].draw()
        else:
            self.search['top'].lineColor = self.colors[
                trial['search_colors'][1]]
            self.search['top'].draw()
            self.search['bot'].lineColor = self.colors[
                trial['search_colors'][0]]
            self.search['bot'].draw()
            self.line[('top', 'straight')].draw()
        self.line[(trial['target_pos'], trial['target_type'])].draw()

        self.win.flip()
        timer = core.MonotonicClock()
        key = event.waitKeys(
            maxWait=self.timing['search'], keyList=self.search_keymap.keys() + ['escape'])
        if key is None:
            pass
        elif key[0] == 'escape':
            core.quit()
        else:
            return (self.search_keymap[key[0]], timer.getTime())
        self.win.flip()
        key = event.waitKeys(
            maxWait=self.timing['blank'], keyList=self.search_keymap.keys() + ['escape'])
        if key is None:
            return ('timeout', timer.getTime())
        elif key[0] == 'escape':
            core.quit()
        else:
            return (self.search_keymap[key[0]], timer.getTime())

    def do_memory(self):
        for stim in self.memory:
            stim.draw()
        self.win.flip()
        timer = core.MonotonicClock()
        key = event.waitKeys(
            maxWait=self.timing['WM'], keyList=self.mem_keymap.keys() + ['escape'])
        self.win.flip()
        if key is None:
            return ('timeout', timer.getTime())
        elif key[0] == 'escape':
            core.quit()
        else:
            return (self.mem_keymap[key[0]], timer.getTime())


def text_keypress(win, text):
    display_text = visual.TextStim(win, text=text,
                                   font='Helvetica', alignHoriz='center',
                                   alignVert='center', units='norm',
                                   pos=(0, 0), height=0.1,
                                   color=[255, 255, 255], colorSpace='rgb255',
                                   wrapWidth=2)
    display_text.draw()
    win.flip()
    key = event.waitKeys()
    if key[0] == 'escape':
        core.quit()
    win.flip()


def text(win, text):
    display_text = visual.TextStim(win, text=text,
                                   font='Helvetica', alignHoriz='center',
                                   alignVert='center', units='norm',
                                   pos=(0, 0), height=0.1,
                                   color=[255, 255, 255], colorSpace='rgb255',
                                   wrapWidth=2)
    display_text.draw()
    win.flip()


def get_settings():
    dlg = gui.Dlg(title='Choose Settings')
    dlg.addField('Experiment Name:', 'WM_Search')
    dlg.addField('Subject ID:', '0000')
    dlg.addField('Number of blocks:', 10)
    dlg.show()
    if dlg.OK:
        return dlg.data
    else:
        sys.exit()


def get_window():
    return visual.Window(
        size=(1920, 1080), monitor="testMonitor", units="pix", screen=0,
        fullscr=True, colorSpace='rgb255', color=(0, 0, 0))


def run():
    (expname, sid, numblocks) = get_settings()
    win = get_window()
    win.flip()
    timing = {'fixation': 0.5,
              'cue': 1.0,
              'delay': 2,
              'search': 0.3,
              'WM': 3,
              'blank': 1.2,
              'intertrial': 0.5}
    colors = {'red': (227, 2, 24),
              'green': (95, 180, 46),
              'blue': (48, 62, 152),
              'yellow': (251, 189, 18)}
    stim = Stimuli(win, timing, colors)

    text_keypress(win, 'You will be presented with a circle which you will ' +
                       'need to remember the color of.\n\n\n'
                       'Hit any key to continue.')
    text_keypress(win, 'Then you will be presented with a series of ' +
                       'searches where you will need to press the key ' +
                       'corresponding to the way the tilted line is tilted.\n\n\n'
                       'Hit any key to continue.')
    text_keypress(win, 'At the end, you will be asked to pick the color ' +
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
        stim.draw_fixation()
        stim.draw_cue(block['cue_color'])
        for trial_num in range(len(block['trials'])):
            trial = block['trials'][trial_num]
            resp, time = stim.do_search(trial)
            block['trials'][trial_num]['search_response'] = resp
            block['trials'][trial_num]['search_response_time'] = time
            corr = (resp == trial['target_type'])
            block['trials'][trial_num]['search_correct'] = corr
            if not corr:
                if resp == 'timeout':
                    text(win, 'Timeout')
                else:
                    text(win, 'Incorrect')
            core.wait(timing['intertrial'])
        chosen_col, time = stim.do_memory()
        block_list[block_num]['mem_response'] = chosen_col
        block_list[block_num]['mem_response_time'] = time
        corr = (chosen_col == block['cue_color'])
        block_list[block_num]['mem_correct'] = corr
        if corr:
            text(win, 'Correct!')
        elif chosen_col == 'timeout':
            text(win, 'Timeout')
        else:
            text(win, 'Incorrect')
        core.wait(timing['intertrial'])
        with open(expname + '_' + sid + '.json', 'a') as f:
            f.write(json.dumps(block))
            f.write('\n')
        if block_num < len(block_list) - 1:
            text_keypress(win, 'Press any button when ready to continue.')
        else:
            text_keypress(win, 'Congratulations! You have finished.')

if __name__ == '__main__':
    run()
