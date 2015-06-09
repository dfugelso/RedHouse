
import pytest
import time
import os

@pytest.fixture(scope='module')
def daemon (request):
    import tray
    import folders
    global f
    if os.path.isfile('output.txt'):
        os.remove('output.txt')
    if not os.path.isfile('output2.txt'):
        with open('output2.txt', 'w') as p:
            p.write('Hi there!')
    f = folders.folders('C:\Users\dfugelso\Documents\Projects\RedHouse', 'Jacks URL')
    def resource_teardown():
        f.stop()
    request.addfinalizer(resource_teardown)    
    return f


def testAdd(daemon):
    
    totalfiles1, b, c, d, e = daemon.GetStatistics()
    print totalfiles1, b, c, d, e
    assert totalfiles1 > 0
    with open('output.txt', 'w') as p:
        p.write('Hi there!')
    assert os.path.isfile('output.txt')
    time.sleep(6)
    totalfiles2, b, c, d, e = daemon.GetStatistics()   
    print totalfiles1, b, c, d, e
    assert totalfiles1 < totalfiles2
    os.remove('output.txt')
    assert not os.path.isfile('output.txt')   

def testDelete(daemon):
    time.sleep(6)
    totalfiles1, b, c, d, e = daemon.GetStatistics()
    assert os.path.isfile('output2.txt')
    os.remove('output2.txt')
    time.sleep(6)
    totalfiles2, b, c, d, e = daemon.GetStatistics() 
    assert totalfiles1 > totalfiles2
    with open('output2.txt', 'w') as p:
        p.write('Hi there!')

def test_remote_add():
    pass
