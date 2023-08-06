#!/usr/bin/env python3

import os, datetime
import easyzip

#9-306M
#4-311M
#1-324M
#0-307M

easyzip.zip(".")

# for i in range(10):
# 	startTime = datetime.datetime.now()
# 	easyzip.zip("/home/noone/.vscode", "code.zip", i, "123456")
# 	endTime = datetime.datetime.now()

# 	fileSize = os.path.getsize('code.zip')
# 	unit = 'B'
# 	if fileSize > 1024:
# 		fileSize = fileSize / 1024
# 		unit = 'KB'
# 	if fileSize > 1024:
# 		fileSize = fileSize / 1024
# 		unit = 'MB'
# 	if fileSize > 1024:
# 		fileSize = fileSize / 1024
# 		unit = 'GB'

# 	print(f'compress level: {i}, file size: {fileSize} {unit}, time: {(endTime - startTime).total_seconds()}')
# 	os.remove("code.zip")

# easyzip.zip("~/Pictures", password = "123456")
