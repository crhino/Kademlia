#!/usr/bin/env python
#
# Python script to simulate a Sybil attack on a Kademlia Network


import os, sys, time, signal
import twisted.internet.reactor
from entangled.node import EntangledNode
from entangled.kademlia.datastore import SQLiteDataStore
from sybil import SybilNode

# The Entangled DHT Sybil node; instantiated in the newNode() method
sybil = None


# Starting port number
port = 5000

# The key to use for this example when storing/retrieving data
KEY = 'example_key'
# The value to store
VALUE = 'example_value'

def print_info():
    sybil.printContacts()
    print '\n\n'


# Function: newNode
# Args: node_list - list of knownNodes
#
# Creates a sybil node.
def newNode(node_list):
    global port
    global sybil
    print 'Creating Entangled Node...'
    if os.path.isfile('/tmp/dbFile%s.db' % port):
        os.remove('/tmp/dbFile%s.db' % port)
    dataStore = SQLiteDataStore(dbFile = '/tmp/dbFile%s.db' % port)
    
    sybil = SybilNode (id=KEY, udpPort=port, dataStore=dataStore)
    #sybil = EntangledNode (id=KEY, udpPort=port, dataStore=dataStore)
    
    sybil.joinNetwork(node_list)


# Taken from entangled examples.
#
# A generic error callback.
def genericErrorCallback(failure):
    """ Callback function that is invoked if an error occurs during any of the DHT operations """
    print 'An error has occurred:', failure.getErrorMessage()
    twisted.internet.reactor.callLater(0, stop)

# Taken from entangled examples.
#
# Does a findVal RPC on the DHT for specified key.
def getValue(key):
    """ Retrieves the value of the specified key (KEY) from the DHT """
    global sybil
    # Get the value for the specified key (immediately returns a Twisted deferred result)
    print '\nRetrieving value from DHT for key "%s"...' % key
    deferredResult = sybil.iterativeFindValue(key)
    # Add a callback to this result; this will be called as soon as the operation has completed
    deferredResult.addCallback(getValueCallback)
    # add the generic error callback
    deferredResult.addErrback(genericErrorCallback)

# Taken from entangled examples.
#
# The findVal RPC passed result to us.
def getValueCallback(result):
    """ Callback function that is invoked when the getValue() operation succeeds """
    # Check if the key was found (result is a dict of format {key: value}) or not (in which case a list of "closest" Kademlia contacts would be returned instead")
    print result
    if type(result) == dict:
        print 'Value successfully retrieved: %s' % result[KEY]
    else:
        print 'Value not found'

# Function: storeVal
# Args: key, val - Both strings.
#
# Stores val in the DHT using the given key.
def storeVal(key, val):
    print "Storing (key,val) pair: (\"%s\", \"%s\")." % (key, val)
    deferredResult = sybil.iterativeStore(key, val)
    deferredResult.addCallback(storeValCallback)
    deferredResult.addErrback(genericErrorCallback)

def storeValCallback(*args, **kwargs):
    print 'Value has been stored in the DHT'


def mainLoop():
    uinput = ''
    while uinput != 'quit':
        uinput = raw_input("> ")
        if uinput == 'store':
          storeVal(KEY, VALUE)
          storeVal('another_key', 'another_value')
        elif uinput == 'get':
          getValue(KEY)
          getValue('another_key')
        elif uinput == 'print':
          print_info()
    stop()


def stop():
    """ Stops the Twisted reactor, and thus the script """
    print '\nStopping Kademlia node and terminating script...'
    twisted.internet.reactor.stop()

if __name__ == '__main__':
    
    import sys, os

    if len(sys.argv) != 2:
        print 'Usage:\n%s [KNOWN_UDP_PORT]' % sys.argv[0]

    try:
        int(sys.argv[1])
    except ValueError:
        print '\nNUM_REG_NODES must be an integer value.\n'
        sys.exit(1)
    
    
    newNode([('127.0.0.1', int(sys.argv[1]))])    
    
    twisted.internet.reactor.callLater(2.5, mainLoop)
    # Start the Twisted reactor
    print 'Twisted reactor started (script will commence in 2.5 seconds)'
    twisted.internet.reactor.run()
