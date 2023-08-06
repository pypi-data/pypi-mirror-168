#!/usr/bin/env python3

import pyminizip, os

def getAllFileInPath(inputPath):
	result = []

	if os.path.exists(inputPath) == False:
		raise Exception('path or file is not exist')

	if os.path.isfile(inputPath):
		result.append({
			"fname": os.path.basename(inputPath),
			"path": os.path.dirname(inputPath),
			"filePath": inputPath
		})
		return result

	if inputPath[-1] != '/':
		inputPath += '/'

	for fname in os.listdir(inputPath):
		filePath = inputPath + fname
		if os.path.isdir(filePath):
			result.extend(getAllFileInPath(filePath))
			continue
		if os.path.isfile(filePath):
			result.append({
				"fname": fname,
				"path": inputPath[:-1],
				"filePath": filePath
			})

	return result

def zip(inputPath, outputFile = None, compressLevel = 4, password = None):
	print('compressing')

	inputPath = os.path.expanduser(inputPath)
	inputPath = os.path.abspath(inputPath)

	if outputFile == None:
		outputFile = os.path.basename(inputPath) + '.zip'

	if os.path.exists(inputPath) == False:
		raise Exception('path or file is not exist')

	filePathDictList = getAllFileInPath(inputPath)
	
	srcFileNameList = []
	pathInDstZip = []

	for filePathDict in filePathDictList:
		print(filePathDict)
		srcFileNameList.append(filePathDict['filePath'])
		pathInDstZip.append(filePathDict['path'])

	pyminizip.compress_multiple(srcFileNameList, pathInDstZip, outputFile, password, compressLevel)
	print(f'compressdone output: {outputFile}')

def unzip(inputFile, outputPath, password = None):
	print('uncompressing')
	isExist = os.path.exists(outputPath)
	if isExist == False:
		os.makedirs(outputPath)
	pyminizip.uncompress(inputFile, password, outputPath, 0)
	print(f'uncompressdone output: {outputPath}')
