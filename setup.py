from distutils.core import setup
import py2exe

setup(console=['notification.py'],
	options = {'py2exe' : {
		'packages' : ['bs4', 'mechanize','Tkinter', 'json', 'webbrowser']
	}})