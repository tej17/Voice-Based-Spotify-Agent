import json
import spotipy
import webbrowser
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import warnings
import time
import pyautogui


warnings.filterwarnings("ignore", category=DeprecationWarning) 
username = ''
clientID = ''
clientSecret = ''
redirect_uri = 'http://google.com/callback/'
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()


r = sr.Recognizer()
with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source)
	print("Please say something")
	audio = r.listen(source)

	try:

		speech = r.recognize_google(audio)
		print("You have said : \n" + speech)

		search_song = speech.split(" ")[1:]
		results = spotifyObject.search(search_song, 1, 0, "track")
		songs_dict = results['tracks']
		song_items = songs_dict['items']
		song = song_items[0]['external_urls']['spotify']
		# webbrowser.open(song)
		
		options = Options()
		options.add_argument("--window-size=1920,1080")
		driver = webdriver.Chrome(executable_path="/chromedriver.exe")
		driver.maximize_window()
		driver.get(song)

		time.sleep(15)
		login_button = driver.find_element("xpath","//*[@id='main']/div/div[2]/div[1]/header/div[5]/button[2]")
		login_button.click()
		
		time.sleep(5)
		driver.find_element("xpath","//*[@id='login-username']").send_keys("tthakkar@cs.stonybrook.edu")
		driver.find_element("xpath","//*[@id='login-password']").send_keys("")

		time.sleep(2)
		log_in_button = driver.find_element("xpath","//*[@id='login-button']")
		log_in_button.click()
		
		time.sleep(10)
		play_button = driver.find_element("xpath","//*[@id='main']/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div[4]/div/div/div/div/div/button")
		play_button.click()

		pyautogui.press("space")
		pyautogui.press("space")


		while True:
			pass
		# Login Button - /html/body/div[3]/div/div[2]/div[1]/header/div[5]/button[2]
		# Username - //*[@id="login-username"]
		# Password - //*[@id="login-password"]
		# Login - //*[@id="login-button"]

		
	except Exception as e:
		print("Error: " + str(e))



		
