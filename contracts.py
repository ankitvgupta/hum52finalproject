import Queue
import threading
import numpy as np
import time

class Contract(object):
	def __init__(self, seller, buyer, date, price):
		self.seller = seller
		self.buyer = buyer
		self.date = date
		self.price = price




numpeople = 500
startprice = 1000

# Give everyone money, and no one stock
money = [np.random.randint(10000) for i in range(numpeople)]
stock = [0 for i in range(numpeople)]

# Add a few growers, who are in depth.
stock[-2] = 500
stock[-1] = 150
money[-2] = -500
money[-1] = -200


multiplier = 1.1
allcontracts = []

values = [startprice]
for iteration in range(100):

	lastprice = float(sum(values))/len(values)
	print lastprice
	values = []

	# For each user, if they have any stock, create a contract with someone.
	for user in range(numpeople):
		while stock[user] > 0:
			randomuser = np.random.randint(numpeople)
			if randomuser == user:
				continue
			value = np.random.normal(multiplier*lastprice)
			allcontracts.append(Contract(user, randomuser, iteration + np.random.randint(1, 50), value))
			stock[user] -= 1
	j = 0
	while j < len(allcontracts):
		contract = allcontracts[j]
		if contract.date == iteration:
			#stock[contract.seller] -= 1
			stock[contract.buyer] += 1
			money[contract.seller] += contract.price
			money[contract.buyer] -= contract.price
			del(allcontracts[j])
		else:
			j += 1

	for i in range(len(allcontracts)):
		contract = allcontracts[i]
		randomuser = np.random.randint(numpeople)
		if randomuser == contract.seller or randomuser == contract.buyer:
			continue
		value = np.random.normal(multiplier*lastprice)
		netval = value - contract.price
		if netval > 0:
			money[contract.buyer] += netval
			money[randomuser] -= netval
			contract.buyer = randomuser
			values.append(value)
		else:
			#pass
			if stock[randomuser] > 0:
				money[contract.seller] += netval
				money[randomuser] -= netval
				stock[contract.seller] += 1
				stock[randomuser] -= 1
				contract.seller = randomuser



# for contract in allcontracts:
# 	print contract.seller, contract.buyer, contract.price, contract.date
#value = [money[i] + startprice*stock[i] for i in range(numpeople)]

print("Num of remaining contracts", len(allcontracts))
print("Poorest person", min(money))
print("Richest person", max(money))


# Calculate the wealth amongst stockholders
total_stock_money = 0
total_unstocked_money = 0
for user in range(numpeople):
	if stock[user]  > 0:
		total_stock_money += money[user]
	else:
		total_unstocked_money += money[user]

num_stockholders =  sum(x > 0 for x in stock)
num_notstockholders = sum(x == 0 for x in stock)
print("Wealth of people holding stock", total_stock_money)
print("Wealth of people not holding stock", total_unstocked_money)
print("Number of people holding stock",num_stockholders)
print("Number of people not stock", num_notstockholders)
print("Average wealth of stockholders", total_stock_money/num_stockholders)
print("Average wealth of not stockholders", total_unstocked_money/num_notstockholders)
print("Total wealth", sum(money))

#print sum(money), max(money), min(money)

lastprice = 10.
multiplier = .75



# for roundi in range(100):

# 	offers = [np.random.normal(multiplier*lastprice, 5) for i in range(numpeople)]
# 	sellprices = []
# 	for i in range(numpeople):
# 		sellprice = np.random.normal(multiplier*lastprice)
# 		for j in range(numpeople):
# 			if sellprice < offers[j] and i != j:
# 				money[i] += offers[j]
# 				money[j] -= offers[j]
# 				stock[j] += 1
# 				stock[i] -= 1
# 				sellprices.append(offers[j])
# 				offers[j] = 0
# 	if len(sellprices) != 0:
# 		lastprice = float(sum(sellprices))/len(sellprices)
# 	#print lastprice

# #print sum(money), max(money), min(money)

# # for i in range(numthreads):
# # 	t = threading.Thread(target=worker, args=(i, startprice, sells, buys, arrlock ))
# # 	threads.append(t)
# # 	t.start()
# # 	#time.sleep(.001)
# # for t in threads:
# # 	t.join()
# # print -sells.get()
# # print stock
