import getpass
from tkinter import *
import re
import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import messagebox


# -------------------------------- AUTO COMPLETE STARST HERE-----------------------------#

#-------------------LIST FOR AUTOCOMPLETE SAVED IN ticker_list.txt -----------------#
lista=[]
with open("ticker_list") as f:
    for item in f:
        item = item.strip()
        lista.append(item)
#-------------------LIST FOR AUTOCOMPLETE SAVED IN ticker_list.txt -----------------#


class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

# ------------------------------- AUTO COMPLETE ENDS HERE -------------------------------------#


##################### ---------------------------------- GUI TKINTER STARTS HERE ----------------------------- ########################

root = Tk()

#---------------------------------- MENU START HERE -----------------------------#
def help():
    messagebox.showinfo("Help","How to use:\n1)Insert your tickers into the boxes, only choose tickers that show\n2)Choose the year span ( Make sure all tickers were out at that date)\n3)Click submit and watch the results")

def about():
    messagebox.showinfo("About","Made By Shay and Max ")


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=help)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
#------------------------------------ MENU END HERE ------------------------------- #

def delete(e):
    print("the focus actviated: do Nothing")


root.title('Efficient Frontier')
#title = Label(root, text="Efficient Frontier Assets").grid(row=0,column=0,columnspan=2,sticky=W+E+N+S)

#----------------------------Default 5 stock ticker entries ----------------------------#
row_4 = 4

label1 = Label(root, text="1").grid(row=row_4)
entry1 = AutocompleteEntry(lista, root, text="")
entry1.grid(row=row_4, column=1)


label2 = Label(root, text="2").grid(row=row_4+1)
entry2 = AutocompleteEntry(lista, root, text="")
entry2.grid(row=row_4+1, column=1)


label3 = Label(root, text="3").grid(row=row_4+2)
entry3 = AutocompleteEntry(lista, root, text="")
entry3.grid(row=row_4+2, column=1)



label4 = Label(root, text="4").grid(row=row_4+3)
entry4 = AutocompleteEntry(lista, root, text="")
entry4.grid(row=row_4+3, column=1)



label5 = Label(root, text="5").grid(row=row_4+4)
entry5 = AutocompleteEntry(lista, root, text="")
entry5.grid(row=row_4+4, column=1)



label3 = Label(root, text="6").grid(row=row_4+5)
entry3 = AutocompleteEntry(lista, root, text="")
entry3.grid(row=row_4+5, column=1)


label6 = Label(root, text="7").grid(row=row_4+6)
entry6 = AutocompleteEntry(lista, root, text="")
entry6.grid(row=row_4+6, column=1)


label7 = Label(root, text="3").grid(row=row_4+2)
entry7 = AutocompleteEntry(lista, root, text="")
entry7.grid(row=row_4+2, column=1)


label8 = Label(root, text="8").grid(row=row_4+7)
entry8 = AutocompleteEntry(lista, root, text="")
entry8.grid(row=row_4+7, column=1)

label9 = Label(root, text="9").grid(row=row_4+8)
entry9 = AutocompleteEntry(lista, root, text="")
entry9.grid(row=row_4+8, column=1)


label310 = Label(root, text="10").grid(row=row_4+9)
entry10 = AutocompleteEntry(lista, root, text="")
entry10.grid(row=row_4+9, column=1)


selected = []
entry_list =[]

global row
row = 14 # saved as 6, print the text as row-3


def addBox():
    global row
    Label(root, text=row-3).grid(row=row)
    ent_extra = AutocompleteEntry(lista, root, text="")
    ent_extra.grid(row=row, column=1)
    entry_list.append((ent_extra))
    row+=1

# Checking if an inserted stock is not present in the stock list
global bad_stock_flag
bad_stock_flag = False
bad_stocks = []
def submit():
    global bad_stock_flag
    if(entry1.get() != '' and entry1.get() in lista):
        selected.append(entry1.get())
    elif entry1.get() not in lista:
        bad_stocks.append(entry1.get())
        bad_stock_flag = True
    if (entry2.get() != '' and str(entry2.get()) in lista):
        selected.append(entry2.get())
    elif entry2.get() not in lista:
        bad_stocks.append(entry2.get())
        bad_stock_flag = True
    for number, (ent1) in enumerate(entry_list):
        if(ent1.get() != '' and ent1.get() in lista):
             selected.append(ent1.get())
        elif(not(ent1.get()  in lista)):
            bad_stocks.append(ent1.get())
            bad_stock_flag = True

    if(bad_stock_flag and selected != []):
        messagebox.showinfo("Incorrect Stock Inserted Error", "The stock\s: "+str(bad_stocks)[1:-1]+" Were not found\n"+"Showing results for: "+str(selected))
    elif selected ==[]:
        messagebox.showinfo("Error","Please insert at least 2 stocks")
    selected.append(entry3.get())
    selected.append(entry4.get())
    selected.append(entry5.get())

    root.destroy()
    global start_year
    start_year = change_dropdown1()
    global end_year
    end_year = change_dropdown2()



btn_add = Button(root, text="Add more +", command=addBox ,bg="#54DCFF")
btn_add.config(width =20)
btn_add.grid(row=2, columnspan=2)


submit = Button(root, text="Submit", command=submit,bg="#54DCFF")
submit.config(width =20)
submit.grid(row=3, columnspan=2)


# Create a Tkinter variable
year1 = StringVar(root)

# ------------------YEAR OPTIONS -------------------------
choices = [] # list of years
for i in range(1980, 2020):
    choices.append(i)
choices.reverse()


year1.set('2014') # set the default option
popupMenu = OptionMenu(root, year1, *choices)
popupMenu.config(width=5)
# Label(root, text="").grid(row = 1, column = 0, stickky=W)
popupMenu.grid(row = 1, column =0, sticky=W, ipadx=3, pady=5,columnspan=2)



year2 = StringVar(root)
year2.set('2018') # set the default option
popupMenu = OptionMenu(root, year2, *choices)
popupMenu.config(width=5)
# Label(root, text="To").grid(row = 1, column = 2, sticky=W,padx=0, pady=5,columnspan=2)
popupMenu.grid(row = 1, column =1, sticky=E, ipadx=3, pady=5,columnspan=2)

label_FROM = Label(root, text="From").grid(row=0,column=0)
label_TO = Label(root, text="To").grid(row=0,column=1)

def change_dropdown1(*args):
    return year1.get() + '-1-1'
year1.trace('w', change_dropdown1)
def change_dropdown2(*args):
    return year2.get() + '-1-1'
year2.trace('w', change_dropdown2)
#----------------- YEAR OPTIONS --------------------------


root.mainloop()
##################### ---------------------------------- GUI TKINTER ENDS HERE ----------------------------- ########################


##################### ---------------------------------- QUANDL STARTS HERE ----------------------------- ########################
quandl.ApiConfig.api_key = 'jkKcow3Zps9u--2z_deJ'
data = quandl.get_table('WIKI/PRICES', ticker=selected,
                        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                        date = { 'gte': start_year, 'lte': end_year}, paginate=True)
# reorganise data pulled by setting date as index with
# columns of tickers and their corresponding adjusted prices
clean = data.set_index('date')
table = clean.pivot(columns='ticker')

# calculate daily and annual returns of the stocks
returns_daily = table.pct_change()
returns_annual = ((1+ returns_daily.mean())**250) - 1

# get daily and covariance of returns of the stock
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250

# empty lists to store returns, volatility and weights of imiginary portfolios
port_returns = []
port_volatility = []
sharpe_ratio = []
stock_weights = []

# set the number of combinations for imaginary portfolios
num_assets = len(selected)
num_portfolios = 500

#set random seed for reproduction's sake
np.random.seed(101)

# populate the empty lists with each portfolios returns,risk and weights
for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns*100)
    port_volatility.append(volatility*100)
    stock_weights.append(weights)

# a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

# extend original dictionary to accomodate each ticker and weight in the portfolio
for counter,symbol in enumerate(selected):
    portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

# make a nice dataframe of the extended dictionary
df = pd.DataFrame(portfolio)

# get better labels for desired arrangement of columns
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected]

# reorder dataframe columns
df = df[column_order]

# plot frontier, max sharpe & min Volatility values with a scatterplot
# find min Volatility & max sharpe values in the dataframe (df)
min_volatility =df['Volatility'].min()
#min_volatility1 = df['Volatility'].min()+1
max_sharpe = df['Sharpe Ratio'].max()
max_return = df['Returns'].max()
max_vol = df['Volatility'].max()
# use the min, max values to locate and create the two special portfolios
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]
max_returns = df.loc[df['Returns'] == max_return]
max_vols = df.loc[df['Volatility'] == max_vol]


# plot frontier, max sharpe & min Volatility values with a scatterplot
plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='green', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='orange', marker='D', s=200 )
plt.scatter(x=max_vols['Volatility'], y=max_returns['Returns'], c='red', marker='D', s=200 )
plt.style.use('seaborn-dark')

plt.xlabel('Volatility (Std. Deviation) Percentage %')
plt.ylabel('Expected Returns Percentage %')
plt.title('Efficient Frontier')
plt.subplots_adjust(bottom=0.4)


# ------------------ Pritning 3 optimal Protfolios -----------------------
#Setting max_X, max_Y to act as relative border for window size

red_num = df.index[df["Returns"] == max_return]
yellow_num = df.index[df['Volatility'] == min_volatility]
green_num = df.index[df['Sharpe Ratio'] == max_sharpe]
multseries = pd.Series([1,1,1]+[100 for stock in selected], index=['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected])
with pd.option_context('display.float_format', '%{:,.2f}'.format):
    plt.figtext(0.2, 0.15, "Max returns Porfolio: \n" + df.loc[red_num[0]].multiply(multseries).to_string(),bbox=dict(facecolor='red', alpha=0.5), fontsize=11, style='oblique',ha='center', va='center', wrap=True)
    plt.figtext(0.45, 0.15, "Safest Portfolio: \n" + df.loc[yellow_num[0]].multiply(multseries).to_string(),bbox=dict(facecolor='yellow', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center', wrap=True)
    plt.figtext(0.7, 0.15, "Sharpe  Portfolio: \n" + df.loc[green_num[0]].multiply(multseries).to_string(),bbox=dict(facecolor='green', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center', wrap=True)


#------------------ Pritning 3 optimal Protfolios -----------------------

##################### ---------------------------------- QUANDL ENDS HERE ----------------------------- ########################

# ---- Image Button ---- #

#
# #plt.savefig ("C:\\Users\\"+getpass.getuser()+"\\Desktop\\figure.png")
# import sys
# import os
# from matplotlib.widgets import Button
#
#
# def image(event):
#     time = datetime.now().strftime('%H.%M.%S')
#     plt.savefig("C:\\Users\\" + getpass.getuser() + "\\Desktop\\Stocks"+str(selected)+"Time"+"["+time+"]"".png")
#
#
# class Index(object):
#     ind = 0
#
#     def next(self, event):
#         """Restarts the current program.
#         #     Note: this function does not return. Any cleanup action (like
#         #     saving data) must be done before calling this function."""
#
#         python = sys.executable
#         os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
#         # os.execl(python, python, * sys.argv)
#
#
# callback = Index()
#
# axnext1 = plt.axes([0.81, 0.2, 0.1, 0.075])
# bnext1 = Button(axnext1, 'Save Image')
# bnext1.on_clicked(image)
#
# #plt.savefig('cover.png')
# plt.show()



# ---- Restart Button ---- #


#plt.savefig ("C:\\Users\\"+getpass.getuser()+"\\Desktop\\figure.png")
import sys
import os
from matplotlib.widgets import Button


def image(event):
    time = datetime.now().strftime('%H.%M.%S')
    plt.savefig('cover.png')


class Index(object):
    ind = 0

    def next(self, event):
        """Restarts the current program.
        #     Note: this function does not return. Any cleanup action (like
        #     saving data) must be done before calling this function."""

        python = sys.executable
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        # os.execl(python, python, * sys.argv)


callback = Index()

axnext1 = plt.axes([0.81, 0.2, 0.1, 0.075])
bnext1 = Button(axnext1, 'Save Image')
bnext1.on_clicked(image)

axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Restart')
bnext.on_clicked(callback.next)



#plt.savefig('cover.png')
plt.show()

