import sys
sys.path.append('C:\\Users\\piotrek\\Desktop\\nauka\\7 semestr\\esl\\tutor\\project\\myhdl_first_project\\src')
from myhdl import *
#from ..src.complex_mult import complex_mult
from complex_mult import complex_mult
import random
import numpy as np
random.seed(6)
randrange = random.randrange

@block
def test_complex_mult(dat1_real,dat1_imag,dat2_real,dat2_imag,dat_out_real,dat_out_imag):

    
    @instance
    def stimulous():
        for i in range(20):
            dat1_real.next,dat1_imag.next,dat2_real.next,dat2_imag.next = [Signal(modbv(i+j,min=-32768,max=32767)) 
                                                                           for j in range(4)]
            print(dat1_real)
            yield delay(10)
        raise StopSimulation()

    return stimulous

dat1_real,dat1_imag,dat2_real,dat2_imag = [Signal(modbv(0,min=-32768,max=32767)) for i in range(4)]
dat_out_real = Signal(modbv(0,min=-2147483648,max=2147483647))
dat_out_imag = Signal(modbv(0,min=-2147483648,max=2147483647))
mult1 = complex_mult(dat1_real,dat1_imag,dat2_real,dat2_imag,dat_out_real,dat_out_imag)
#dat1 = ConcatSignal(dat1_real,dat1_imag)
#dat2 = ConcatSignal(dat2_real,dat2_imag)


tb = test_complex_mult(dat1_real,dat1_imag,dat2_real,dat2_imag,dat_out_real,dat_out_imag)
tb.config_sim(trace=True)
tb.run_sim()