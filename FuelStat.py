from tkinter import *
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('fuelLog.db')
c = conn.cursor()

root = Tk()
root.title("Fuel Stats")
root.option_add('*tearOff', FALSE)

logMiles = StringVar()
logGallons = StringVar()
logCost = StringVar()
tripMPG = StringVar()
tripCostPerMile = StringVar()
tripMiles = StringVar()
tripMPGPercentile = StringVar()
autoMilesTotal = StringVar()
autoMilesTracked = StringVar()
autoGallonsTracked = StringVar()
autoMPGTracked = StringVar()
autoExtGallons = StringVar()
autoCostTracked = StringVar()
autoExtCost = StringVar()
autoAvgCost = StringVar()

def submit():
	milesIn = logMiles.get()
	gallonsIn = logGallons.get()
	costIn = logCost.get()
	c.execute('SELECT id FROM fuelLog ORDER BY id DESC;')
	idTup = c.fetchone()
	if idTup:
		idIn = float(idTup[0]) + 1
	else:
		idIn = 1
	newLog = (idIn, milesIn, gallonsIn, costIn)
	c.execute('INSERT INTO fuelLog VALUES(?,?,?,?)', newLog)
	updateTrip(milesIn, gallonsIn, costIn)
	updateAuto()
	logMiles.set('')
	logGallons.set('')
	logCost.set('')

def updateTrip(mi, ga, co):
	c.execute('SELECT miles FROM fuelLog ORDER BY miles DESC;')
	milesThis = c.fetchone()
	print (milesThis)
	milesLast = c.fetchone()
	print (milesLast)
	if milesLast:
		newMiles = float(milesThis[0]) - float(milesLast[0])
	else:
		newMiles = float(milesThis[0])
	tripMiles.set(newMiles)
	MPG = float(mi) / float(ga)
	tripMPG.set(MPG)
	CPM = (float(co) * float(ga)) / float(mi)
	tripCostPerMile.set(CPM)
	conn.commit()


def updateAuto():
	c.execute('SELECT miles FROM fuelLog ORDER BY miles DESC;')
	greatestMilesTup = c.fetchone()
	if greatestMilesTup:
		greatestMilesFlo = float(greatestMilesTup[0])
	else:
		greatestMilesFlo = 0
	autoMilesTotal.set("{0:.2f}".format(greatestMilesFlo))
	
	c.execute('SELECT miles FROM fuelLog ORDER BY miles ASC;')
	leastMilesTup = c.fetchone()
	if leastMilesTup:
		leastMilesFlo = float(leastMilesTup[0])
	else:
		leastMilesFlo = 0
	milesTracked = greatestMilesFlo - leastMilesFlo
	autoMilesTracked.set("{0:.2f}".format(milesTracked))

	c.execute('SELECT gallons FROM fuelLog')
	gal = c.fetchall()
	galSum = 0
	for element in gal:
		galSum += element[0]
	autoGallonsTracked.set("{0:.2f}".format(galSum))

	mpg = milesTracked / galSum
	autoMPGTracked.set("{0:.2f}".format(mpg))

	extGal = (1 / mpg) * greatestMilesFlo
	autoExtGallons.set("{0:.2f}".format(extGal))

	c.execute('SELECT cost, gallons FROM fuelLog')
	cost = c.fetchall()
	costGalSum = 0
	for element in cost:
		costGalSum += element[0] * element[1]
	autoCostTracked.set("{0:.2f}".format(costGalSum))

	avgCost = costGalSum/galSum
	autoAvgCost.set("{0:.2f}".format(avgCost))
	
	setAvgCost = avgCost * greatestMilesFlo / mpg
	autoExtCost.set("{0:.2f}".format(setAvgCost))


mainFrame = ttk.Frame(root, padding="5 5 5 5")
logFrame = ttk.Labelframe(mainFrame, text='Log New Refill')
tripFrame = ttk.Labelframe(mainFrame, text='Trip Stats')
autoFrame = ttk.Labelframe(mainFrame, text='Automobile Stats')

#win = Toplevel(root)
#menubar = Menu(win)
#win['menu'] = menubar
#menu_file = Menu(menubar)
#menu_file.add_command(label='New', command=newFile)
#menu_file.add_command(label='Open', command=openFile)
#menu_file.add_command(label='Save', command=saveFile)

logMilesLabel = ttk.Label(logFrame, text='Current Odometer Reading')
logMilesEdit = ttk.Entry(logFrame, textvariable=logMiles)
logGallonsLabel = ttk.Label(logFrame, text='Gallons of Fuel Added')
logGallonsEdit = ttk.Entry(logFrame, textvariable=logGallons)
logCostLabel = ttk.Label(logFrame, text='Cost Per Gallon')
logCostEdit = ttk.Entry(logFrame, textvariable=logCost)
logSubmitButton = ttk.Button(logFrame, text='Submit', command=submit)

tripMilesLabel = ttk.Label(tripFrame, text='Miles Traveled')
tripMilesEdit = ttk.Entry(tripFrame, textvariable=tripMiles)
tripMPGLabel = ttk.Label(tripFrame, text='MPG')
tripMPGEdit = ttk.Entry(tripFrame, textvariable=tripMPG)
tripCostPerMileLabel = ttk.Label(tripFrame, text='Cost Per Mile')
tripCostPerMileEdit = ttk.Entry(tripFrame, textvariable=tripCostPerMile)
tripMPGPercentileLabel = ttk.Label(tripFrame, text='MPG Percentile')
tripMPGPercentileEdit = ttk.Entry(tripFrame, textvariable=tripMPGPercentile)

autoMilesTotalLabel = ttk.Label(autoFrame, text='Total Mileage Traveled')
autoMilesTotalEdit = ttk.Entry(autoFrame, textvariable=autoMilesTotal)
autoMilesTrackedLabel = ttk.Label(autoFrame, text='Mileage Tracked')
autoMilesTrackedEdit = ttk.Entry(autoFrame, textvariable=autoMilesTracked)
autoGallonsTrackedLabel = ttk.Label(autoFrame, text='Gallons Tracked')
autoGallonsTrackedEdit = ttk.Entry(autoFrame, textvariable=autoGallonsTracked)
autoMPGTrackedLabel = ttk.Label(autoFrame, text='MPG Tracked')
autoMPGTrackedEdit = ttk.Entry(autoFrame, textvariable=autoMPGTracked)
autoExtGallonsLabel = ttk.Label(autoFrame, text='Extrapolated Gallons Consumed')
autoExtGallonsEdit = ttk.Entry(autoFrame, textvariable=autoExtGallons)
autoCostTrackedLabel = ttk.Label(autoFrame, text='Fuel Cost Tracked')
autoCostTrackedEdit = ttk.Entry(autoFrame, textvariable=autoCostTracked)
autoAvgCostLabel = ttk.Label(autoFrame, text='Average Cost Per Gallon')
autoAvgCostEdit = ttk.Entry(autoFrame, textvariable=autoAvgCost)
autoExtCostLabel = ttk.Label(autoFrame, text='Extrapolated Fuel Cost')
autoExtCostEdit = ttk.Entry(autoFrame, textvariable=autoExtCost)

mainFrame.grid(column=0, row=0)
logFrame.grid(column=0, row=5, columnspan=5, rowspan=20, sticky=(N, S))
tripFrame.grid(column=5, row=5, columnspan=5, rowspan=20, sticky=(N, S))
autoFrame.grid(column=10, row=5, columnspan=5, rowspan=20, sticky=(N, S))
logMilesLabel.grid(column=0, row=5)
logMilesEdit.grid(column=1, row=5)
logGallonsLabel.grid(column=0, row=6)
logGallonsEdit.grid(column=1, row=6)
logCostLabel.grid(column=0, row=7)
logCostEdit.grid(column=1, row=7)
logSubmitButton.grid(column=1, row=24, sticky=(E))
tripMilesLabel.grid(column=5, row=5)
tripMilesEdit.grid(column=6, row=5)
tripMPGLabel.grid(column=5, row=6)
tripMPGEdit.grid(column=6, row=6)
tripCostPerMileLabel.grid(column=5, row=7)
tripCostPerMileEdit.grid(column=6, row=7)
tripMPGPercentileLabel.grid(column=5, row=8)
tripMPGPercentileEdit.grid(column=6, row=8)
autoMilesTotalLabel.grid(column=10, row=5)
autoMilesTotalEdit.grid(column=11, row=5)
autoMilesTrackedLabel.grid(column=10, row=6)
autoMilesTrackedEdit.grid(column=11, row=6)
autoGallonsTrackedLabel.grid(column=10, row=7)
autoGallonsTrackedEdit.grid(column=11, row=7)
autoExtGallonsLabel.grid(column=10, row=8)
autoExtGallonsEdit.grid(column=11, row=8)
autoMPGTrackedLabel.grid(column=10, row=9)
autoMPGTrackedEdit.grid(column=11, row=9)
autoCostTrackedLabel.grid(column=10, row=10)
autoCostTrackedEdit.grid(column=11, row=10)
autoAvgCostLabel.grid(column=10, row=11)
autoAvgCostEdit.grid(column=11, row=11)
autoExtCostLabel.grid(column=10, row=12)
autoExtCostEdit.grid(column=11, row=12)

updateAuto()
root.mainloop()



 