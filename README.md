# Matrix multiplication with MyHDL

## 1. Goal
Goal of this project is to develop algorithm for fast complex matrix multiplication. It is assumed that matrices are stored in dedicated memory blocks with one read and one write port. Thus writing and reading can be performed only sequentially. Complex number is represented as follows: real part on MSB and imaginary part on LSB.

## 2. Algorithm description
It is assumed that we multiply matrices KxM- X and MxN- Y. Algorithm is as follows:

<ol>
  <li value="1">Wait for input data to be valid</li>
  <li>Fetch m-th column of X and m-th row of Y</li>
  <li>Do multiplication of vectors with KxN MAC blocks</li>
  <li>Repeat points 2 and 3 through entire matrix</li>
  <li>Store obtained matrix in memory</li>
  <li>Set ready</li>
</ol>

Time of execution will be [(max(K,N)+1)*M + K*N ] ticks + a few ticks for control\

![Very simple drawing][drawing.jpg]

## 3. Matrix Multiplier

### Interface list

![interface list][interfacea.jpg]

### Functional description

1. MAC blocks are equipped with 40bits accumulators, this allows circuit to multiply matrices with depth 255.
2. Data is 16-bit signed integer
3. Control is realized with AXI(vld,rdy).
4. Design is controlled with main FSM and one secondary FSM(calc), description below.
5. Main FSM
- `IDLE`: If data valid go to calc
- `CALC`: Activate secondary FSM, when calculations finished go to `WRITE_DATA`
- `WRITE_DATA`: Store output data in memory and go to `DONE`
- `DONE`: Display valid, when ready go to IDLE
6. Calc FSM
- `IDLE`: When FSM signalizes that data is valid, go to `READ`
- `READ`: Fetch m-th column/row and go to `MULT`
- `MULT`: Multiply data, if end of matrix reached go to done, otherwise go back to `READ`
- `DONE`: Display done flag and go to `IDLE`




