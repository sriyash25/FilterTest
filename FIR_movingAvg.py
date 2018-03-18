from myhdl import *

def MOVAVG(clk, reset, x,y):
    """ moving average filter.

    x -- input intbv signal
    y -- output intbv signal
  
    """
    
    ffd = [Signal(intbv(0, min=x.min, max=x.max)) for i in range(4)]
    y_full= intbv(0)[16:] 
    
    h0=intbv(1)
    h1=intbv(1)
    h2=intbv(1)
    h3=intbv(1)
    h4=intbv(1)

    @always(clk.posedge)
    def FIR():
        
        if not reset:

             ffd[1].next=ffd[0]
             ffd[2].next=ffd[1]
             ffd[3].next=ffd[2]
             ffd[0].next=x
  
             y_full= h0*x+h1*ffd[0]+h2*ffd[1]+h3*ffd[2]+h4*ffd[3]
             y.next=y_full>>2
        else:
            y.next=y

    return FIR


def testBench():
    
    clk = Signal(bool(1))
    reset= Signal(bool(0))
    x= Signal(intbv(0)[8:])
    y= Signal(intbv(0)[8:])

    mov=MOVAVG(clk, reset, x, y)
   
    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
         "input for test bench taken from text file test.txt"
        for line in open('test.txt'):
            x.next=int(line)
            yield delay(20)
        
        raise StopSimulation
        
    return mov, clkgen, stimulus

def main():
    tb = traceSignals(testBench)
    sim = Simulation(tb)
    sim.run()

if __name__ == '__main__':
    main()