#!/usr/bin/python
# coding=UTF-8
"""
一个简易的串口助手
"""
import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from crc16 import crc16
import re
import time
import chardet
import time
import datetime

linesPerPack = 4

import binascii

def hexStr_to_str(hex_str):
	hex = hex_str.encode('utf-8')
	str_bin = binascii.unhexlify(hex)    
	return str_bin.decode('utf-8')

def hexStr_to_list(s):
	ll = []
	idx = 0
	while idx < len(s)-1:
		lu = int(s[idx:idx+2],16)
		ll.append(lu)
		idx += 2
	return ll
	
def str_to_hexlist(s,idx):
	ll = [0x01,0x61]
	ll.append((idx>>8)&0xFF)
	ll.append(idx&0xff)
	idx &= 0xFFFF
	idx = 0xFFFF - idx
	ll.append((idx>>8)&0xFF)
	ll.append(idx&0xff)
	for ch in s:
		ll.append(ord(ch))
	return ll
	
class My_UI():
	def __init__(self):
		self.haveComOpen = False
		self.__root = Tk()
		self.__root.title("HEX文件发送")
		self.__root.option_add('*tearOff', FALSE)
		menubar = Menu(self.__root)
		self.__root['menu'] = menubar
		menu_file = Menu(menubar)
		menubar.add_cascade(menu=menu_file, label='File')
		menu_file.add_command(label='Save...', command=self.SaveFile, accelerator='Ctr+s')
		menu_file.add_command(label='Quit', command=lambda : self.__root.destroy(), accelerator='Ctr+q')

		#创建与布局各个控件
		mainframe = ttk.Frame(self.__root, padding="3")		
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

		self.tt = serial.tools.list_ports.comports()
		listcom=[]
		self.devices=[]
		for t in self.tt:
			listcom.append(t.device+' '+t.description)
			self.devices.append(t.device)
		cnames = StringVar()
		self.Combobox = ttk.Combobox(mainframe, textvariable=cnames, values=listcom)
		self.Combobox.grid(column=0, row=0, sticky=(W, E))
		
		ttk.Button(mainframe, text="打开串口", command=self.serial_Open).grid(column=0, row=1, sticky=(W,E))
		
		bottomframe = ttk.Frame(mainframe, padding="3")		
		bottomframe.grid(column=2, row=5, sticky=(N, W, E, S))
		ttk.Button(bottomframe, text="清除窗口", command=self.clear_RxWin).grid(column=0, row=0, sticky=(W))
		self.StringTXRX = StringVar()
		self.StringTXRX.set(r'发送/接收：0/0')
		self.TxCount = 0
		self.RxCount = 0
		ttk.Label(mainframe, textvariable=self.StringTXRX).grid(column=2, row=5, sticky=(E))
		self.HexRecvFlag = StringVar()
		self.HexRecvFlag.set(0)
		cb = ttk.Checkbutton(bottomframe, text="Hex显示", variable=self.HexRecvFlag, onvalue=1, offvalue=0)
		cb.grid(column=5, row=0, sticky=(W))
		self.AddCrcFlag = StringVar()
		self.AddCrcFlag.set(0)
		cb = ttk.Checkbutton(bottomframe, text="附加CRC", variable=self.AddCrcFlag, onvalue=1, offvalue=0)
		cb.grid(column=6, row=0, sticky=(W))
		self.AutoResendFlag = StringVar()
		ttk.Checkbutton(bottomframe, text="定时发送", variable=self.AutoResendFlag, onvalue=1, offvalue=0).grid(column=2, row=0, sticky=(W))
		self.AutoResendFlag.set(0)
		self.__AutoResendVal = Text(bottomframe, width=4, height=1)
		self.__AutoResendVal.grid(column=3, row=0, sticky=(W))
		self.__AutoResendVal.delete(1.0,'end')
		self.__AutoResendVal.insert(1.0,"1000")
		self.timeStampFlag = StringVar()
		ttk.Checkbutton(bottomframe, text="时间戳", variable=self.timeStampFlag, onvalue=1, offvalue=0).grid(column=4, row=0, sticky=(W))
		self.timeStampFlag.set(0)
		
		self.__result = Text(mainframe, width=80, height=10)
		self.__result.grid(column=2, row=0, rowspan= 4, sticky=(W,E,N,S))
		__resultProgBar = ttk.Scrollbar( mainframe, orient=VERTICAL, command=self.__result.yview)
		self.__result.configure(yscrollcommand=__resultProgBar.set)
		__resultProgBar.grid(column=3, row=0, rowspan= 4, sticky=(W,E,N,S))
		
		self.__txFrame = Text(mainframe, width=60, height=3)
		self.__txFrame.grid(column=2, row=7, rowspan= 4, sticky=(W,E,N,S))
		ttk.Button(mainframe, text="手动发送", command=self.manual_send).grid(column=0, row=7, sticky=(W,E))

		for child in mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)
		#配置画面拉伸
		self.__root.columnconfigure(0, weight=1)
		self.__root.rowconfigure(0, weight=1)
		mainframe.columnconfigure(0, weight=0)
		mainframe.columnconfigure(1, weight=0)
		mainframe.columnconfigure(2, weight=1)
		mainframe.columnconfigure(3, weight=1)
		mainframe.rowconfigure(0, weight=0)
		mainframe.rowconfigure(1, weight=1)
		mainframe.rowconfigure(2, weight=1)
		mainframe.rowconfigure(3, weight=1)
		mainframe.rowconfigure(4, weight=0)		
		
		# ~ self.Combobox.focus()
		self.__root.bind_all("<Control-q>", lambda event: self.__root.destroy())
		
		self.idx = 0
		self.packidx = 0
		self.haveFileOpened = 0
		self.canceled = 0
		self.count = 0
		self.lastCount = 0
		self.transStep = 0
		self.lastTransBool = False
		self.sendingfileBool = False
		self.updateFailBool = False
		
		sw = self.__root.winfo_screenwidth()
		#得到屏幕宽度
		# ~ sh = self.__root.winfo_screenheight()
		# ~ ww = 800
		# ~ wh = 400
		# ~ x = (sw-ww) / 2
		# ~ y = (sh-wh) / 2
		# ~ self.__root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
			
	def clear_RxWin(self):		
		self.__result.delete(1.0,'end')
		self.TxCount = 0
		self.RxCount = 0
		self.StringTXRX.set(f'发送/接收：{self.TxCount}/{self.RxCount}')
		
	def serial_Tx(self,s):
		self.myserial.write(s)
		self.TxCount += len(s)
		self.StringTXRX.set(f'发送/接收：{self.TxCount}/{self.RxCount}')
	
	def manual_send(self):
		if self.haveComOpen == False:
			return
		s = self.__txFrame.get(1.0,'end')
		s = s.strip()
		s = re.sub(' ','',s)
		ch = int(self.HexRecvFlag.get())
		if ch == 1:#Hex显示
			hexs = hexStr_to_list(s)			
			ch = int(self.AddCrcFlag.get())
			if ch == 1:#CRC
				mycrc = crc16(hexs,1)
				hexs.append(mycrc>>8)
				hexs.append(mycrc&0xff)
			self.serial_Tx(hexs)
			ch = int(self.timeStampFlag.get())
			if ch == 1:#时间戳
				curr = datetime.datetime.now()
				micors = curr.microsecond/1000
				s1 = '['+datetime.datetime.strftime(curr,'%H:%M:%S.')+'%03d' % micors +']发hex '
				s = ''
				for ch in hexs:
					s += '%02X' % ch + ' '
				self.__result.insert('end',s1+s+'\n')
		else:
			self.serial_Tx(s.encode("ascii"))
			ch = int(self.timeStampFlag.get())
			if ch == 1:#时间戳
				curr = datetime.datetime.now()
				micors = curr.microsecond/1000
				s1 = '['+datetime.datetime.strftime(curr,'%H:%M:%S.')+'%03d' % micors +']发字符 '
				self.__result.insert('end',s1+s+'\n')
		
		self.__result.yview_moveto(1.0)
		ch = int(self.AutoResendFlag.get())
		if ch == 1:#自动重发
			s = self.__AutoResendVal.get(1.0,'end')
			try:
				val = int(s)
				self.__root.after(val, self.manual_send)
			except:
				self.__root.after(1000, self.manual_send)
		else:
			return
		
	def select_com(self,*args):
		self.idxs = self.Combobox.current()
		self.selected = True
		
	def run_UI(self):
		self.Combobox.current(0)
		self.__root.mainloop()
		
	def SaveFile(self,*args):
		pass
	
	def serial_Open(self):	
		self.select_com()
		try:
			self.myserial = serial.Serial(self.devices[self.idxs], 115200)# 打开COM并设置波特率为115200
		except:
			self.__result.delete(1.0,'end')
			self.__result.insert(1.0,'无法打开串口')
			return
		self.__result.delete(1.0,'end')
		self.__result.insert(1.0,self.myserial)
		self.haveComOpen = True		
		# ~ self.serial_recv()
		self.serial_blockedrecv()
						
	def serial_blockedrecv(self):
		if self.haveComOpen == False:
			return
		
		count = self.myserial.inWaiting()
		if count > 0:
			if self.lastCount != count:#接收中，有数据进来
				self.lastCount = count
				self.__root.after(10, self.serial_blockedrecv)
				return	
			data = self.myserial.read(count)
			self.RxCount += count
			self.StringTXRX.set(f'发送/接收：{self.TxCount}/{self.RxCount}')
			ch = int(self.HexRecvFlag.get())
			if ch == 1:#Hex显示
				s = ''.join(['%02X ' % b for b in data])
				ch = int(self.timeStampFlag.get())
				if ch == 1:#时间戳
					curr = datetime.datetime.now()
					micors = curr.microsecond/1000
					s1 = '['+datetime.datetime.strftime(curr,'%H:%M:%S.')+'%03d' % micors +']收hex '
					data = s1+s
				else:
					data = s
			else:					
				try:
					data = data.decode('gb2312')
					ch = int(self.timeStampFlag.get())
					if ch == 1:#时间戳
						curr = datetime.datetime.now()
						micors = curr.microsecond/1000
						s1 = '['+datetime.datetime.strftime(curr,'%H:%M:%S.')+'%03d' % micors +']收字符 '
						data = s1+data
				except:
					data = ''
			startTime = time.time()
			if self.sendingfileBool == False:
				self.__result.insert('end',data+'\n')
				self.__result.yview_moveto(1.0)
			self.lastCount = self.myserial.inWaiting()
			
		self.__root.after(10, self.serial_blockedrecv)


if __name__ == '__main__':
	myui = My_UI()
	myui.run_UI()
