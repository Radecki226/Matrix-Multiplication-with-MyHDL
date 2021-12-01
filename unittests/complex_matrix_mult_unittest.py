import unittest
import sys
sys.path.append('C:\\Users\\piotrek\\Desktop\\nauka\\7 semestr\\esl\\tutor\\project\\myhdl_first_project\\src')
from myhdl import *
from complex_matrix_mult import complex_matrix_mult
from dual_port_ram import dual_port_ram
import os
import numpy as np
np.random.seed(2021)


class MatrixMultTest(unittest.TestCase):
    

    def testWriteAndRead(self):
        """Test 1: Fill entire array with numbers and read it"""


        @block
        def test_mm1():
            K = 2
            M = 100
            N = 2
            COMPLEX_DAT_W = 16
            MAX_INT = 32768
            MIN_INT = -32768
            #clk
            clk = Signal(bool(0))
            #rst
            rst = Signal(bool(0))
            #control
            mm_valid = Signal(bool(0))
            mm_ready = Signal(bool(0))
            mm_done = Signal(bool(0))
            #Xmem
            X_ADDR_W = int(np.ceil(np.log2(K*M)+1))
            x_we = Signal(bool(0))
            x_waddr = Signal(intbv(0)[X_ADDR_W:])
            x_din = Signal(intbv(0)[2*COMPLEX_DAT_W:])
            x_re = Signal(bool(0))
            x_raddr = Signal(intbv(0)[X_ADDR_W:])
            x_dout = Signal(intbv(0)[2*COMPLEX_DAT_W:])
            Xmem = dual_port_ram(clk, x_we, x_waddr, x_din, x_re, x_raddr, x_dout, X_ADDR_W, 2*COMPLEX_DAT_W)

            #Ymem
            Y_ADDR_W = int(np.ceil(np.log2(M*N)+1))
            y_we = Signal(bool(0))
            y_waddr = Signal(intbv(0)[X_ADDR_W:])
            y_din = Signal(intbv(0)[2*COMPLEX_DAT_W:])
            y_re = Signal(bool(0))
            y_raddr = Signal(intbv(0)[X_ADDR_W:])
            y_dout = Signal(intbv(0)[2*COMPLEX_DAT_W:])
            Ymem = dual_port_ram(clk, y_we, y_waddr, y_din, y_re, y_raddr, y_dout, Y_ADDR_W, 2*COMPLEX_DAT_W)

            #Zmem
            Z_ADDR_W = int(np.ceil(np.log2(K*N)+1))
            z_we = Signal(bool(0))
            z_waddr = Signal(intbv(0)[X_ADDR_W:])
            z_din = Signal(intbv(0)[2*COMPLEX_DAT_W:])
            z_re = Signal(bool(0))
            z_raddr = Signal(intbv(0)[X_ADDR_W:])
            z_dout = Signal(intbv(0)[2*COMPLEX_DAT_W:])
            Zmem = dual_port_ram(clk, x_we, x_waddr, x_din, x_re, x_raddr, x_dout, X_ADDR_W, 2*COMPLEX_DAT_W)

            #MatrixMult
            dut = complex_matrix_mult(clk,rst,mm_valid,mm_ready,mm_done,x_re,x_raddr,x_dout,y_re,y_raddr,y_dout,z_we,z_waddr,z_din,
                                X_ADDR_W,Y_ADDR_W,Z_ADDR_W,DAT_WIDTH = 32,K = 2,M = 100,N = 2,ACCU_WIDTH = 80)
            

            half_period = delay(10)

            #reference array:
            x_array = np.random.randint(MIN_INT,MAX_INT,K*M) + 1j*np.random.randint(MIN_INT,MAX_INT,K*M) 
            x_matrix = x_array.reshape(K,M)
            y_array = np.random.randint(MIN_INT,MAX_INT,M*N) + 1j*np.random.randint(MIN_INT,MAX_INT,M*N)
            y_matrix = y_array.reshape(M,N)
            z_matrix = x_matrix@y_matrix
            z_array = np.squeeze(z_matrix)

            #clock gen
            @always(half_period)
            def clock_gen():
                clk.next = not clk

            @instance 
            def stimulus():
                #write
                for i in range(200): #TODO edit
                    yield clk.posedge
                    #X data wirte
                    x_real = Signal(intbv(int(np.real(x_array[i])),min=MIN_INT,max=MAX_INT)[COMPLEX_DAT_W:].unsigned())
                    x_imag = Signal(intbv(int(np.imag(x_array[i])),min=MIN_INT,max=MAX_INT)[COMPLEX_DAT_W:].unsigned())
                    x_in = ConcatSignal(x_real,x_imag)
                    x_we.next = 1
                    x_din.next = x_in
                    x_waddr.next = Signal(intbv(i)[X_ADDR_W:])

                    #Ydata write
                    y_real = Signal(intbv(int(np.real(y_array[i])),min=MIN_INT,max=MAX_INT)[COMPLEX_DAT_W:].unsigned())
                    y_imag = Signal(intbv(int(np.imag(y_array[i])),min=MIN_INT,max=MAX_INT)[COMPLEX_DAT_W:].unsigned())
                    y_in = ConcatSignal(y_real,y_imag)
                    y_we.next = 1
                    y_din.next = y_in
                    y_waddr.next = Signal(intbv(i)[Y_ADDR_W:])

                yield clk.posedge
                mm_valid.next = 1
                x_we.next = 0
                y_we.next = 0
                yield clk.posedge


                while(mm_ready == 0):
                    yield clk.posedge
                mm_valid.next = 0

                while(mm_done == 0):
                    yield clk.posedge
                
                for i in range(K*N):
                    yield clk.posedge

                #read
                
                for i in range(K*M):
                    yield clk.posedge
                    z_re.next = 1
                    z_raddr.next = Signal(intbv(i)[Z_ADDR_W:])


                yield delay(100)
                raise StopSimulation()
            
            
            @instance 
            def monitor():
                #registers for monitoring
                #re_r = Signal(bool(0))
                #raddr_r = Signal(intbv(0)[addr_w:])

                valid_cnt = 0
                done_cnt = 0
                is_processing = 0
                x_re_r = Signal(bool(0))
                x_raddr_r = Signal(intbv(0)[X_ADDR_W:])
                z_re_r = Signal(bool(0))
                z_raddr_r = Signal(intbv(0)[Z_ADDR_W:])
                while(1):
                    yield clk.posedge

                    #check if ready comes
                    if (mm_valid == 1):
                        if (mm_ready == 1):
                            is_processing = 1
                            valid_cnt = 0
                        else:
                            valid_cnt += 1
                    if (valid_cnt == 10):
                        self.assertEqual(mm_ready,mm_valid)
                    #check if done comes
                    if (is_processing == 1):
                        if (mm_done == 1):
                            done_cnt = 0
                        else:
                            done_cnt += 1   
                    if (done_cnt == 2*max(K*M,M*N)+K*N):
                        self.assertEqual(mm_done,bool(1))

                    #check if correct data is read from x
                    x_re_r.next = x_re
                    x_raddr_r.next = x_raddr
                    if (x_re_r == Signal(bool(1))):

                        x_real_read_check = x_dout[2*COMPLEX_DAT_W:COMPLEX_DAT_W].signed()
                        x_imag_read_check = x_dout[COMPLEX_DAT_W:].signed()
                        self.assertEqual(x_real_read_check+1j*x_imag_read_check,x_array[x_raddr_r])

                    #check if correct data is read from z
                    z_re_r.next = z_re
                    z_raddr_r.next = z_raddr
                    if (z_re_r.next == Signal(bool(1))):
                        z_real_read_check = z_dout[2*COMPLEX_DAT_W:COMPLEX_DAT_W]
                        z_imag_read_check = z_dout[COMPLEX_DAT_W:]
                        self.assertEqual(z_real_read_check+1j*z_imag_read_check,z_array[z_raddr_r])



            return Xmem,Ymem,dut,clock_gen,stimulus,monitor

        self.runTests(test_mm1)


    def runTests(self, test):
        check = test()
        if (os.path.isfile("test_mm1.vcd")):
            os.remove("test_mm1.vcd")
        tb = traceSignals(check)
        tb.run_sim()
        print("End of sim")


if __name__ == '__main__':
    unittest.main(verbosity=2)