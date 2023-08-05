from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'reCaptcha v2 solver for selenium'
LONG_DESCRIPTION = '''
A package that allows to solve reCaptcha v2 with selenium.
<br>
<h3>Simple Example:</h3>
<pre><code>
from selenium import webdriver
from selenium_recaptcha import Recaptcha_Solver

driver = webdriver.Chrome()
driver.get('https://www.google.com/recaptcha/api2/demo')

solver = Recaptcha_Solver(
    driver=driver, # Your Web Driver
    ffmpeg_path='C:/Users/Administrator/Downloads/ffmpeg/bin/ffmpeg.exe', # FFmpeg Path
    debug=False
)
solver.solve_recaptcha()

</code></pre>

<h3>External Requirements:</h3>
<b><a href="https://ffmpeg.org/">FFmpeg Encoder</a></b>
<a href="https://ffmpeg.org/download.html#build-windows">Download For Windows</a>
<a href="https://ffmpeg.org/download.html#build-linux">Download For Linux</a>
<a href="https://ffmpeg.org/download.html#build-mac">Download For Mac</a>
'''

# Setting up
setup(
    name="selenium-recaptcha",
    version=VERSION,
    author="S M Shahriar Zarir",
    author_email="<shahriarzariradvance@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['SpeechRecognition', 'selenium'],
    keywords=['python', 'reCaptcha', 'bot','selenium','selenium recaptcha solver'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)