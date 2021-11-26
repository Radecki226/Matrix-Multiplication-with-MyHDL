from myhdl import *

@block 

def dual_port_ram(

    #clk 
    clk,
    rst,
    #control
    vld_i,
    rdy_o,
    #in1
    x_re_o,
    x_raddr_o,
    x_dat_i,
    #in2
    y_re_o,
    y_raddr_o,
    y_dat_i,
    
    #out
    z_we_o,
    z_waddr_o,
    z_dat_o,

    #generics
    DAT_WIDTH = 32,
    K = 2,
    M = 2,
    N = 2,
    ACCU_WIDTH = 80
):

    #arrray of accumulators:
    accu_array_r = [Signal(intbv(0)[ACCU_WIDTH:]) for i in range(K*N)]
    x_column_array_r = [Signal(intbv(0)[DAT_WIDTH:]) for i in range(K)]
    y_row_array_r = [Signal(intbv(0)[DAT_WIDTH:]) for i in range(N)]

    main_fsm_st_t = enum('IDLE', 'CALC', 'WRITE_DATA','DONE')
    main_fsm_st_r = Signal(main_fsm_st_t.IDLE)

    calc_fsm_st_t = enum('IDLE','READ','MULT','DONE')
    calc_fsm_st_r = Signal(calc_fsm_st_t.IDLE)

    m_cnt = Signal(intbv(0,min=0,max=M-1))
    k_cnt = Signal(intbv(0,min=0,max=K-1))
    n_cnt = Signal(intbv(0,min=0,max=N-1))

    k_cnt_full = Signal(bool(0))
    n_cnt_full = Signal(bool(0))

    re = Signal(bool(0))
    re_r = Signal(bool(0))

    addr = Signal(bool(0))
    addr_r = Signal(bool(0))


    @always(clk.posedge)
    def main_fsm_reg():
        if rst == 1:
            raise NotImplementedError
        else:
            if main_fsm_st_r == main_fsm_st_t.IDLE:
                raise NotImplementedError
            elif main_fsm_st_r == main_fsm_st_t.CALC:
                raise NotImplementedError
            elif main_fsm_st_r == main_fsm_st_t.WRITE_DATA:
                raise NotImplementedError
            elif main_fsm_st_r == main_fsm_st_t.DONE:
                raise NotImplementedError
            else: 
                raise ValueError("undefined state")

    @always_comb
    def main_fsm_comb():
        if main_fsm_st_r == main_fsm_st_t.IDLE:

    @always(clk.posedge)
    def calc_fsm():
        if rst == 1:
            raise NotImplementedError
        else:
            if calc_fsm_st_r == calc_fsm_st_t.IDLE:
                raise NotImplementedError
            elif calc_fsm_st_r == calc_fsm_st_t.READ:
                raise NotImplementedError
            elif calc_fsm_st_r == calc_fsm_st_t.MULT:
                raise NotImplementedError
            elif calc_fsm_st_r == calc_fsm_st_t.DONE:
                raise NotImplementedError
            else: 
                raise ValueError("undefined state")
    


    return FSM