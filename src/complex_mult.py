REAL_WIDTH = 16
IMAG_WIDTH = 16
REAL_OUT_WIDTH = 32
IMAG_OUT_WIDTH = 32
from myhdl import *

#Real bits are MSB and imag LSB

@block
def complex_mult(
    #inputs:
    dat1_real_i,
    dat1_imag_i,
    dat2_real_i,
    dat2_imag_i,
    
    #output:
    dat_real_o,
    dat_imag_o
):
    
    @always_comb
    def mult():

        dat_real_o.next = dat1_real_i*dat2_real_i - dat1_imag_i*dat2_imag_i
        dat_imag_o.next = dat1_real_i*dat2_imag_i + dat1_imag_i*dat2_real_i

    return mult




