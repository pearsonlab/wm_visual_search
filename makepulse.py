# coding= latin-1

from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *

LO_TIME = 0.01    # amount of time pulse is low (in s)
HI_TIME = 0.01    # amount of time pulse is high (in s)
DELAY = 1e-6      # how long to wait before pulsing
COUNTER = "Dev3/ctr1"

def makepulse():
    pulse_gene1 = ContinuousPulseTrainGeneration("dev3/ctr1", reset=True)
    pulse_gene1.start()
    pulse_gene1.wait()
    pulse_gene1.stop()
    pulse_gene1.clear()


class ContinuousPulseTrainGeneration():
    """ Class to create a continuous pulse train on a counter
    
    Usage:  pulse = ContinuousTrainGeneration(period [s],
                duty_cycle (default = 0.5), counter (default = "dev1/ctr0"),
                reset = True/False)
            pulse.start()
            pulse.stop()
            pulse.clear()
    """
    def __init__(self, counter="Dev1/ctr0", reset=False):
        if reset:
            DAQmxResetDevice(counter.split('/')[0])
        taskHandle = TaskHandle(0)
        DAQmxCreateTask("",byref(taskHandle))
        DAQmxCreateCOPulseChanTime(taskHandle,counter,"",DAQmx_Val_Seconds,DAQmx_Val_Low, 
            DELAY, LO_TIME, HI_TIME)
        # DAQmxCfgImplicitTiming(taskHandle,DAQmx_Val_ContSamps,1000)
        self.taskHandle = taskHandle
    def start(self):
        DAQmxStartTask(self.taskHandle)
    def wait(self):
        DAQmxWaitUntilTaskDone(self.taskHandle,10.0)
    def stop(self):
        DAQmxStopTask(self.taskHandle)
    def clear(self):
        DAQmxClearTask(self.taskHandle)


if __name__=="__main__":
    makepulse()
   


