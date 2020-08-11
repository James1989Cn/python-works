import re

s = """
static int BUS1_USART_Init(void *arg)
{
    UARTBase *pUART = (UARTBase *)arg;
    UartData    *pHMIdata = (UartData *)pUART->pData;

    if(pUART->config.recmode == UARTRec_ISR)
    {
        Driver_UART_SetISR(pUART->config.port, BUS1USART_ISR);
    }
    pUART->osport.sem = Kernel_OSMboxCreate(0);
    //pHMIdata->osport.que              = SnsrSrl_Q;
    pHMIdata->inbufferlen =              0;
    pHMIdata->outbufferlen = 0;
    /*串口的参数都配置完了再注册到MODBUS，串口的收发方式在这里被设置为modbus的
    ，如果需要自定义在后面再自行设置*/
    ModbusHandler.addRTUReg(pUART);//注册到Modbus
    /*软件都配置完了再初始化硬件*/
    Driver_UARTConfig(pUART->config);
    Driver_IO_Init(BUS1_RST_Port,BUS1_RST_Pin,IO_Mode_Out_PP,IO_Speed_50MHz);
    Driver_IO_ResetBits(BUS1_RST_Port,BUS1_RST_Pin);
    return 1;
}
"""

def codePreety(st,spaceoffset = 4):
	"""
	st 源代码
	spaceoffset 缩进宽度
	源代码美化目前功能包括：
	1. 调整缩进
	2. 去除一行中多余的空格
	3. ‘，’后面补充空格
	"""
	t = st.split('\n')
	ret = ""
	offsetCnt = 0
	for ch in t:
		ch = ch.strip()
		ch = re.sub(",",", ",ch)
		ch = re.sub(" +"," ",ch)
		if len(ch) > 0:
			if ch[0] == '{':
				for i in range(offsetCnt):
					ret += ' '
				ret += ch + '\n'				
				offsetCnt += spaceoffset
				continue
			if '}' in ch:
				offsetCnt -= spaceoffset
		
		for i in range(offsetCnt):
			ret += ' '
		ret += ch + '\n'
	return ret

if __name__ == "__main__": 
	print(codePreety(s,4))
