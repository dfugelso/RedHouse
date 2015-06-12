def fileRecord( file):
    '''
    Store file information so we can update modified files.
    '''
    fileDict = dict()
    try:
        fileDict['Name'] = file

        return fileDict
    except WindowsError:
        return None
        
        
l = ('a', 'b', 'c', 'd')

q = (fileRecord(c) for c in l)

if any('a' is d['Name'] for d in q):
    print 'Yolo'
else:
    print 'Nolo'
    
if any('q' in d for d in q):
    print 'Yolo'
else:
    print 'Nolo'