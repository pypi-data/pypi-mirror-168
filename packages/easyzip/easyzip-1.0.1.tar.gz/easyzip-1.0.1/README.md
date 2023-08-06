
EASY ZIP
====

## What is it?

EASY ZIP is a simple tool to create zip archives. Whatever you zip from file or folder, it will be zipped in a single archive.
You can also create a password protected zip archive.

## How to use it?

### Create a zip archive

```

import easyzip

easyzip.zip('path/to/file/or/folder', 'path/to/zip/archive.zip', compressLevel = 4, password = 'hahahahaha')

```

#### easyzip.zip(pathWillBeZipped, pathToZipArchive, compressLevel, password)
##### pathWillBeZipped
The path of file or folder will be zipped.

##### pathToZipArchive
The path of zip archive. If the path does not exist, it will be created. The name of zip archive default use pathWillBeZipped base path name.

##### compressLevel
The compress level of zip archive. The default value is 4.

##### password
The password of zip archive. If the password is not None, the zip archive will be password protected.

### Unzip a zip archive

```

import easyzip

easyzip.unzip('path/to/zip/archive.zip', 'path/to/unzip/folder', password = 'hahahahaha')

```

#### easyzip.unzip(pathToZipArchive, pathToUnzipFolder, password)

##### pathToZipArchive
The path of zip archive.

##### pathToUnzipFolder
The path of folder will be unzipped. If the path does not exist, it will be created.

##### password
The password of zip archive.
