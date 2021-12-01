from myhdl import *
@block 

def complex_matrix_mult(

    #clk 
    clk,
    rst,
    #control
    vld_i,
    rdy_o,
    done_o,
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
    X_ADDR_W,
    Y_ADDR_W,
    Z_ADDR_W,
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

    k_cnt = Signal(intbv(0,min=0,max=K))
    m_cnt = Signal(intbv(0,min=0,max=M))
    n_cnt = Signal(intbv(0,min=0,max=N))

    k_cnt_r = Signal(intbv(0,min=0,max=K))
    m_cn_rt = Signal(intbv(0,min=0,max=M))
    n_cnt_r = Signal(intbv(0,min=0,max=N))


    k_cnt_full = Signal(bool(0))
    n_cnt_full = Signal(bool(0))

    x_re_r = Signal(bool(0))
    x_raddr_r = Signal(intbv(0)[X_ADDR_W:])

    y_re_r = Signal(bool(0))
    y_raddr_r = Signal(intbv(0)[Y_ADDR_W:])

    addr = Signal(bool(0))
    addr_r = Signal(bool(0))

    #communication between main and calc
    do_calc = Signal(bool(0))
    calc_finished = Signal(bool(0))


    @always(clk.posedge)
    def main_fsm_reg():
        if rst == 1:
            raise NotImplementedError
        else:
            if main_fsm_st_r == main_fsm_st_t.IDLE:
                if(rdy_o == 1 and vld_i == 1):
                    main_fsm_st_r.next = main_fsm_st_t.CALC

            elif main_fsm_st_r == main_fsm_st_t.CALC:
                if (calc_finished == 1):
                    main_fsm_st_r.next = main_fsm_st_t.WRITE
            elif main_fsm_st_r == main_fsm_st_t.WRITE_DATA:
                raise NotImplementedError
            elif main_fsm_st_r == main_fsm_st_t.DONE:
                raise NotImplementedError
            else: 
                raise ValueError("undefined state")

    @always_comb
    def main_fsm_comb():
        if main_fsm_st_r == main_fsm_st_t.IDLE:
            rdy_o.next = 1
        else:
            rdy_o.next = 0

        if main_fsm_st_r == main_fsm_st_t.CALC:
            do_calc.next = 1
        

    @always(clk.posedge)
    def calc_fsm():
        if rst == 1:
            raise NotImplementedError
        else:
            if calc_fsm_st_r == calc_fsm_st_t.IDLE:
                if (do_calc == 1):
                    calc_fsm_st_r.next = calc_fsm_st_t.READ
                    x_re_o.next = 1
                    x_re_o.next = 1

            elif calc_fsm_st_r == calc_fsm_st_t.READ:
                if (k_cnt_full == 1 and n_cnt_full == 1):
                    for i in range(K*N):
                        accu_array_r[i].next = accu_array_r[i] + x_column_array_r[]
                    calc_fsm_st_r.next = calc_fsm_st_t.MULT
            elif calc_fsm_st_r == calc_fsm_st_t.MULT:
                raise NotImplementedError
            elif calc_fsm_st_r == calc_fsm_st_t.DONE:
                raise NotImplementedError
            else: 
                raise ValueError("undefined state")
    @always_comb
    def calc_fsm_comb():
        if (k_cnt == K-1):
            k_cnt_full.next = 1
        else:
            k_cnt_full.next = 0
        
        if (n_cnt == N-1):
            n_cnt_full.next = 1
        else:
            n_cnt_full.next = 0
    
    @always(clk.posedge)
    def k_counter_p():
        if (rst == 1 or calc_fsm_st_r == calc_fsm_st_t.MULT):
            k_cnt.next = 0
        else:
            if (calc_fsm_st_r == calc_fsm_st_t.READ):
                if (k_cnt != K-1):
                    k_cnt.next = k_cnt + 1

    @always(clk.posedge)
    def n_counter_p():
        if (rst == 1 or calc_fsm_st_r == calc_fsm_st_t.MULT):
            n_cnt.next = 0
        else:
            if (calc_fsm_st_r == calc_fsm_st_t.READ):
                if (n_cnt != N-1):
                    n_cnt.next = n_cnt + 1

    @always_comb
    def addr_gen_p():
        x_raddr_o.next = m_cnt*K + k_cnt
        y_raddr_o.next = n_cnt*M + m_cnt

    @always(clk.posedge)
    def latency_handling_p():
        x_re_r.next = x_re_o
        x_raddr_r.next = x_raddr_o
        y_re_r.next = y_re_o
        y_raddr_r.next = y_raddr_o
        k_cnt_r.next = k_cnt
        n_cnt_r.next = n_cnt

        if (x_re_r == 1):
            x_column_array_r[k_cnt_r] = x_dat_i
            y_row_array_r[n_cnt_r] = y_dat_i





    return main_fsm_reg,main_fsm_comb,calc_fsm,calc_fsm_comb,k_counter_p,n_counter_p,addr_gen_p,latency_handling_p