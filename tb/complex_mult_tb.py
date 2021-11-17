import sys
sys.path.append('C:\\Users\\piotrek\\Desktop\\nauka\\7 semestr\\esl\\tutor\\project\\src')
from myhdl import *
#from ..src.complex_mult import complex_mult
from complex_mult import complex_mult
import random
import numpy as np
random.seed(6)
randrange = random.randrange

@block
def test_complex_mult():
    dat1_real,dat1_imag,dat2_real,dat2_imag = [Signal(modbv(0,min=-32768,max=32767)) for i in range(4)]
    dat_out_real = Signal(modbv(0,min=-2147483648,max=2147483647))
    dat_out_imag = Signal(modbv(0,min=-2147483648,max=2147483647))
    #dat1 = ConcatSignal(dat1_real,dat1_imag)
    #dat2 = ConcatSignal(dat2_real,dat2_imag)


    mult1 = complex_mult(dat1_real,dat1_imag,dat2_real,dat2_imag,dat_out_real,dat_out_imag)

    @instance
    def stimulous():
        for i in range(20):
            dat1_real.next,dat1_imag.next,dat2_real.next,dat2_imag.next = [Signal(modbv(i+1,min=-32768,max=32767)) 
                                                                           for i in range(4)]
            dat_test = (dat1_real+1j*dat1_imag)*(dat2_real+1j*dat2_imag)
            #dat_test_real = hex(int(np.real(dat_test)))
            #dat_test_imag = hex(int(np.imag(dat_test)))

            print(dat_test)
            print(dat_out_real)
            print(dat_out_imag)
            yield delay(10)

    return mult1,stimulous
tb = test_complex_mult()
tb.config_sim(trace=True)
tb.run_sim()