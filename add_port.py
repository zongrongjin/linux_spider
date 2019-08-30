import subprocess
import sys

port_list = sys.argv[1:]

for port in port_list:
	print(port)
	if '-' not in port:
		subprocess.getstatusoutput('firewall-cmd --zone=public --add-port=%s/tcp --permanent' % port)
	else:
		lines = port.split('-')
		start = lines[0]
		end = lines[1]
		for i in range(int(start), int(end)+1):
			subprocess.getstatusoutput('firewall-cmd --zone=public --add-port=%s/tcp --permanent' % str(i))

subprocess.getstatusoutput('firewall-cmd --reload')
