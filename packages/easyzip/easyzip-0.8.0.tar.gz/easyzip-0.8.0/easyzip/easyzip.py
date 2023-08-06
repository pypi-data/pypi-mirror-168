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

def zip(inputPath, outputFile, compressLevel = 9, password = None):
	print('compressing')
	filePathDictList = getAllFileInPath(inputPath)
	
	srcFileNameList = []
	pathInDstZip = []

	for filePathDict in filePathDictList:
		print(filePathDict)
		srcFileNameList.append(filePathDict['filePath'])
		pathInDstZip.append(filePathDict['path'])

	pyminizip.compress_multiple(srcFileNameList, pathInDstZip, outputFile, password, compressLevel)
	print(f'compressdone output: {outputFile}')

