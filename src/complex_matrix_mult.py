from myhdl import Signal,block,intbv,enum,always,always_comb,instances,ConcatSignal,ResetSignal,always_seq

def complex_mult_signed_real(dat1_real_i,dat1_imag_i,dat2_real_i,dat2_imag_i):
    dat_real_o = dat1_real_i.signed()*dat2_real_i.signed() - dat1_imag_i.signed()*dat2_imag_i.signed()
    return dat_real_o
def complex_mult_signed_imag(dat1_real_i,dat1_imag_i,dat2_real_i,dat2_imag_i):
    dat_imag_o = dat1_real_i.signed()*dat2_imag_i.signed() + dat1_imag_i.signed()*dat2_real_i.signed()
    return dat_imag_o


@block 
def complex_matrix_mult(

    #clk 
    clk,
    rst,
    #control
    input_vld_i,
    input_rdy_o,
    output_vld_o,
    output_rdy_i,
    #re
    re_o,
    #in1
    x_raddr_o,
    x_dat_i,
    #in2
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

    COMPLEX_DAT_WIDTH = int(DAT_WIDTH/2)
    COMPLEX_ACCU_WIDTH = int(ACCU_WIDTH/2)

    #arrray of accumulators:
    accu_array_real_r = [Signal(intbv(0)[COMPLEX_ACCU_WIDTH:].signed()) for i in range(K*N)]
    accu_array_imag_r = [Signal(intbv(0)[COMPLEX_ACCU_WIDTH:].signed()) for i in range(K*N)]
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
    n_cnt_r = Signal(intbv(0,min=0,max=N))


    k_cnt_full = Signal(bool(0))
    n_cnt_full = Signal(bool(0))
    m_cnt_full = Signal(bool(0))

    re_r = Signal(bool(0))

    z_write_cnt = Signal(intbv(0,min=0,max=K*N))
    z_write_cnt_full = Signal(bool(0))

    #communication between main and calc
    do_calc = Signal(bool(0))
    calc_finished = Signal(bool(0))

    #latency
    mult_r = Signal(bool(0))

    #internal signals 
    input_rdy_s = Signal(bool(0))
    re_s = Signal(bool(0))



    @always_seq(clk.posedge,reset=rst)
    def main_fsm_reg_p():
        if rst == 1:
            main_fsm_st_r.next = main_fsm_st_t.IDLE
        else:
            if main_fsm_st_r == main_fsm_st_t.IDLE:
                if(input_rdy_s == 1 and input_vld_i == 1):
                    main_fsm_st_r.next = main_fsm_st_t.CALC

            elif main_fsm_st_r == main_fsm_st_t.CALC:
                if (calc_finished == 1):
                    main_fsm_st_r.next = main_fsm_st_t.WRITE_DATA

            elif main_fsm_st_r == main_fsm_st_t.WRITE_DATA:
                if (z_write_cnt_full == 1):
                    main_fsm_st_r.next = main_fsm_st_t.DONE

            elif main_fsm_st_r == main_fsm_st_t.DONE:
                if (output_rdy_i  == 1):
                    main_fsm_st_r.next = main_fsm_st_t.IDLE
            else: 
                raise ValueError("undefined state")

    @always_comb
    def main_fsm_comb_p():
        if main_fsm_st_r == main_fsm_st_t.IDLE:
            input_rdy_s.next = 1
        else:
            input_rdy_s.next = 0

        if main_fsm_st_r == main_fsm_st_t.CALC:
            do_calc.next = 1
        else: 
            do_calc.next = 0

        if main_fsm_st_r == main_fsm_st_t.DONE:
            output_vld_o.next = 1
        else:
            output_vld_o.next = 0
        
        if main_fsm_st_r == main_fsm_st_t.WRITE_DATA:
            z_we_o.next = 1
        else:
            z_we_o.next = 0

        if z_write_cnt == K*N - 1:
            z_write_cnt_full.next = 1
        else:
            z_write_cnt_full.next = 0

    @always_seq(clk.posedge,reset=rst)
    def z_write_counter_p():
        if (rst == 1 or main_fsm_st_r == main_fsm_st_t.DONE):
            z_write_cnt.next = 0
        else:
            if (main_fsm_st_r == main_fsm_st_t.WRITE_DATA):
                if (z_write_cnt != K*N-1):
                    z_write_cnt.next = z_write_cnt + 1
        
        

    @always_seq(clk.posedge,reset=rst)
    def calc_fsm_reg_p():
        if rst == 1:
            calc_fsm_st_r.next = calc_fsm_st_t.IDLE
        else:
            if calc_fsm_st_r == calc_fsm_st_t.IDLE:
                if (do_calc == 1):
                    calc_fsm_st_r.next = calc_fsm_st_t.READ

            elif calc_fsm_st_r == calc_fsm_st_t.READ:
                if (k_cnt_full == 1 and n_cnt_full == 1):
                    calc_fsm_st_r.next = calc_fsm_st_t.MULT

            elif calc_fsm_st_r == calc_fsm_st_t.MULT:
                if (m_cnt_full == 1):
                    calc_fsm_st_r.next = calc_fsm_st_t.DONE
                else:
                    calc_fsm_st_r.next = calc_fsm_st_t.READ

            elif calc_fsm_st_r == calc_fsm_st_t.DONE:
                calc_fsm_st_r.next = calc_fsm_st_t.IDLE

                
            else: 
                raise ValueError("undefined state")

    @always_comb
    def calc_fsm_comb_p():
        if (k_cnt == K-1):
            k_cnt_full.next = 1
        else:
            k_cnt_full.next = 0
        
        if (n_cnt == N-1):
            n_cnt_full.next = 1
        else:
            n_cnt_full.next = 0
        
        if (m_cnt == M-1):
            m_cnt_full.next = 1
        else:
            m_cnt_full.next = 0

        if (calc_fsm_st_r == calc_fsm_st_t.DONE):
            calc_finished.next = 1
        else:
            calc_finished.next = 0
        
        if (calc_fsm_st_r == calc_fsm_st_t.READ):
            re_s.next = 1
        else:
            re_s.next = 0

    
    
    @always_seq(clk.posedge,reset=rst)
    def k_counter_p():
        if (rst == 1 or calc_fsm_st_r == calc_fsm_st_t.MULT):
            k_cnt.next = 0
        else:
            if (calc_fsm_st_r == calc_fsm_st_t.READ):
                if (k_cnt != K-1):
                    k_cnt.next = k_cnt + 1

    @always_seq(clk.posedge,reset=rst)
    def n_counter_p():
        if (rst == 1 or calc_fsm_st_r == calc_fsm_st_t.MULT):
            n_cnt.next = 0
        else:
            if (calc_fsm_st_r == calc_fsm_st_t.READ):
                if (n_cnt != N-1):
                    n_cnt.next = n_cnt + 1
    @always_seq(clk.posedge,reset=rst)
    def m_counter_p():
        if (rst == 1 or calc_fsm_st_r == calc_fsm_st_t.IDLE):
            m_cnt.next = 0
        else:
            if (calc_fsm_st_r == calc_fsm_st_t.MULT and n_cnt_full == 1 and k_cnt_full == 1):
                if (m_cnt != M-1):
                    m_cnt.next = m_cnt + 1

    @always_comb
    def addr_gen_p():
        x_raddr_o.next = k_cnt*M + m_cnt
        y_raddr_o.next = m_cnt*N + n_cnt
        z_waddr_o.next = z_write_cnt
        z_dat_o.next = ConcatSignal(accu_array_real_r[z_write_cnt],accu_array_imag_r[z_write_cnt])

    @always_seq(clk.posedge,reset=rst)
    def latency_handling_p():
        re_r.next = re_s
        k_cnt_r.next = k_cnt
        n_cnt_r.next = n_cnt

        if (re_r == 1):
            x_column_array_r[k_cnt_r].next = x_dat_i
            y_row_array_r[n_cnt_r].next = y_dat_i

        if calc_fsm_st_r == calc_fsm_st_t.MULT:
            mult_r.next = 1
        else:
            mult_r.next = 0


    #drive outputs
    @always_comb
    def outputs_p():
        input_rdy_o.next = input_rdy_s
        re_o.next = re_s

    #multiplication
    #If mult_r do multiplication, if main fsm returned to idle- clear
    @always(clk.posedge)
    def multiplication_p():
        for k in range(K):
            for n in range(N):
                if (mult_r == 1):
                    x_real = x_column_array_r[k][2*COMPLEX_DAT_WIDTH:COMPLEX_DAT_WIDTH].signed()
                    x_imag = x_column_array_r[k][COMPLEX_DAT_WIDTH:].signed()
                    y_real = y_row_array_r[n][2*COMPLEX_DAT_WIDTH:COMPLEX_DAT_WIDTH].signed()
                    y_imag = y_row_array_r[n][COMPLEX_DAT_WIDTH:].signed()
                    out_real = complex_mult_signed_real(x_real,x_imag,y_real,y_imag)
                    out_imag = complex_mult_signed_imag(x_real,x_imag,y_real,y_imag)
                    accu_array_real_r[k*N+n].next = accu_array_real_r[k*N+n].signed() + out_real
                    accu_array_imag_r[k*N+n].next = accu_array_imag_r[k*N+n].signed() + out_imag
                elif(main_fsm_st_r == main_fsm_st_t.IDLE):
                    accu_array_real_r[k*N+n].next = 0
                    accu_array_imag_r[k*N+n].next = 0
            





    return instances()