import mechanize
from bs4 import BeautifulSoup
from Tkinter import *
import json
import webbrowser

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
def init():
	m.set("Trying to log in!")
	file = open("logininfo.txt", "r")
	res = json.loads(file.read())
	username = res["username"]
	password = res["password"]
	file.close()
	res = br.open("http://codeforces.com/enter")
	if res.code == 200:
		br.select_form(nr=1)
		br["handle"] = username
		br["password"] = password
		result = br.submit()
		if "Invalid handle or password" in result.read():
			m.set("Invalid handle or password!")
			return False
		else:
			m.set("Now retrieving unread blogs!")
			return True
	else:
		m.set("Failed to reach the server!")
		return False
def main():
	status = init()
	if status == False:
		return
	file = open("favourite.txt", "r")
	d = json.loads(file.read())
	urls = d["favs"]
	file.close()
	new = []
	for blog in urls:
		soup = BeautifulSoup(br.open(blog))
		unread = soup.findAll("table", {"class" : "comment-table highlight-blue"})
		if len(unread) > 0:
			new.append({"url" : blog, "unread" : len(unread), "title" : soup.title.text})
	win1 = Tk()
	win1.title("Codeforces Blog Notifier")
	win1.geometry("300x300")
	for blog in new:
		url = blog["url"]
		label = Label(win1, text=blog["title"])
		label.bind("<Button-1>",lambda e,url=url:webbrowser.open(url))
		label1 = Label(win1, text = str(blog["unread"]) + " new comments")
		label.pack()
		label1.pack()
	if len(new) == 0:
		label = Label(win1, text = "No new comments in any blog!")
		label.pack()
def updateUP():
	file = open("logininfo.txt", "w")
	username = uTextBox.get()
	password = pTextBox.get()
	login = {"username" : username, "password" : password}
	file.write(json.dumps(login))
	file.close()
	m.set("Username & Password is updated!")
	uTextBox.delete(0, len(username))
	pTextBox.delete(0, len(password))
def addFav():
	file = open("favourite.txt", "r")
	d = json.loads(file.read())
	urls = d["favs"]
	file.close()
	newURL = favTextBox.get()
	if newURL != "" and newURL not in urls:
		file = open("favourite.txt", "w")
		urls.append(newURL)
		file.write(json.dumps({"favs" : urls}))
		file.close()
		m.set("URL successfully added!")
		favTextBox.delete(0, len(newURL))
	else:
		m.set("This URL already exists in favs!")
def delete(url, widgets):
	file = open("favourite.txt", "r")
	d = json.loads(file.read())
	urls = d["favs"]
	file.close()
	for w in widgets:
		if w["url"] == url:
			urls.remove(url)
			file = open("favourite.txt", "w")
			file.write(json.dumps({"favs" : urls}))
			file.close()
			w["label"].pack_forget()
			w["button"].pack_forget()
			return
def delFav():
	win2 = Tk()
	win2.title("Manage Favourites")
	win2.geometry("300x300")
	file = open("favourite.txt", "r")
	d = json.loads(file.read())
	urls = d["favs"]
	file.close()
	widgets = []
	for url in urls:
		label = Label(win2, text = url)
		button = Button(win2, text = "Delete")
		widgets.append({"url" : url, "label" : label, "button" : button})
	for w in widgets:
		w["button"].configure(command = lambda w=w: delete(w["url"], widgets))
		w["label"].pack()
		w["button"].pack()
window = Tk()
m = StringVar()
window.title("Codeforces Blog Notifier")
window.geometry("300x300")
window.configure(background = "#a1dbcd")
uLabel = Label(window, text = "Username")
uTextBox = Entry(window)
pLabel = Label(window, text = "Password")
pTextBox = Entry(window)
updateButton = Button(window, text = "Update Username & Password", command = updateUP)
favTextBox = Entry(window)
favButton = Button(window, text = "Add Favourite Blog", command = addFav)
delButton = Button(window, text = "Manage Stored Blogs", command = delFav)
notifierButton = Button(window, text = "Run Notifier", command = main)
message = Label(window, textvariable = m, fg = "red")
uLabel.pack()
uTextBox.pack()
pLabel.pack()
pTextBox.pack()
updateButton.pack()
favTextBox.pack()
favButton.pack()
delButton.pack()
notifierButton.pack()
message.pack()
window.mainloop()