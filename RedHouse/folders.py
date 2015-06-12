'''
folders.py

Class to hold directories and files for a single directory.

Holds absolute and relative path names.

When the class is created if the designated directory does not exist. It creates it.

Methods:

'''

import os
import re
import threading
import time
import json

class folders(object):
    ''' 
    Contains two sets of folder hierarchies. A remote and a local. IT periodically updates each and makes compares for differences.
    '''

    root = None
    localFiles = None
    fnames = None
    url = None
    updateLocalRate = 5 # update every Nth seconds
    updateRemoteRate = 5 # every Nth time local files are updated update remote 
    totalFiles = 0
    locallyAddedFiles = 0
    locallyDeletedFiles = 0
    locallyUpdatedFiles = 0
    remotelyAddedFiles = 0
    remotelyDeletedFiles = 0    
    remotelyUpdatedFiles = 0    
    
    def __init__(self, root_folder, url):
        '''
        Initialize the class and start the update thread.
        '''
        self.path = root_folder
        self.url = url
        self.UpdateLocalFiles()
        self.UpdateRemoteFolders()
        threading.Thread ( target = self.update).start()
        
    def fileRecord(self, root, name):
        '''
        Store file information so we can update modified files.
        '''
        fileDict = dict()
        try:
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(os.path.join(root, name))
            fileDict['Name'] = name
            fileDict['Created'] = ctime
            fileDict['Modified'] = os.path.getmtime(os.path.join(root, name))
            fileDict['Deleted'] = False
            return fileDict
        except WindowsError:
            return None
        print 'return fail'
        
    def update (self):
        ''' 
        Syncs files periodically.
        '''
        loopCounter = 0
        self.running = True
        while (self.running):
            time.sleep (1)
            loopCounter += 1
            if loopCounter % self.updateLocalRate == 0:
                if loopCounter == self.updateRemoteRate * self.updateLocalRate:
                    '''
                    Update remote first if time.
                    '''
                    print 'update remote'
                    loopCounter = 0
                    self.UpdateRemoteFolders ()
                #Update local folders
                print 'updating local folders'
                self.UpdateLocalFiles()
  
        
    def UpdateLocalFiles (self):
        '''
        Get all the local files folders.
        '''

        #root, dirs, fnames = os.walk(self.path)
        
        if self.localFiles is None:
            '''
            Check for local additions and deletions.
            '''
            self.localFiles = dict()
            for root, localFiles, files in os.walk(self.path, topdown=False):
                #print root
                self.totalFiles += len(files)
                key = root[len(self.path)+1:]
                #print key
                self.localFiles[key] = filter(None, (self.fileRecord(root, name) for name in files))
        else:
            #check for local changes 
            for root, localFiles, files in os.walk(self.path, topdown=False):
                #check for additions
                key = root[len(self.path)+1:]
                if not self.localFiles.has_key(key):
                    self.localFiles[key] = list()
                adds = list()
                for file in files:
                    if not any(file == fileRec['Name'] for fileRec in self.localFiles[key]):
                        print 'Adding file'
                        newfile = self.fileRecord(root, file)
                        if newfile is not None:
                            adds.append (newfile)
                    else:
                        fileRec = next(fileRec for fileRec in self.localFiles[key] if fileRec['Name'] == file)
                        if os.path.getmtime(os.path.join(root, file)) != fileRec['Modified']:
                            fileRec['Modified'] = os.path.getmtime(os.path.join(root, file))
                            print 'Updated file'
                            self.UpdateFile (root, file)
                            self.locallyUpdatedFiles += 1
                self.totalFiles += len(adds)
                self.locallyAddedFiles += len(adds)
                for file in adds:
                    self.localFiles[key].append(file)
                    self.AddFile (key, file)
                #Check for deletions
                deletes = list()
                for file in self.localFiles[key]:
                    if file['Name'] not in files:
                        print 'delete file'
                        deletes.append (file)
                    # else:
                        # print file['Name'],
                        # print ' was found'
                self.locallyDeletedFiles += len(deletes)
                self.totalFiles -= len(deletes)
                for file in deletes:
                    self.localFiles[key].remove(file)
                    self.DeleteFile(root, file)
        
        
    def AddedFolder (self, folderName):
        '''
        Add a newly created folder. 
        '''
        pass
        
        
    def AddFile (self, root,  name):
        '''
        Add a newly created file. 
        '''
        pass
        
    def UpdateFile (self, root,  name):
        '''
        Update a file that has been modified. 
        '''
        pass       
        
    def DeleteFile (self, root,  name):
        '''
        Remove a file that has been deleted locally.
        '''
        pass
        
    def UpdateRemoteFolders (self):
        '''
        Get files on the remote system.
        '''
        print 'Running remote file check'
        
    def stop (self):
        '''
        Stop the server.
        '''
        self.running = False
        
    def GetStatistics (self):
        return self.totalFiles, self.locallyAddedFiles, self.locallyUpdatedFiles, self.locallyDeletedFiles, self.remotelyAddedFiles, self.remotelyDeletedFiles, self.remotelyUpdatedFiles
        
if __name__ == '__main__':
    ''' 
    Temporary testing here. Will move to tests folder soon.
    '''
    f = folders ('C:\Users\dfugelso\Documents\Projects\RedHouse', 'Jacks URL')