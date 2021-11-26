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
    

    def WriteAndReadTest(self):
        """Test 1: Fill entire array with numbers and read it"""


        @block
        def test_mm1():
            K = 2
            M = 100
            N = 2
            COMPLEX_DAT_W = 16
            MAX_INT = 32767
            MIN_INT = -32768
            #clk
            clk = Signal(bool(0))
            #Xmem
            X_ADDR_W = np.ceil(np.log2(K*M)+1)
            x_we = Signal(bool(0))
            x_waddr = Signal(intbv(0)[X_ADDR_W:])
            x_din = Signal(intbv(0,min=MIN_INT,max=MAX_INT)[2*COMPLEX_DAT_W])
            x_re = Signal(bool(0))
            x_raddr = Signal(intbv(0)[X_ADDR_W:])
            x_dout = Signal(intbv(0,min=MIN_INT,max=MAX_INT)[2*COMPLEX_DAT_W])
            Xmem = dual_port_ram(clk, x_we, x_waddr, x_din, x_re, x_raddr, x_dout, X_ADDR_W, 2*COMPLEX_DAT_W)

            #Ymem
            Y_ADDR_W = np.ceil(np.log2(M*N)+1)
            y_we = Signal(bool(0))
            y_waddr = Signal(intbv(0)[X_ADDR_W:])
            y_din = Signal(intbv(0,min=MIN_INT,max=MAX_INT)[2*COMPLEX_DAT_W])
            y_re = Signal(bool(0))
            y_raddr = Signal(intbv(0)[X_ADDR_W:])
            y_dout = Signal(intbv(0,min=MIN_INT,max=MAX_INT)[2*COMPLEX_DAT_W])
            Ymem = dual_port_ram(clk, y_we, y_waddr, y_din, y_re, y_raddr, y_dout, Y_ADDR_W, 2*COMPLEX_DAT_W)

            #Zmem
            Z_ADDR_W = np.ceil(np.log2(K*N)+1)
            z_we = Signal(bool(0))
            z_waddr = Signal(intbv(0)[X_ADDR_W:])
            z_din = Signal(intbv(0,min=MIN_INT,max=MAX_INT)[2*COMPLEX_DAT_W])
            z_re = Signal(bool(0))
            z_raddr = Signal(intbv(0)[X_ADDR_W:])
            z_dout = Signal(intbv(0,min=MIN_INT,max=MAX_INT)[2*COMPLEX_DAT_W])
            Zmem = dual_port_ram(clk, x_we, x_waddr, x_din, x_re, x_raddr, x_dout, X_ADDR_W, 2*COMPLEX_DAT_W)

            #MatrixMult


            half_period = delay(10)

            #reference array:
            x_array = np.array([np.random.randint(MIN_INT,MAX_INT) + 1j*np.random.randint(MIN_INT,MAX_INT) for i in range(K*M)])
            x_matrix = x_array.reshape(K,M)
            y_array = np.array([np.random.randint(MIN_INT,MAX_INT) + 1j*np.random.randint(MIN_INT,MAX_INT) for i in range(M*N)])
            y_array = y_array.reshape(M,N)

            #clock gen
            @always(half_period)
            def clock_gen():
                clk.next = not clk

            @instance 
            def stimulus():
                #write
                for i in range(K*M):
                    yield clk.posedge
                    x_re = Signal(intbv(np.real(x_array[i]),min=MIN_INT,max=MAX_INT)[COMPLEX_DAT_W].unsigned())
                    x_im = Signal(intbv(np.real(x_array[i]),min=MIN_INT,max=MAX_INT)[COMPLEX_DAT_W].unsigned())
                    x_we.next = 1
                    x_din.next = ConcatSignal(x_re,x_im)
                    waddr.next = Signal(intbv(i)[addr_w:])
                    
                #read
                for i in range(ram_size):
                    yield clk.posedge
                    we.next = 0
                    re.next = 1
                    raddr.next = Signal(intbv(i)[addr_w:])

                yield delay(100)
                raise StopSimulation()
            
            
            @instance 
            def monitor():
                #registers for monitoring
                re_r = Signal(bool(0))
                raddr_r = Signal(intbv(0)[addr_w:])
                while(1):
                    yield clk.posedge
                    re_r.next = re
                    raddr_r.next = raddr
                    if (re_r == Signal(bool(1))):
                        self.assertEqual(dout,intbv(arr[raddr_r]))

            return dut,clock_gen,stimulus,monitor

        self.runTests(test_mm1)


    def runTests(self, test):
        check = test()
        if (os.path.isfile("test_mm1.vcd")):
            os.remove("test_mm1.vcd")
        tb = traceSignals(check)
        tb.run_sim()


if __name__ == '__main__':
    unittest.main(verbosity=2)