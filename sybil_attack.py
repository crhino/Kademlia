#!/usr/bin/env python
#
# Python script to simulate a Sybil attack on a Kademlia Network


import os, sys, time, signal
import twisted.internet.reactor
from entangled.node import EntangledNode
from entangled.kademlia.datastore import SQLiteDataStore

# The Entangled DHT nodes; instantiated in the main() method
nodes = []

# The Sybil attack nodes, cooperating to comprimise network.
sybils = []

# The key to use for this example when storing/retrieving data
KEY = 'example_key'
# The value to store
VALUE = 'example_value'

def action():
    i=0
    print len(nodes)
    for node in nodes:
        node.printContacts()
    time.sleep(2)

def newNode():
  global port
  dataStore = SQLiteDataStore(dbFile = '/tmp/dbFile%s.db' % port)
  node = EntangledNode (udpPort=port, dataStore=dataStore)
  node.joinNetwork(knownNodes)
  nodes.append(node)
  knownNodes.append(('127.0.0.1', port))
  port+=1


def mainLoop():
  

def stop():
    """ Stops the Twisted reactor, and thus the script """
    print '\nStopping Kademlia node and terminating script...'
    twisted.internet.reactor.stop()

if __name__ == '__main__':
    
    import sys, os
    port = 4000 # Starting UDP port for Kad nodes.
    knownNodes = []

    if len(sys.argv) != 2:
        print 'Usage:\n%s [NUM_NODES]' % sys.argv[0]

    try:
        int(sys.argv[1])
    except ValueError:
        print '\nNUM_NODES must be an integer value.\n'
        sys.exit(1)


    for x in range(0, int(sys.argv[1])):
        if os.path.isfile('/tmp/dbFile%s.db' % port):
            os.remove('/tmp/dbFile%s.db' % port)
        print 'Creating Entangled Node...'
        newNode()    
    twisted.internet.reactor.callLater(2.5, mainLoop)
    # Start the Twisted reactor
    print 'Twisted reactor started (script will commence in 2.5 seconds)'
    twisted.internet.reactor.run()

