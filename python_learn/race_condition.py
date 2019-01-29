import time, threading

balance = 0

lock = threading.Lock()



def change_value(n):
	global balance
	balance = balance + n
	balance = balance - n
def run_thread(n):
	for i in range(1000000):
		lock.acquire()
		try:
			change_value(n)
		finally:
			lock.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(4,))

t1.start()
t2.start()
t1.join()
t2.join()
print(balance)