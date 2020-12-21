from fpioa_manager import fm
import time
from machine import UART
import ustruct
from uart_protocol import uartTrans

def cus_cmd(uart, num):
    print("execute cus cmd {}".format(num))
    uart.write("execute cus cmd {}".format(num))
    
# read cmd from uart and execute cmd fun
if __name__ == "__main__":
    fm.register(22, fm.fpioa.UART1_TX, force=True)
    fm.register(21, fm.fpioa.UART1_RX, force=True)

    fm.register(24, fm.fpioa.UART2_TX, force=True)
    fm.register(23, fm.fpioa.UART2_RX, force=True)

    uart1 = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
    uart2 = UART(UART.UART2, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)

    uart_TA = uartTrans(uart1)
    uart_TB = uartTrans(uart2)

    # pack hello and cus cmd, then send 
    print("send the packed 'hello' 'cus' cmd to uart1")
    uart_TA.write('cus', 1)
    uart_TA.write('hello')
    
    # unregister cus cmd
    # uart_A.unreg_cmd("cus")
    
    # register cus cmd
    uart_TA.reg_cmd("cus", cus_cmd, uart1, 1) 
    uart_TB.reg_cmd("cus", cus_cmd, uart2, 2) 

    # start to parse the receive cmd
    while True:
        uart_TA.parse(uart_TA.read())
        uart_TB.parse(uart_TB.read())
        time.sleep_ms(100)

'''output
>>> send the packed 'hello' 'cus' cmd to uart1
recv cmd: b'cus'
execute cus cmd 1
recv data: b'hello'
recv cmd: b'cus'
'''

'''packed data: b'hello'  cmd: b'cus'
DD FF 00 00 05 68 65 6C 6C 6F F6 34 AA FF DD FF 01 00 03 63 75 73 E6 AB AA FF 
'''