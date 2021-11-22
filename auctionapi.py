import grequests
import json
from pprint import pprint
import time
import pydirectinput as pyd
import pyperclip
import numpy as np
import math
from pynput.mouse import Button, Controller as MouseController
from PIL import Image, ImageDraw, ImageGrab
import cv2
import pytesseract

mouse = MouseController()
auc_requirements = {"Gemstone_Mixture": {"item_name": "Gemstone Mixture", "tier": "RARE", "category": "misc", "price": 1301000}, 
					"Divan_Fragment": {"item_name": "Divan Fragment", "tier": "EPIC", "category": "misc", "price": 1701000}}
'''auc_requirements = {"Divan_Fragment": {"item_name": "Divan Fragment", "tier": "EPIC", "category": "misc", "price": 1701000},
					"Gemstone_Mixture": {"item_name": "Gemstone Mixture", "tier": "RARE", "category": "misc", "price": 1201000}}'''
'''auc_requirements = {"Diamante's_Handle": {"item_name": "Diamante's Handle", "tier": "", "category": "misc", "price": 1251000}}'''
'''auc_requirements = {"One_For_All_I": {"item_name": "One For All I", "tier": "COMMON", "category": "misc", "price": 12001000},
					"Diamante's_Handle": {"item_name": "Diamante's Handle", "tier": "", "category": "misc", "price": 1251000}}'''

API_KEY = "f588fdd8-00f1-4eca-ade3-cac67f5ab656"

data = {}
auction_final = []
auction_final_cheapest = {}
auction_final_cheapest_sorted = []

start_time = time.time()

url_base = f"https://api.hypixel.net/skyblock/auctions?key={API_KEY}"

temp_auc = []

def check_if_found():
	# Path of tesseract executable
	#pytesseract.pytesseract.tesseract_cmd ='C:\Program Files\Tesseract-OCR\tesseract'
	# ImageGrab-To capture the screen image in a loop. 
	# Bbox used to capture a specific area.

	cap5 = ImageGrab.grab(bbox = (0, 1920, 1920, 1980))
	cap6 = cv2.cvtColor(np.array(cap5), cv2.COLOR_BGR2GRAY)

	(irrelevant, dirimagepre) = cv2.threshold(cap6, 103, 255, cv2.THRESH_TOZERO)
	(irrelevant, directionimage) = cv2.threshold(dirimagepre, 105, 255, cv2.THRESH_TOZERO_INV)

	#cv2.imshow('ooga', directionimage)
	#cv2.waitKey(0)
	# Converted the image to monochrome for it to be easily 
	# read by the OCR and obtained the output String.

	direction = pytesseract.image_to_string(directionimage, lang = 'mc')

	return(direction)

def check_if_collect():
	# Path of tesseract executable
	#pytesseract.pytesseract.tesseract_cmd ='C:\Program Files\Tesseract-OCR\tesseract'
	# ImageGrab-To capture the screen image in a loop. 
	# Bbox used to capture a specific area.

	'''cap3 = ImageGrab.grab(bbox = (1965, 820, 400, 100))
	cap4 = cv2.cvtColor(np.array(cap3), cv2.COLOR_BGR2GRAY)
	cv2.imshow('ooga', cap4)
	cv2.waitKey(0)
	(irrelevant, dirimagepre) = cv2.threshold(cap4, 103, 255, cv2.THRESH_TOZERO)
	(irrelevant, directionimage) = cv2.threshold(dirimagepre, 105, 255, cv2.THRESH_TOZERO_INV)'''

	cap3 = ImageGrab.grab(bbox = (1965, 820, 2365, 920))
	cap4 = cv2.cvtColor(np.array(cap3), cv2.COLOR_BGR2GRAY)
	(irrelevant, dirimagepre) = cv2.threshold(cap4, 128, 255, cv2.THRESH_TOZERO)
	(irrelevant, directionimage) = cv2.threshold(dirimagepre, 130, 255, cv2.THRESH_TOZERO_INV)

	#cv2.imshow('ooga', directionimage)
	#cv2.waitKey(0)
	# Converted the image to monochrome for it to be easily 
	# read by the OCR and obtained the output String.

	direction = pytesseract.image_to_string(directionimage, lang = 'mc')

	return(direction)

def click():
	pyd.mouseDown()
	z = np.random.normal(0.07,0.02,None)
	print(z)
	time.sleep(z)
	pyd.mouseUp()

def smoothAccel(degrees, rotatedirection = "+", axis = "x"):
	px = 10*degrees
	diff = 0
	if rotatedirection == "+" and axis == "x":
		n = 0
		totalinc = 0
		inc = 0
		final_inc = 0
		rotation_time = np.random.normal(0.25,0.075,None)
		interval = int(rotation_time*60)
		if interval%2 == 1:
			interval += -1
		for i in range(interval):
			diff = px-totalinc
			if i < interval/2:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				totalinc += inc
				mouse.move(inc,0)
				time.sleep(1/60)
			elif i < interval-4:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				if inc > 4:
					mouse.move(inc,0)
					final_inc = inc
					totalinc += inc
				else:
					continue
				time.sleep(1/60)
		while diff > 0:
			if final_inc == 0:
				final_inc = 1
			if diff % final_inc == 0:
				mouse.move(final_inc,0)
				time.sleep(1/60)
				totalinc += final_inc
			elif diff > final_inc: 
				mouse.move(final_inc,0)
				time.sleep(1/60)
				totalinc += final_inc
			else:
				mouse.move(diff % final_inc,0)
				time.sleep(1/60)
				totalinc += diff % final_inc
			diff = px - totalinc
	elif rotatedirection == "-" and axis == "x":
		n = 0
		totalinc = 0
		inc = 0
		final_inc = 0
		rotation_time = abs(np.random.normal(0.5,0.3,None))
		interval = int(rotation_time*60)
		if interval%2 == 1:
			interval += -1
		for i in range(interval):
			diff = px-totalinc
			if i < interval/2:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				totalinc += inc
				mouse.move(-inc,0)
				time.sleep(1/60)
			elif i < interval-4:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				if inc > 4:
					mouse.move(-inc,0)
					final_inc = inc
					totalinc += inc
				else:
					continue
				time.sleep(1/60)
		while diff > 0:
			if final_inc == 0:
				final_inc = 1
			if diff % final_inc == 0:
				mouse.move(-final_inc,0)
				time.sleep(1/60)
				totalinc += final_inc
			elif diff > final_inc: 
				mouse.move(-final_inc,0)
				time.sleep(1/60)
				totalinc += final_inc
			else:
				mouse.move(-1*(diff % final_inc),0)
				time.sleep(1/60)
				totalinc += diff % final_inc
			diff = px - totalinc
	if rotatedirection == "-" and axis == "y":
		n = 0
		totalinc = 0
		inc = 0
		final_inc = 0
		rotation_time = np.random.normal(0.25,0.075,None)
		interval = int(rotation_time*60)
		if interval%2 == 1:
			interval += -1
		for i in range(interval):
			diff = px-totalinc
			if i < interval/2:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				totalinc += inc
				mouse.move(0,inc)
				time.sleep(1/60)
			elif i < interval-4:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				if inc > 4:
					mouse.move(0,inc)
					final_inc = inc
					totalinc += inc
				else:
					continue
				time.sleep(1/60)
		while diff > 0:
			if final_inc == 0:
				final_inc = 1
			if diff % final_inc == 0:
				mouse.move(0,final_inc)
				time.sleep(1/60)
				totalinc += final_inc
			elif diff > final_inc: 
				mouse.move(0,final_inc)
				time.sleep(1/60)
				totalinc += final_inc
			else:
				mouse.move(0,diff % final_inc)
				time.sleep(1/60)
				totalinc += diff % final_inc
			diff = px - totalinc
	elif rotatedirection == "+" and axis == "y":
		n = 0
		totalinc = 0
		inc = 0
		final_inc = 0
		rotation_time = abs(np.random.normal(0.5,0.3,None))
		interval = int(rotation_time*60)
		if interval%2 == 1:
			interval += -1
		for i in range(interval):
			diff = px-totalinc
			if i < interval/2:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				totalinc += inc
				mouse.move(0,-inc)
				time.sleep(1/60)
			elif i < interval-4:
				inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
				if inc > 4:
					mouse.move(0,-inc)
					final_inc = inc
					totalinc += inc
				else:
					continue
				time.sleep(1/60)
		while diff > 0:
			if final_inc == 0:
				final_inc = 1
			if diff % final_inc == 0:
				mouse.move(0,-final_inc)
				time.sleep(1/60)
				totalinc += final_inc
			elif diff > final_inc: 
				mouse.move(0,-final_inc)
				time.sleep(1/60)
				totalinc += final_inc
			else:
				mouse.move(0,-1*(diff % final_inc))
				time.sleep(1/60)
				totalinc += diff % final_inc
			diff = px - totalinc

def checkAuctionItem(auction_item):

	# Check if item is BIN
	if("bin" not in auction_item):
		return (False, "Not BIN")

	# Check if item is already claimed
	if(auction_item["claimed"] == True):
		return (False, "Already claimed")

	# For unique obj ruleset
	for id in auc_requirements:

		# Start as valid item
		valid = True

		# For every rule in obj ruleset
		for req in auc_requirements[id]:

			# Make sure rule isn't price
			if(req != "price"):

				# Make sure it follows the rule
				if(auc_requirements[id][req] not in auction_item[req]):

					# No longer valid
					valid = False
					break

		# Found a potential match with a filter!
		if(valid):

			# Found a  match with a filter AND price! (Success)
			if(auction_item["starting_bid"] < auc_requirements[id]["price"]):
				dashed_uuid = auction_item['uuid'][:8] + '-' + auction_item['uuid'][8:12] + '-' + auction_item['uuid'][12:16]
				dashed_uuid += '-' + auction_item['uuid'][16:20] + '-' + auction_item['uuid'][20:]
				return (True, (id, f"/viewauction {dashed_uuid}", auction_item['starting_bid'], auction_item["item_name"]))


	# Broke on one of the requirements
	return (False, "Not all requirements met")


# Async to first page
while True:
	resp = grequests.get(url_base)
	#print(check_if_found())
	for res in grequests.map([resp]):
		data = json.loads(res.content)
		total_pages = data['totalPages']
		print(f"Total Pages found: {data['totalPages']}")

		# Verify success
		if(data["success"]):
			# Get items from page 0
			for auction_item in data["auctions"]:
				try:
					item_ans = checkAuctionItem(auction_item)
					# Passed filter
					if(item_ans[0]):
						auction_final.append(item_ans[1])
					# Failed filter
					else:
						pass
				except:
					pprint(data)

		# Unsuccessful GET request
		else:
			print(f"Failed GET request: {data['cause']}")


	first_page_time = time.time()

	# Get all page urls
	urls = []
	for page_count in range(1, total_pages+1):
		urls.append(f"{url_base}&page={page_count}")

	# Async to remaining pages
	resp = (grequests.get(url) for url in urls)

	made_requests_time = time.time()

	# Get items from remaining pages
	for res in grequests.map(resp):
		data = json.loads(res.content)

		# Verify success
		if(data["success"]):
			# Get items from pages 1 -> n
			for auction_item in data["auctions"]:
				try:
					item_ans = checkAuctionItem(auction_item)
					# Passed filter
					if(item_ans[0]):
						auction_final.append(item_ans[1])
					# Failed filter
					else:
						pass
				except:
					pprint(data)

		# Unsuccessful GET request
		else:
			print(f"Failed GET request: {data['cause']}")

	# Debug for amount of items found
	print(f"{len(auction_final)} items found")

	# Sort out the results
	auction_final = sorted(auction_final, key=lambda x: (x[0], x[2]))

	print(auction_final)

	# Get only the cheapest of every time
	for auc in auction_final:

		# If not in new dict yet
		if(auc[0] not in auction_final_cheapest):
			auction_final_cheapest[auc[0]] = auc

		# If already in new dict, compare against previous
		else:
			if(auc[2] < auction_final_cheapest[auc[0]][2]):
				auction_final_cheapest[auc[0]] = auc

	# Add all items from cheapest to cheapest_sorted
	for auc in auction_final_cheapest:
		auction_final_cheapest_sorted.append(auction_final_cheapest[auc])

	# Sort cheapest_sorted
	auction_final_cheapest_sorted = sorted(auction_final_cheapest_sorted, key=lambda x: x[2])


	end_time = time.time()

	for i in range(len(auction_final)):
		if auction_final[i] not in temp_auc:
			write = auction_final[i][1]
			print(write)
			pyperclip.copy(write)
			pyd.keyDown("t")
			pyd.keyUp("t")
			pyd.keyDown("ctrl")
			pyd.keyDown("v")
			pyd.keyUp("ctrl")
			pyd.keyUp("v")
			pyd.keyDown("enter")
			time.sleep(1/30)
			pyd.keyUp("enter")
			if ("This" not in check_if_found()):
				smoothAccel(12, "+", "y")
				collect_test = check_if_collect()
				print(collect_test)
				if ("C" in collect_test):
					pyd.keyDown("esc")
					pyd.keyUp("esc")
				else:
					click()
					smoothAccel(12, "-")
					click()
			else:
				print("Not found")
				print(check_if_found())
			time.sleep(0.75)

	temp_auc = auction_final
	auction_final = []

	time.sleep(1)

#print(f"Time Taken: {end_time-start_time}\n\tFirst Page: {first_page_time-start_time}\n\tFinished Requests: {made_requests_time-start_time}")