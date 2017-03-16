import os
import pandas as pd
from .settings import settings


download_directory = settings().download_directory
local_archive_directory = settings().local_archive_directory
server_archive_directory = settings().server_archive_directory

########################################################
def importExcelSheetDF(filename,sheetname,dirPath,subdirPath=None):

	if '.xlsx' not in filename:
		filename += '.xlsx'

	directory = '/'+dirPath
	if subdirPath != None:
		directory += '/'+subdirPath
	
	### Try Reading from Locally First
	success=False
	fulldir = local_archive_directory+directory+'/'+filename
	data=pd.read_excel(fulldir,sheetname=sheetname,skiprows=1)
	try:
		data=pd.read_excel(fulldir,sheetname=sheetname,skiprows=1)
		success = True
	except IOError:
		### Try Reading from Server Based Directory
		fulldir = server_archive_directory+directory+filename
		try:
			data=pd.read_excel(fulldir,sheetname=sheetname,skiprows=1)
			success = True
		except IOError:
			print 'Cannot Read Excel File  : ',filename
			return None
			
	if success == False:
		return None
	return data

########################################################
def exportPDF(canvas,filename,dirPath,subdirPath=None):

	filename_options=[]
	tempdir='/'+filename+'.pdf'

	directory = '/'+dirPath
	if subdirPath != None:
		directory += '/'+subdirPath

	filename_options.append(tempdir)
	for i in range(4):
		tempdir='/'+filename+'('+str(i+2)+')'+'.pdf'
		filename_options.append(tempdir)

	### Try Saving Locally First
	success=False
	for filename in filename_options:
		fulldir = local_archive_directory+directory+filename
		canvas.__filename = fulldir
		print canvas.__filename
		if success == False:
			try:
				canvas.save()
				success = True
			except IOError:
				continue

	### Try Saving Server if Still Not Saving
	if success == False:
		for filename in filename_options:
			fulldir = server_archive_directory+directory+filename
			canvas.__filename = fulldir
			if success == False:
				try:
					canvas.save()
					success = True
				except IOError:
					continue

	if success == False:
		print 'Error Trying to Save PDF File : ',filename
		return False
	return True

########################################################
def importDF(filename,dirPath,subdirPath=None):

	if '.csv' not in filename:
		filename += '.csv'

	directory = '/'+dirPath
	if subdirPath != None:
		directory += '/'+subdirPath

	### Try Reading from Locally First
	success=False
	fulldir = local_archive_directory+directory+'/'+filename
	try:
		data = pd.read_csv(fulldir)
		success = True
	except IOError:
		### Try Reading from Server Based Directory
		fulldir = server_archive_directory+directory+'/'+filename
		print fulldir
		try:
			data = pd.read_csv(fulldir)
			success = True
		except IOError:
			print 'Cannot Read CSV File  : ',filename

	if success == False:
		return None
	return data


########################################################
def exportDF(data,filename,dirPath,subdirPath=None):

	directory = '/'+dirPath
	if subdirPath != None:
		directory += '/'+subdirPath

	filename_options=[]
	tempdir='/'+filename+'.csv'
	filename_options.append(tempdir)
	for i in range(4):
		tempdir='/'+filename+'('+str(i+2)+')'+'.csv'
		filename_options.append(tempdir)

	### Try Saving Locally First
	success=False
	for filename in filename_options:
		fulldir = local_archive_directory+directory+filename
		if success == False:
			try:
				data.to_csv(fulldir)
				success = True
			except IOError:
				continue

	### Try Saving Server if Still Not Saving
	if success == False:
		for filename in filename_options:
			fulldir = server_archive_directory+directory+filename
			if success == False:
				try:
					data.to_csv(fulldir)
					success = True
				except IOError:
					continue

	if success == False:
		print 'Error Trying to Save File : ',filename
		return False
	return True