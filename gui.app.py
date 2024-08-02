from tkinter import *
from tkinter import filedialog
from scrapy.utils import project
from scrapy import spiderloader
from tkinter import messagebox
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import threading
import tkinter as tk


def get_spiders():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    return spider_loader.list()


def get_chosen_spider(value):
    global chosen_spider
    chosen_spider = value
    return chosen_spider


def get_chosen_feed(value):
    global chosen_feed
    chosen_feed = value
    return chosen_feed


def browse_button():
    global folder_path
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, END)
    folder_path_entry.insert(0, folder_path)
    return folder_path


def execute_spider():
    if dataset_entry.get() == '' or chosen_feed not in ['CSV', 'JSON']:
        messagebox.showerror('Error', 'All fields are required')
        return
    try:
        feed_uri = f"file:///{folder_path_entry.get()}/{dataset_entry.get()}.{chosen_feed}"
    except:
        messagebox.showerror('Error', 'All fields are required')

    settings = project.get_project_settings()
    settings.set('FEED_URI', feed_uri)
    settings.set('FEED_TYPE', chosen_feed)

    configure_logging()
    runner = CrawlerRunner(settings)
    runner.crawl(chosen_spider)
    reactor.run()


def start_execute_thread(event):
    global execute_thread
    execute_thread = threading.Thread(target=execute_spider, daemon=True)
    execute_thread.start()
    app.after(10, check_execute_thread)


def check_execute_thread():
    if execute_thread.is_alive():
        app.after(10, check_execute_thread)


def add_placeholder(entry, placeholder_text):
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')

    entry.insert(0, placeholder_text)
    entry.config(fg='grey')
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)


app = tk.Tk()

# spiders list
spider_label = Label(app, text="Choose a spider")
spider_label.grid(column=0, row=0, sticky=W, padx=10, pady=10)

spider_text = StringVar(app)
spider_text.set("Choose a spider")
spiders = get_spiders()

spiders_dropdown = OptionMenu(app, spider_text, *spiders, command=get_chosen_spider)
spiders_dropdown.grid(column=1, row=0, columnspan=2)

# feed type
feed_label = Label(app, text="Choose a feed")
feed_label.grid(column=0, row=1, sticky=W, padx=10, pady=10)

feed_text = StringVar(app)
feed_text.set("Choose a feed type")
feed = ["json", "csv"]

feed_dropdown = OptionMenu(app, feed_text, *feed, command=get_chosen_feed)
feed_dropdown.grid(column=1, row=1, columnspan=2)

# Path entry
folder_path_text = tk.StringVar(app)
folder_path_entry = tk.Entry(app, textvariable=folder_path_text)
folder_path_entry.grid(column=0, row=2, padx=10, pady=10)
add_placeholder(folder_path_entry, "Enter path or browse")

# Dataset entry
dataset_text = tk.StringVar(app)
dataset_entry = tk.Entry(app, textvariable=dataset_text, width=10)
dataset_entry.grid(column=1, row=2, padx=10, pady=10)
add_placeholder(dataset_entry, "listings")

# browse btn
browse_btn = Button(app, text='Browse', command=browse_button)
browse_btn.grid(column=2, row=2)

# execute btn
execute_btn = Button(app, text='Execute', command=lambda: start_execute_thread(None))
execute_btn.grid(column=0, row=3, columnspan=3)

app.title("Centris")
app.geometry("300x200")
app.resizable(False, False)
app.mainloop()
