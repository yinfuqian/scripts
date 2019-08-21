#!/usr/bin/python 
#coding=utf-8
#User Larryd 
#time 2019/06/27
#获取本机IP
import socket
def get_host_ip():	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()
	print  ip
get_host_ip()
