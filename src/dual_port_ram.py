from myhdl import *

@block 

def dual_port_ram(
    #clk 
    clk,
    #write
    we_i,
    waddr_i,
    din_i,
    #read
    re_i,
    raddr_i,
    dout_o,

    #generics
    ADDR_WIDTH = 8,
    DATA_WIDTH = 8
):

    MEM_SIZE = 2**ADDR_WIDTH

    #registered memory block
    ram_array_r = [Signal(intbv(0)[DATA_WIDTH:]) for i in range(MEM_SIZE)]

    @always(clk.posedge)
    def write_p():
        if (we_i == 1):
            ram_array_r[waddr_i].next = din_i

    @always(clk.posedge)
    def read_p():
        if (re_i == 1):
            dout_o.next = ram_array_r[raddr_i]

    return  write_p,read_p