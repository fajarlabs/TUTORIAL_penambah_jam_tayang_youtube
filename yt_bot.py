# from fp.fp import FreeProxy
from selenium import webdriver
import time
import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

UA = UserAgent() # From here we generate a random user agent
PROXIES = [] # Will contain proxies [ip, port]

DEBUG = False
MAX_TIMEOUT = 10 # two minutes

# Url Profile
YOUTUBE_URL = 'https://www.youtube.com/results?search_query=Fajarlabs'
# Klik profile
CLICK_PROFILE = '//*[@id="img"]'
# KLIK NAV PLAYLIST
NAV_LIST = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[3]/div'
# KLIK THUMBNAIL TUTORIAL
THUMB_PLAYLIST = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-playlist-renderer[1]/yt-formatted-string/a'
# COOKIE CONSENT
COOKIE_CONSENT = '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span'
# Choose playlist , recommended PLAY ALL
PLAY_ALL = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-playlist-sidebar-renderer/div/ytd-playlist-sidebar-primary-info-renderer/h1/yt-formatted-string/a'
# CONTROL
LOOP_CTRL = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/ytd-playlist-panel-renderer/div/div[1]/div/div[2]/div[1]/div[1]/ytd-menu-renderer/div[2]/ytd-toggle-button-renderer[1]/a/yt-icon-button/button'
SHUFFLE_CTRL = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/ytd-playlist-panel-renderer/div/div[1]/div/div[2]/div[1]/div[1]/ytd-menu-renderer/div[2]/ytd-toggle-button-renderer[2]/a/yt-icon-button/button'

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

if __name__ == '__main__':
	USE_PROXY = False
	
	while True :
		driver = None
		proxy = ""
		try :
			prox = getProxy()
			firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
			firefox_capabilities['marionette'] = True
			proxy = prox["ip"]+":"+prox["port"]

			if USE_PROXY == True :
				firefox_capabilities['proxy'] = {
				    "proxyType": "MANUAL",
				    "httpProxy": proxy,
				    "ftpProxy": proxy,
				    "sslProxy": proxy
				}
			browser = webdriver.Firefox(capabilities=firefox_capabilities)
			print(">> Query search channel :"+YOUTUBE_URL)
			browser.get(YOUTUBE_URL)

			time.sleep(5)
			
			for i in range(MAX_TIMEOUT):
				state = False
				try :
					print("Waiting checking COOKIE CONSENT..")
					cookie_start = browser.find_element_by_xpath(COOKIE_CONSENT)
					cookie_start.click()
					state = True
				except Exception as e :
					if DEBUG :
						print(e)

				if state :
					print(">> COOKIE CONSENT Passed..")
					break

				time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking PROFILE...")
					get_channel = browser.find_element_by_xpath(CLICK_PROFILE)
					get_channel.click()
					state = True
				except Exception as e :
					if DEBUG :
						print(e)

				if state :
					print(">> COOKIE CONSENT passed..")
					break

				time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking NAVIGATION LIST..")
					nav_list = browser.find_element_by_xpath(NAV_LIST)
					nav_list.click()
					state = True
				except Exception as e :
					if DEBUG :
						print(e)

				if state :
					print(">> NAVIGATION LIST passsed..")
					break

				time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking THUMB_PLAYLIST..")
					play_list = browser.find_element_by_xpath(THUMB_PLAYLIST)
					play_list.click()
					state = True
				except Exception as e :
					if DEBUG :
						print(e)

				if state :
					print(">> THUMB_PLAYLIST passed..")
					break

				time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking PLAY PLAYLIST..")
					play_playlist = browser.find_element_by_xpath(PLAY_ALL)
					play_playlist.click()
					state = True
				except Exception as e :
					if DEBUG :
						print(e)

				if state :
					print(">> PLAY PLAYLIST passed..")
					break

				time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False
				try :
					print("Waiting checking SHUFFLE_CTRL..")
					ctrl_shuffle = browser.find_element_by_xpath(SHUFFLE_CTRL)
					ctrl_shuffle.click()
					state = True
				except Exception as e :
					if DEBUG :
						print(e)

				if state :
					print("SHUFFLE_CTRL passed..")
					break

				time.sleep(1)

			for i in range(MAX_TIMEOUT):
				state = False

				try :
					print("Waiting checking LOOP_CTRL..")
					ctrl_loop = browser.find_element_by_xpath(LOOP_CTRL)
					ctrl_loop.click()
					state = True
				except Exception as e :
					if DEBUG :
						print(e)

				if state :
					print(">> Waiting checking LOOP_CTRL..")
					break

				time.sleep(1)

			print(">> Waiting to rotating in more than 3000 seconds")
			for i in range(4000):
				if i > random.randint(1800,6000) :
					break
				time.sleep(1)

			try :
				print("Close browser")
				browser.quit()
			except Exception as e :
				if DEBUG :
					print(e)

		except Exception as e :
			if DEBUG :
				print(e)
			print(e)
			try :
				print("Close browser")
				browser.quit()
			except Exception as e :
				if DEBUG :
					print(e)