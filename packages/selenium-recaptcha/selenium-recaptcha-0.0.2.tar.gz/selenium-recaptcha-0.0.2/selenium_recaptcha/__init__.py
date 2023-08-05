from .components import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import speech_recognition as sr
import subprocess
import os
import urllib
from time import sleep

class Recaptcha_Solver:
	"""
	Usage:
		solver = Recaptcha_Solver(driver, ffmpeg_path)
		solver.solve_recaptcha()
	How to use:
		1. Pass your webdriver variable in driver param
		2. Download ffmpeg depending your os
		3. Then add the ffmpeg folder to your OS PATH
		or Copy your ffmpeg path and pass it to ffmpeg_path param
	"""
	def __init__(self,driver,ffmpeg_path='ffmpeg',debug=False):
		self.driver=driver
		self.mp3='captcha.mp3'
		self.wav='captcha.wav'
		self.ffmpeg_path=ffmpeg_path
		self.time_to_sleep_after_submit=3
		self.debug=debug

	def solve_recaptcha(self):
		iframe1=find_until_located(self.driver,By.XPATH,'//*[@title="reCAPTCHA"]')
		self.driver.switch_to.frame(iframe1)
		sleep(1)
		find_until_clicklable(self.driver,By.CLASS_NAME,'recaptcha-checkbox-border').click()
		sleep(1)
		self.driver.switch_to.default_content()
		iframe2=find_until_located(self.driver,By.XPATH,'//*[@title="recaptcha challenge expires in two minutes"]')
		self.driver.switch_to.frame(iframe2)
		sleep(1)
		find_until_clicklable(self.driver,By.ID,'recaptcha-audio-button').click()
		sleep(1)
		err=True
		try:
			header_text=self.driver.find_element(By.CLASS_NAME,'rc-doscaptcha-header-text')
		except:
			err=False

		if err:
			raise Exception('Sorry, looks like google blocking the captcha.')

		if self.debug==True:
			print('Solving Captcha...')
		audio_url=find_until_located(self.driver,By.CLASS_NAME,'rc-audiochallenge-tdownload-link').get_attribute('href')
		if self.debug==True:
			print('Downloading Audio...')
		urllib.request.urlretrieve(audio_url, self.mp3)
		if self.debug==True:
			print('Processing audio...')
		try:
			subprocess.call([self.ffmpeg_path, '-y', '-i', self.mp3, self.wav], stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)
		except:
			raise FileNotFoundError('Please download ffmpeg depending on your os and pass ffmpeg path to "ffmpeg_path" param')

		r=sr.Recognizer()

		def recognize_audio(wav_file):
			with sr.AudioFile(wav_file) as source:
				r.adjust_for_ambient_noise(source)
				audio=r.listen(source)
				text=r.recognize_google(audio)
				return text


		if self.debug==True:
			print('Recognizing audio...')

		text=recognize_audio(self.wav)

		os.remove(self.mp3)
		os.remove(self.wav)

		find_until_located(self.driver,By.ID,'audio-response').send_keys(text)
		sleep(1)
		find_until_clicklable(self.driver,By.ID,'recaptcha-verify-button').click()
		sleep(self.time_to_sleep_after_submit)
		msg=find_until_located(self.driver,By.CLASS_NAME,'rc-audiochallenge-error-message').text
		if msg!='':
			# find_until_clicklable(self.driver,By.ID,'recaptcha-reload-button').click()
			raise Exception('Captcha Could not be solved')
		else:
			if self.debug==True:
				print('Successfully Solved')
			self.driver.switch_to.default_content()