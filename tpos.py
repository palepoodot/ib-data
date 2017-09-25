# IbPy Wrapped Code

#! /usr/bin/python

#import dependencies
from ib.opt import Connection #for IbPy
from ib.ext.Contract import Contract #for IbPy
import time #for measuring current time and feeding it to IB, deliberate delays so IB can send data
import datetime #for processing IB dateformat
from prettytable import PrettyTable, from_csv #for publishing data

#global variables
ticks = [] #stores IB data raw
dates = [] #columns of our output
prices = [] #rows of our output
table = [] #final output table
today = datetime.datetime.today() #current date and time reference
now = datetime.datetime.now() #current date and time reference
ts = now.strftime('%Y%m%d') + ' ' + now.strftime('%X') + ' PST' #convert current time into IB friendly format
tickername = input("Enter the ticker (SPX, AAPL, NQ, Default is SPX): ") or 'SPX' #SPX, SPY, get the ticker
tickertype = input("Enter the type (STK, IND, FUT, Default is IND): ") or 'IND' #IND, STK, get the index
tickerexch = input("Enter the exchange (SMART, CBOE, CME, Default is CBOE): ") or 'CBOE' #CBOE, SMART, get the exchange for routing
tickerprimaryexch = '' #''
tickercurr = 'USD' #USD

interval = input("Enter the interval (1 min, 2 mins, 5 mins, Default is 1 min): ") or '1 min' #'1 min' get the interval for rounding
lookback = input("Enter the lookback period (1 D, 9 D, 24 D, Default is 2 D): ") or '2 D' #'24 D' get the lookback period
precision = int(input("Enter the price precision in decimal places (0, 1, 2, Default is 1): ") or 1) #'24 D' get the lookback period

#define a dictionary of codes for time periods for market profile
coderef = {
			'06:30:00' : 'A',
			'06:31:00' : 'A',
			'06:32:00' : 'A',
			'06:33:00' : 'A',
			'06:34:00' : 'A',
			'06:35:00' : 'A',
			'06:36:00' : 'A',
			'06:37:00' : 'A',
			'06:38:00' : 'A',
			'06:39:00' : 'A',
			'06:40:00' : 'A',
			'06:41:00' : 'A',
			'06:42:00' : 'A',
			'06:43:00' : 'A',
			'06:44:00' : 'A',
			'06:45:00' : 'A',
			'06:46:00' : 'A',
			'06:47:00' : 'A',
			'06:48:00' : 'A',
			'06:49:00' : 'A',
			'06:50:00' : 'A',
			'06:51:00' : 'A',
			'06:52:00' : 'A',
			'06:53:00' : 'A',
			'06:54:00' : 'A',
			'06:55:00' : 'A',
			'06:56:00' : 'A',
			'06:57:00' : 'A',
			'06:58:00' : 'A',
			'06:59:00' : 'A',
			'07:00:00' : 'B',
			'07:01:00' : 'B',
			'07:02:00' : 'B',
			'07:03:00' : 'B',
			'07:04:00' : 'B',
			'07:05:00' : 'B',
			'07:06:00' : 'B',
			'07:07:00' : 'B',
			'07:08:00' : 'B',
			'07:09:00' : 'B',
			'07:10:00' : 'B',
			'07:11:00' : 'B',
			'07:12:00' : 'B',
			'07:13:00' : 'B',
			'07:14:00' : 'B',
			'07:15:00' : 'B',
			'07:16:00' : 'B',
			'07:17:00' : 'B',
			'07:18:00' : 'B',
			'07:19:00' : 'B',
			'07:20:00' : 'B',
			'07:21:00' : 'B',
			'07:22:00' : 'B',
			'07:23:00' : 'B',
			'07:24:00' : 'B',
			'07:25:00' : 'B',
			'07:26:00' : 'B',
			'07:27:00' : 'B',
			'07:28:00' : 'B',
			'07:29:00' : 'B',
			'07:30:00' : 'C',
			'07:31:00' : 'C',
			'07:32:00' : 'C',
			'07:33:00' : 'C',
			'07:34:00' : 'C',
			'07:35:00' : 'C',
			'07:36:00' : 'C',
			'07:37:00' : 'C',
			'07:38:00' : 'C',
			'07:39:00' : 'C',
			'07:40:00' : 'C',
			'07:41:00' : 'C',
			'07:42:00' : 'C',
			'07:43:00' : 'C',
			'07:44:00' : 'C',
			'07:45:00' : 'C',
			'07:46:00' : 'C',
			'07:47:00' : 'C',
			'07:48:00' : 'C',
			'07:49:00' : 'C',
			'07:50:00' : 'C',
			'07:51:00' : 'C',
			'07:52:00' : 'C',
			'07:53:00' : 'C',
			'07:54:00' : 'C',
			'07:55:00' : 'C',
			'07:56:00' : 'C',
			'07:57:00' : 'C',
			'07:58:00' : 'C',
			'07:59:00' : 'C',
			'08:00:00' : 'D',
			'08:01:00' : 'D',
			'08:02:00' : 'D',
			'08:03:00' : 'D',
			'08:04:00' : 'D',
			'08:05:00' : 'D',
			'08:06:00' : 'D',
			'08:07:00' : 'D',
			'08:08:00' : 'D',
			'08:09:00' : 'D',
			'08:10:00' : 'D',
			'08:11:00' : 'D',
			'08:12:00' : 'D',
			'08:13:00' : 'D',
			'08:14:00' : 'D',
			'08:15:00' : 'D',
			'08:16:00' : 'D',
			'08:17:00' : 'D',
			'08:18:00' : 'D',
			'08:19:00' : 'D',
			'08:20:00' : 'D',
			'08:21:00' : 'D',
			'08:22:00' : 'D',
			'08:23:00' : 'D',
			'08:24:00' : 'D',
			'08:25:00' : 'D',
			'08:26:00' : 'D',
			'08:27:00' : 'D',
			'08:28:00' : 'D',
			'08:29:00' : 'D',
			'08:30:00' : 'E',
			'08:31:00' : 'E',
			'08:32:00' : 'E',
			'08:33:00' : 'E',
			'08:34:00' : 'E',
			'08:35:00' : 'E',
			'08:36:00' : 'E',
			'08:37:00' : 'E',
			'08:38:00' : 'E',
			'08:39:00' : 'E',
			'08:40:00' : 'E',
			'08:41:00' : 'E',
			'08:42:00' : 'E',
			'08:43:00' : 'E',
			'08:44:00' : 'E',
			'08:45:00' : 'E',
			'08:46:00' : 'E',
			'08:47:00' : 'E',
			'08:48:00' : 'E',
			'08:49:00' : 'E',
			'08:50:00' : 'E',
			'08:51:00' : 'E',
			'08:52:00' : 'E',
			'08:53:00' : 'E',
			'08:54:00' : 'E',
			'08:55:00' : 'E',
			'08:56:00' : 'E',
			'08:57:00' : 'E',
			'08:58:00' : 'E',
			'08:59:00' : 'E',
			'09:00:00' : 'F',
			'09:01:00' : 'F',
			'09:02:00' : 'F',
			'09:03:00' : 'F',
			'09:04:00' : 'F',
			'09:05:00' : 'F',
			'09:06:00' : 'F',
			'09:07:00' : 'F',
			'09:08:00' : 'F',
			'09:09:00' : 'F',
			'09:10:00' : 'F',
			'09:11:00' : 'F',
			'09:12:00' : 'F',
			'09:13:00' : 'F',
			'09:14:00' : 'F',
			'09:15:00' : 'F',
			'09:16:00' : 'F',
			'09:17:00' : 'F',
			'09:18:00' : 'F',
			'09:19:00' : 'F',
			'09:20:00' : 'F',
			'09:21:00' : 'F',
			'09:22:00' : 'F',
			'09:23:00' : 'F',
			'09:24:00' : 'F',
			'09:25:00' : 'F',
			'09:26:00' : 'F',
			'09:27:00' : 'F',
			'09:28:00' : 'F',
			'09:29:00' : 'F',
			'09:30:00' : 'G',
			'09:31:00' : 'G',
			'09:32:00' : 'G',
			'09:33:00' : 'G',
			'09:34:00' : 'G',
			'09:35:00' : 'G',
			'09:36:00' : 'G',
			'09:37:00' : 'G',
			'09:38:00' : 'G',
			'09:39:00' : 'G',
			'09:40:00' : 'G',
			'09:41:00' : 'G',
			'09:42:00' : 'G',
			'09:43:00' : 'G',
			'09:44:00' : 'G',
			'09:45:00' : 'G',
			'09:46:00' : 'G',
			'09:47:00' : 'G',
			'09:48:00' : 'G',
			'09:49:00' : 'G',
			'09:50:00' : 'G',
			'09:51:00' : 'G',
			'09:52:00' : 'G',
			'09:53:00' : 'G',
			'09:54:00' : 'G',
			'09:55:00' : 'G',
			'09:56:00' : 'G',
			'09:57:00' : 'G',
			'09:58:00' : 'G',
			'09:59:00' : 'G',
			'10:00:00' : 'H',
			'10:01:00' : 'H',
			'10:02:00' : 'H',
			'10:03:00' : 'H',
			'10:04:00' : 'H',
			'10:05:00' : 'H',
			'10:06:00' : 'H',
			'10:07:00' : 'H',
			'10:08:00' : 'H',
			'10:09:00' : 'H',
			'10:10:00' : 'H',
			'10:11:00' : 'H',
			'10:12:00' : 'H',
			'10:13:00' : 'H',
			'10:14:00' : 'H',
			'10:15:00' : 'H',
			'10:16:00' : 'H',
			'10:17:00' : 'H',
			'10:18:00' : 'H',
			'10:19:00' : 'H',
			'10:20:00' : 'H',
			'10:21:00' : 'H',
			'10:22:00' : 'H',
			'10:23:00' : 'H',
			'10:24:00' : 'H',
			'10:25:00' : 'H',
			'10:26:00' : 'H',
			'10:27:00' : 'H',
			'10:28:00' : 'H',
			'10:29:00' : 'H',
			'10:30:00' : 'I',
			'10:31:00' : 'I',
			'10:32:00' : 'I',
			'10:33:00' : 'I',
			'10:34:00' : 'I',
			'10:35:00' : 'I',
			'10:36:00' : 'I',
			'10:37:00' : 'I',
			'10:38:00' : 'I',
			'10:39:00' : 'I',
			'10:40:00' : 'I',
			'10:41:00' : 'I',
			'10:42:00' : 'I',
			'10:43:00' : 'I',
			'10:44:00' : 'I',
			'10:45:00' : 'I',
			'10:46:00' : 'I',
			'10:47:00' : 'I',
			'10:48:00' : 'I',
			'10:49:00' : 'I',
			'10:50:00' : 'I',
			'10:51:00' : 'I',
			'10:52:00' : 'I',
			'10:53:00' : 'I',
			'10:54:00' : 'I',
			'10:55:00' : 'I',
			'10:56:00' : 'I',
			'10:57:00' : 'I',
			'10:58:00' : 'I',
			'10:59:00' : 'I',
			'11:00:00' : 'J',
			'11:01:00' : 'J',
			'11:02:00' : 'J',
			'11:03:00' : 'J',
			'11:04:00' : 'J',
			'11:05:00' : 'J',
			'11:06:00' : 'J',
			'11:07:00' : 'J',
			'11:08:00' : 'J',
			'11:09:00' : 'J',
			'11:10:00' : 'J',
			'11:11:00' : 'J',
			'11:12:00' : 'J',
			'11:13:00' : 'J',
			'11:14:00' : 'J',
			'11:15:00' : 'J',
			'11:16:00' : 'J',
			'11:17:00' : 'J',
			'11:18:00' : 'J',
			'11:19:00' : 'J',
			'11:20:00' : 'J',
			'11:21:00' : 'J',
			'11:22:00' : 'J',
			'11:23:00' : 'J',
			'11:24:00' : 'J',
			'11:25:00' : 'J',
			'11:26:00' : 'J',
			'11:27:00' : 'J',
			'11:28:00' : 'J',
			'11:29:00' : 'J',
			'11:30:00' : 'K',
			'11:31:00' : 'K',
			'11:32:00' : 'K',
			'11:33:00' : 'K',
			'11:34:00' : 'K',
			'11:35:00' : 'K',
			'11:36:00' : 'K',
			'11:37:00' : 'K',
			'11:38:00' : 'K',
			'11:39:00' : 'K',
			'11:40:00' : 'K',
			'11:41:00' : 'K',
			'11:42:00' : 'K',
			'11:43:00' : 'K',
			'11:44:00' : 'K',
			'11:45:00' : 'K',
			'11:46:00' : 'K',
			'11:47:00' : 'K',
			'11:48:00' : 'K',
			'11:49:00' : 'K',
			'11:50:00' : 'K',
			'11:51:00' : 'K',
			'11:52:00' : 'K',
			'11:53:00' : 'K',
			'11:54:00' : 'K',
			'11:55:00' : 'K',
			'11:56:00' : 'K',
			'11:57:00' : 'K',
			'11:58:00' : 'K',
			'11:59:00' : 'K',
			'12:00:00' : 'L',
			'12:01:00' : 'L',
			'12:02:00' : 'L',
			'12:03:00' : 'L',
			'12:04:00' : 'L',
			'12:05:00' : 'L',
			'12:06:00' : 'L',
			'12:07:00' : 'L',
			'12:08:00' : 'L',
			'12:09:00' : 'L',
			'12:10:00' : 'L',
			'12:11:00' : 'L',
			'12:12:00' : 'L',
			'12:13:00' : 'L',
			'12:14:00' : 'L',
			'12:15:00' : 'L',
			'12:16:00' : 'L',
			'12:17:00' : 'L',
			'12:18:00' : 'L',
			'12:19:00' : 'L',
			'12:20:00' : 'L',
			'12:21:00' : 'L',
			'12:22:00' : 'L',
			'12:23:00' : 'L',
			'12:24:00' : 'L',
			'12:25:00' : 'L',
			'12:26:00' : 'L',
			'12:27:00' : 'L',
			'12:28:00' : 'L',
			'12:29:00' : 'L',
			'12:30:00' : 'M',
			'12:31:00' : 'M',
			'12:32:00' : 'M',
			'12:33:00' : 'M',
			'12:34:00' : 'M',
			'12:35:00' : 'M',
			'12:36:00' : 'M',
			'12:37:00' : 'M',
			'12:38:00' : 'M',
			'12:39:00' : 'M',
			'12:40:00' : 'M',
			'12:41:00' : 'M',
			'12:42:00' : 'M',
			'12:43:00' : 'M',
			'12:44:00' : 'M',
			'12:45:00' : 'M',
			'12:46:00' : 'M',
			'12:47:00' : 'M',
			'12:48:00' : 'M',
			'12:49:00' : 'M',
			'12:50:00' : 'M',
			'12:51:00' : 'M',
			'12:52:00' : 'M',
			'12:53:00' : 'M',
			'12:54:00' : 'M',
			'12:55:00' : 'M',
			'12:56:00' : 'M',
			'12:57:00' : 'M',
			'12:58:00' : 'M',
			'12:59:00' : 'M'
			}

#functions
def timestamp(datetimestamp):
	#process IB's date-time format and provide the last 8 characters, which HH:MM:SS
	return datetimestamp[10:]

def datestamp(datetimestamp):
	#process IB's date-time format and provide the first 8 characters, which MMDDYYYY
	return datetimestamp[:8]

def code(datetimestamp):
	#use the timestamp of each tick data and assign a code by looking up our reference
	return coderef.get(timestamp(datetimestamp), '-')	

def print_message_from_ib(msg):
	#a function to receive all messages from IB and print output so we can catch errors
    print(msg)

def print_data_from_ib(msg):
	#a function to receive only Historical Data type of data from IB and do something with it
	#print(round(msg.close, precision))
	ticks.append(str(round(msg.close, precision))+' '+datestamp(msg.date)+' '+code(msg.date)) #ticks will hold a list of tick information we need
	dates.append(datestamp(msg.date)) #get just the date in IB format
	prices.append(round(msg.close, precision)) #get the prices rounded off (Need to figure this out, maybe a user input)
	
def create_contract(symbol, sec_type, exch, prim_exch, curr):
	#IbPy code for creating an IB format contract to ask IB to get data for
	contract = Contract()
	contract.m_symbol = symbol
	contract.m_secType = sec_type
	contract.m_exchange = exch
	contract.m_primaryExch = prim_exch
	contract.m_currency = curr
	return contract
	print(dates, prices)

def getData():
	#get data from TWS using IbPy wrapped interface commands	
	conn = Connection.create(port=4001, clientId=65) 	#create a connection object, use a port / id that match IB
	conn.registerAll(print_message_from_ib) 		#register message receipt function
	conn.register(print_data_from_ib, 'HistoricalData') #register data receipt function
	conn.connect() 										#make connection
	time.sleep(1) 										#Simply to give the program time to print messages sent from IB	
	mycontract = create_contract(tickername, tickertype, tickerexch, tickerprimaryexch, tickercurr)
	conn.reqHistoricalData(101, mycontract, ts, lookback, interval, 'TRADES', 1, 1)
	time.sleep(5) 										#Simply to give the program time to print messages sent from IB
	conn.disconnect()

def formatdata():
	tpos = sorted(set(ticks), reverse=True)
	tpos.remove('-1 finished -') #massaging the data
	#print(tpos)
	levels = sorted(set(prices), reverse=True)
	levels.remove(-1) #massaging the data
	periods = sorted(set(dates))
	periods.remove('finished') #massaging the data
	
	lowprice = float(levels[0])
	startdate = int(periods[0])
	highprice = float(levels[-1])
	enddate = int(periods[-1])
	days = len(periods)
	points = len(levels)
	
	#checks
	#print(lowprice, startdate, highprice, enddate, days, points)
	#print(periods, levels)
	
	#initialize table with null elements
	p = 0
	while p <= points:
		d = 0
		#setup row first line)
		if p == 0:
				trow = ['Price/Date']
		else:
			trow = [levels[p-1]]		
		
		while d < days:
			if p == 0:
				trow.append(periods[d])			
			else:
				trow.append('')
			d += 1
		table.append(trow)
		p += 1

	#modify table values to get TPO charts	
	for t in tpos:
		ntposplit = t.split(' ')		
		ntpoprice = float(ntposplit[0]) #needs to be int because of rounded prices
		ntpodate = ntposplit[1] 	#this can be string
		ntpocode = ntposplit[2]
		p = levels.index(ntpoprice) + 1
		q = periods.index(ntpodate) + 1
		#check
		#print(ntpoprice, p, ntpodate, q)
		if table[p][q].count(ntpocode) <= 0:
			ecode = str(table[p][q])			
			table[p][q] =  ntpocode + ecode
	
	#add POC and VA markers on TPO charts
	for d in periods:
		maxlen = 0
		cumlen = []
		cumlen.append(0)
		vah = 0
		val = 0
		maxp = ''
		q = periods.index(d) + 1
		for l in levels:
			p = levels.index(l) + 1
			#check
			#print(ntpoprice, p, ntpodate, q)
			cumlen.append(cumlen[p-1] + len(table[p][q]))
			if len(table[p][q]) >= maxlen:
				maxlen = len(table[p][q])
				maxp = p
		table[maxp][q] = table[maxp][q] + '*'#+ str(levels[maxp])
		for l in levels:
			p = levels.index(l) + 1
			cumlen[p]=cumlen[p]/cumlen[-1]
			if (cumlen[p]>0.15 and vah <= 0 and table[p][q].find('<<POC>>') < 0):
				table[p][q] = table[p][q] + '<'#+ str(levels[p])
				vah += 1
			if (cumlen[p]>0.85 and val <= 0 and table[p][q].find('<<POC>>') < 0):
				table[p][q] = table[p][q] + '<'#+ str(levels[p])
				val += 1

def writeDataToCSV():	
	import csv
	with open('./arrays.csv', 'w') as csvfile:
		writer = csv.writer(csvfile, dialect='excel')
		writer.writerows(table)
	now = datetime.datetime.now()
	ts = now.strftime('%Y%m%d')	
	fp = open("arrays.csv", "r") 
	pt = from_csv(fp) 
	fp.close()
	pt.align = "l"
	print(tickername + ' TPOs ' + 'for ' + ts + ' -' + lookback + ' @' + interval + ' interval.')
	print(pt)
    
if __name__ == "__main__": 
	getData()
	time.sleep(0)
	if (ticks == [] or dates == [] or prices == []): 
		print("Error Retrieving Data, Please Retry.")
	else: 
		formatdata()
		writeDataToCSV()
