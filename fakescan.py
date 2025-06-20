
import os
import time

#simulate  port scam with echo and logger
for  i in range(20,25):
	msg = f"simulated scan attempt on port {i}"
	print (msg)
	os.system(f'logger "{msg}"')
	time.sleep(1)
