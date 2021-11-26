import unittest
import sys
sys.path.append('C:\\Users\\piotrek\\Desktop\\nauka\\7 semestr\\esl\\tutor\\project\\myhdl_first_project\\src')
from myhdl import *
from dual_port_ram import dual_port_ram
import os
import numpy as np
np.random.seed(2021)


class DualPortTest(unittest.TestCase):
    

    def testFullWriteFullRead(self):
        """Test 1: Fill entire array with numbers and read it"""


        @block
        def test1(clk,we,waddr,din,re,raddr,dout,addr_w,dat_w):
            dut = dual_port_ram(clk, we, waddr, din, re, raddr, dout, addr_w, dat_w)
            dut.convert(hdl='vhdl')
            ram_size = 2**addr_w
            dat_max = 2**dat_w-1
            half_period = delay(10)

            #reference array:
            arr = [np.random.randint(0,dat_max) for i in range(ram_size)]
            @always(half_period)
            def clock_gen():
                clk.next = not clk

            @instance 
            def stimulus():
                #write
                for i in range(ram_size):
                    yield clk.posedge
                    we.next = 1
                    din.next = Signal(intbv(arr[i])[dat_w:])
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

        self.runTests(test1)


    def runTests(self, test):
        addr_w = 4
        dat_w = 16
        clk,we,re = [Signal(bool(0)) for i in range(3)]
        waddr,raddr = [Signal(intbv(0)[addr_w:]) for i in range(2)]
        din,dout = [Signal(intbv(0)[dat_w:]) for i in range(2)]
        check = test(clk,we,waddr,din,re,raddr,dout,addr_w,dat_w)
        if (os.path.isfile("test1.vcd")):
            os.remove("test1.vcd")
        tb = traceSignals(check)
        tb.run_sim()


if __name__ == '__main__':
    unittest.main(verbosity=2)