# uartTrans

自定义串口传输数据格式, 可自定义指令及回调函数, 采用crc16校验

## 快速开始

* 导入模块

```python
import uartTrans # import 
```

* 创建 uartTrans

```python
fm.register(22, fm.fpioa.UART1_TX, force=True)
fm.register(21, fm.fpioa.UART1_RX, force=True)
uart1 = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
uart_t = uartTrans(uart1)
```

* 注册新的指令回调

```python
def cus_cmd(uart, num):
    print("execute cus cmd {}".format(num))
    uart.write("execute cus cmd {}".format(num))

uart_t.reg_cmd("cus", cus_cmd, uart1, 1) # 注册当接受到 'cus' 时的回调函数为 cus_cmd， 参数为 1
```

* 接收指令或数据

```python
udatas = self.read()
```

* 发送指令或数据

```python
uart_ta.write('cus', True) # send 'cus' cmd
uart_ta.write('hello') # send 'hello'data
```

* 执行接收的指令, 打印接收到的数据

```python
for udata in udatas:
    is_cmd  = udata[0]
    if udata[0]:
        self.exec_cmd(udata[1]) # execute cmd
    else:
        print("recv data:", udata[1])
```

## API

* 注册指令

```python
reg_cmd(self, cmd, fun, *args):
```

参数: `cmd` 指令名, `fun` 指令回调函数, `*args` 回调函数参数

* 注销指令

```python
unreg_cmd(self, cmd, fun):
```

参数: `cmd` 指令名

* 发送指令或数据

```python
write(self, s, is_cmd)
```

参数: `s` 要发送的数据, `is_cmd` 是否以指令的形式发送

* 接受指令或数据

```python
read(self)
```

返回接收到的数据或指令列表, 格式为二维列表: `[[is_cmd, data]]` is_cmd: True 指令, False 数据, data 数据或指令本身
