
EASY ZIP
====

## What is it?

EASY ZIP is a simple tool to create zip archives. Whatever you zip from file or folder, it will be zipped in a single archive.
You can also create a password protected zip archive.

## How to use it?

### Create a zip archive

```

import easyzip

easyzip.zip('path/to/file/or/folder')

```

#### easyzip.zip(pathWillBeZipped, pathToZipArchive, compressLevel, password)
Like 

```
easyzip.zip('path/to/file/or/folder', 'path/to/zip/archive.zip', compressLevel = 4, password = 'hahahahaha')
```

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

easyzip.unzip('path/to/zip/archive.zip')

```

#### easyzip.unzip(pathToZipArchive, pathToUnzipFolder, password)
Like

```
easyzip.unzip('path/to/zip/archive.zip', 'path/to/unzip/folder', password = 'hahahahaha')
```

##### pathToZipArchive
The path of zip archive.

##### pathToUnzipFolder
The path of folder will be unzipped. If the path does not exist, it will be created. Default use pathToZipArchive base path name.

##### password
The password of zip archive.
