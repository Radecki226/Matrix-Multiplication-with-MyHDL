import unittest
import sys
sys.path.append('C:\\Users\\piotrek\\Desktop\\nauka\\7 semestr\\esl\\tutor\\project\\src')
from myhdl import *
from complex_mult import complex_mult
import numpy as np





IN_WIDTH = 16
OUT_WIDTH = 32
INT_MIN_IN = -32768
INT_MAX_IN = 32767
INT_MIN_OUT = -2147483648
INT_MAX_OUT = 2147483647
IN_LEN = 4
OUT_LEN = 2

#conversion
x = [Signal(intbv(0,min=INT_MIN_IN,max=INT_MAX_IN)) for j in range(IN_LEN)]
y = [Signal(intbv(0,min=INT_MIN_OUT,max=INT_MAX_OUT)) for j in range(OUT_LEN)]
complex_mult_i = complex_mult(*x,*y)
complex_mult_i.convert(hdl = 'vhdl')
print("vhdl file generated")

class ComplexMultTest(unittest.TestCase):
    
    def complex_mult_reference(self,x1_r,x1_i,x2_r,x2_i):
        a = x1_r + 1j*x1_i
        b = x2_r + 1j*x2_i
        c = a*b
        return [int(np.real(c)),int(np.imag(c))]

    def testRandomNumbers(self):
        """Check if multiplication is performed properly"""

        def test(x,y):


            for i in range(20):
                #generate random numbers
                inputs = [np.random.randint(INT_MIN_IN,INT_MAX_IN) for j in range(IN_LEN)]
                #feed them to inputs
                for j in range(IN_LEN):
                    x[j].next = Signal(modbv(inputs[j],min=INT_MIN_IN,max=INT_MAX_IN))          
                yield delay(10)
                #expected
                outputs = self.complex_mult_reference(*(inputs))
                y_exp = [Signal(modbv(outputs[j],min=INT_MIN_OUT,max=INT_MAX_OUT)) for j in range(OUT_LEN)]
                self.assertEqual(y,y_exp)

        self.runTests(test)


    def runTests(self, test):
        x = [Signal(modbv(0,min=INT_MIN_IN,max=INT_MAX_IN)) for j in range(IN_LEN)]
        y = [Signal(modbv(0,min=INT_MIN_OUT,max=INT_MAX_OUT)) for j in range(OUT_LEN)]
        dut = complex_mult(*x,*y)
        check = test(x, y)
        sim = Simulation(dut, check)
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main(verbosity=2)

