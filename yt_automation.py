from selenium import webdriver
import time
import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import configparser
from selenium.webdriver.firefox.options import Options
import signal
import logging
import sys
import os
import itertools
import threading
import base64
import speedtest

#function that gets the download speed in mega bytes per second
def get_final_speed():
    rawspeed = speedtest.Speedtest().download()
    roundedspeed = round(rawspeed)
    finalspeed = roundedspeed / 1e+6
    return finalspeed

# Fungsi proxy untuk pindah-pindah lokasi / negara
def getProxy():
  
  # Retrieve latest proxies
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', UA.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    PROXIES.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

  # Choose a random proxy
  proxy_index = random_proxy()
  proxy = PROXIES[proxy_index]

  return proxy

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(PROXIES) - 1)

def closeBrowser():
	global BROWSER, DEBUG

	print("Process clossing browser..")

	try :
		time.sleep(1)
		BROWSER.close()
		print(">> Close current browser OK")
	except Exception as e :
		logging.error(str(e))
		if DEBUG :
			print(e)

	try :
		time.sleep(1)
		BROWSER.quit()
		print(">> Close all browser OK")
		time.sleep(1)
	except Exception as e :
		logging.error(str(e))
		if DEBUG :
			print(e)

def handler(signal, frame):
	global LOOP

	LOOP = False	
	print("Force close...")

	if os.name == 'nt' :
		os.system("TASKKILL /F /IM firefox.exe")
	else :
		os.system("kill -9 $(ps -x | grep firefox)")

		sys.exit(0)
		os._exit(0)

done = False
#here is the animation
def animate(txt):
		for c in itertools.cycle(['|', '/', '-', '\\']):
			if done :
				c = 'OK\n'
			lt = '\r'+ txt + ' ' + c
			sys.stdout.write(lt)
			sys.stdout.flush()
			time.sleep(0.1)
			if done and (c == 'OK\n') :
				break

if __name__ == '__main__':
	UA = UserAgent() # From here we generate a random user agent
	PROXIES = [] # Will contain proxies [ip, port]

	DEBUG = False
	MAX_TIMEOUT = 10 # two minutes
	BROWSER = None
	LOOP = True

	# clear command line
	# for windows OS
	if os.name =="nt":
		os.system("cls")    
	# for linux / Mac OS
	else:
		os.system("clear")

	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S", filename='yt_automation.log', filemode='w')
	signal.signal(signal.SIGINT, handler)

	_developer ="""
** This is for research purposes only **
███████████████████████████████████████████████████████
█▄─▄▄─██▀▄─████▄─▄██▀▄─██▄─▄▄▀█▄─▄████▀▄─██▄─▄─▀█─▄▄▄▄█
██─▄████─▀─██─▄█─███─▀─███─▄─▄██─██▀██─▀─███─▄─▀█▄▄▄▄─█
▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀
-> Jangan lupa SHARE, LIKE & SUBSCRIBE untuk melihat video terbaru <-
	"""
	print(_developer)
	threading.Thread(target=animate, args=("Sedang periksa kecepatan internet anda..",)).start()

	speedInternet = get_final_speed()
	done = True

	time.sleep(1)
	print("Kecepatan internet anda : %s Mbps" % (speedInternet))
	print("Bot Youtube dimulai..")

	if(speedInternet <= 2) :
		threading.Thread(target=animate, args=("Internet anda kurang mendukung atau dibawah 2 mbps..",)).start()
		time.sleep(2)
		done = True
		sys.exit(0)
		os._exit(0)
	YT_CONFIG = configparser.ConfigParser()
	YT_CONFIG.read('yt_config.ini')
	
	while LOOP :
		logging.info("BOT Started...")
		proxy = ""
		try :
			options = Options()
			if YT_CONFIG['SETTING']['IS_HEADLESS'] == 'Y':
				options.headless = True
			prox = getProxy()
			firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
			firefox_capabilities['marionette'] = True
			proxy = prox["ip"]+":"+prox["port"]

			if YT_CONFIG['SETTING']['PROXY'] == 'Y' :
				firefox_capabilities['proxy'] = {
				    "proxyType": "MANUAL",
				    "httpProxy": proxy,
				    "ftpProxy": proxy,
				    "sslProxy": proxy
				}
			BROWSER = webdriver.Firefox(options=options, capabilities=firefox_capabilities)
			print(">> Query search channel :"+YT_CONFIG['ELEMENT']['YOUTUBE_URL'])
			BROWSER.get(YT_CONFIG['ELEMENT']['YOUTUBE_URL'])

			if speedInternet < 3 :
				time.sleep(5)
			else :
				time.sleep(1)

			if YT_CONFIG['SETTING']['IS_COOKIE_CONSENT'] == 'Y' :
				for i in range(MAX_TIMEOUT):
					state = False
					try :
						print("Waiting checking COOKIE CONSENT..")
						cookie_start = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['COOKIE_CONSENT'])
						cookie_start.click()
						state = True
					except Exception as e :
						logging.error(str(e))
						if DEBUG :
							print(e)

					if state :
						print(">> COOKIE CONSENT OK..")
						break

				time.sleep(1)

			time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False
				try :
					print("Waiting to searching channel..")
					trigger_input = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['YOUTUBE_SEARCH_INPUT'])
					trigger_input.click()
					time.sleep(1)
					insert_input = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['QUERY_INPUT_ELEMENT'])
					insert_input.send_keys(YT_CONFIG['SETTING']['CHANNEL_NAME'])
					time.sleep(1)
					cookie_start = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['FIND_BUTTON'])
					cookie_start.click()
					state = True
				except Exception as e :
					logging.error(str(e))
					if DEBUG :
						print(e)

				if state :
					print(">> SEARCHING CHANNEL OK..")
					break

				time.sleep(1)

			time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking PROFILE...")
					get_channel = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['CLICK_PROFILE'])
					get_channel.click()
					state = True
				except Exception as e :
					logging.error(str(e))
					if DEBUG :
						print(e)

				if state :
					print(">> CHECKING PROFILE OK..")
					break

				time.sleep(1)

			time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking NAVIGATION LIST..")
					nav_list = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['NAV_LIST'])
					nav_list.click()
					state = True
				except Exception as e :
					logging.error(str(e))
					if DEBUG :
						print(e)

				if state :
					print(">> NAVIGATION LIST passsed..")
					break

				time.sleep(1)

			time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking THUMB_PLAYLIST..")
					play_list = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['THUMB_PLAYLIST'])
					play_list.click()
					state = True
				except Exception as e :
					logging.error(str(e))
					if DEBUG :
						print(e)

				if state :
					print(">> THUMB_PLAYLIST OK..")
					break

				time.sleep(1)

			time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking PLAY PLAYLIST..")
					play_videolist = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['PLAY_VIDEOLIST'])
					play_videolist.click()
					state = True
				except Exception as e :
					logging.error(str(e))
					if DEBUG :
						print(e)

				if state :
					print(">> PLAY PLAYLIST OK..")
					break

				time.sleep(1)

			time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False
				try :
					print("Waiting checking SHUFFLE_CTRL..")
					ctrl_shuffle = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['SHUFFLE_CTRL'])
					ctrl_shuffle.click()
					state = True
				except Exception as e :
					logging.error(str(e))
					if DEBUG :
						print(e)

				if state :
					print("SHUFFLE_CTRL OK..")
					break

				time.sleep(1)

			time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking LOOP_CTRL..")
					ctrl_loop = BROWSER.find_element_by_xpath(YT_CONFIG['ELEMENT']['LOOP_CTRL'])
					ctrl_loop.click()
					state = True
				except Exception as e :
					logging.error(str(e))
					if DEBUG :
						print(e)

				if state :
					print(">> Waiting checking LOOP_CTRL..")
					break

				time.sleep(1)

			_MAX_RAND = 6000
			stop_rand = random.randint(_MAX_RAND/2,_MAX_RAND)
			print(">> Waiting to rotating in more than %s seconds" % (stop_rand))

			for i in range(_MAX_RAND):
				if i > stop_rand :
					break
				time.sleep(1)
				if LOOP == False :
					time.sleep(1)
					break

			closeBrowser()

			if LOOP == False :
				break

		except Exception as e :
			logging.error(str(e))
			if DEBUG :
				print(e)