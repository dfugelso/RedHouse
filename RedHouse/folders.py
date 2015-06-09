'''
folders.py

Class to hold directories and files for a single directory.

Holds absolute and relative path names.

When the class is created if the designated directory does not exist. It creates it.

Methods:

__init__
Compare
AddFile
AddDirectory
CreateDirectory

'''

import os
import re
import threading
import time


class folder (object):
    '''
    Contains a file list, name and the subdirectories for a single folder.
    '''
    
    def __init__(self, parent, name, files, subdirs):
        this.name = name
        this.files = files
        this.subdirs = subdirs
    

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
    remotelyAddedFiles = 0
    remotelyDeletedFiles = 0    
    
    
    def __init__(self, root_folder, url):
        '''
        Initialize the class and start the update thread.
        '''
        self.path = root_folder
        self.url = url
        self.UpdateLocalFiles()
        self.UpdateRemoteFolders()
        threading.Thread ( target = self.update).start()
        
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
                self.localFiles[key] = files
            #for key in self.localFiles.keys():
                #print key, self.localFiles[key]
            #print '.git\\refs'
            #print self.localFiles['.git\\refs']
        else:
            #check for local changes 
            for root, localFiles, files in os.walk(self.path, topdown=False):
                #check for additions
                key = root[len(self.path)+1:]
                adds = list()
                for file in files:
                    if file not in self.localFiles[key]: 
                        print 'Adding file'
                        adds.append (file)
                self.totalFiles += len(adds)
                self.locallyAddedFiles += len(adds)
                for file in adds:
                    self.localFiles[key].append(file)
                #Check for deletions
                deletes = list()
                for file in self.localFiles[key]:
                    if file not in files:
                        print 'delete file'
                        deletes.append (file)
                self.locallyDeletedFiles += len(deletes)
                self.totalFiles -= len(deletes)
                for files in deletes:
                    self.localFiles[key].remove(file)
                        
        
        
    def AddedFolder (self, folderName):
        '''
        Add a newly created folder. 
        '''
        pass
        
        
    def AddedFile (self, folderName):
        '''
        Add a newly created file. 
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
        return self.totalFiles, self.locallyAddedFiles, self.locallyDeletedFiles, self.remotelyAddedFiles, self.remotelyDeletedFiles
        
if __name__ == '__main__':
    ''' 
    Temporary testing here. Will move to tests folder soon.
    '''
    f = folders ('C:\Users\dfugelso\Documents\Projects\RedHouse', 'Jacks URL')