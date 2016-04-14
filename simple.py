import Queue
import threading
import numpy as np
import time



def worker(num, startprice, sellqueue, buyqueue, arrlock):
	money = np.random.randint(100000)
	#stock = 0
	price = startprice

	currentstock = stock[num]

	arrlock.acquire()
	stock[num] = money
	arrlock.release()



	sellqueue.put_nowait((-money, num))


threads = []
numpeople = 500
sells = Queue.PriorityQueue()
buys = Queue.PriorityQueue()
startprice = 1
arrlock = threading.Lock()
money = [np.random.randint(10000) for i in range(numpeople)]
stock = [np.random.randint(50) for i in range(numpeople)]

print sum(money), max(money), min(money)

lastprice = 10.
multiplier = .5
for roundi in range(100):
	offers = [np.random.normal(multiplier*lastprice, 5) for i in range(numpeople)]
	sellprices = []
	for i in range(numpeople):
		sellprice = np.random.normal(multiplier*lastprice)
		for j in range(numpeople):
			if sellprice < offers[j] and i != j:
				money[i] += offers[j]
				money[j] -= offers[j]
				stock[j] += 1
				stock[i] -= 1
				sellprices.append(offers[j])
				offers[j] = 0
	if len(sellprices) != 0:
		lastprice = float(sum(sellprices))/len(sellprices)
	print lastprice

print sum(money), max(money), min(money)

# for i in range(numthreads):
# 	t = threading.Thread(target=worker, args=(i, startprice, sells, buys, arrlock ))
# 	threads.append(t)
# 	t.start()
# 	#time.sleep(.001)
# for t in threads:
# 	t.join()
# print -sells.get()
# print stock