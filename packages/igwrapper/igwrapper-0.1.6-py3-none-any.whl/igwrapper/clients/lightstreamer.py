from lightstreamer_client import *
from time import sleep

class SubListener:
    def onItemUpdate(self, update):
        print("Update")
        print(update.getItemName())
        print(update.getFields())
        print("UPDATE " + update.getValue("BID") + " " + update.getValue("OFFER"))
    def onListenStart(self, aSub):
        print("Update")

    def onClearSnapshot(self, itemName, itemPos):
        print("Not Update1")

    def onCommandSecondLevelItemLostUpdates(self, lostUpdates, key):
        print("Not Update2")

    def onCommandSecondLevelSubscriptionError(self, code, message, key):
        print("Not Update3")

    def onEndOfSnapshot(self, itemName, itemPos):
        print("Not Update4")

    def onItemLostUpdates(self, itemName, itemPos, lostUpdates):
        print("Not Update5")

    def onListenEnd(self, subscription):
        print("Not Update6")

    def onListenStart(self, subscription):
        print(f"onListenStart: {subscription}")

    def onSubscription(self):
        print("subbed successfully")

    def onSubscriptionError(self, code, message):
        print("onSubscriptionError" + code + "    " + message)

    def onUnsubscription(self):
        print("Not Update10")

    def onRealMaxFrequency(self, frequency):
        print("Not Update11")


class ClientListener:
    def onListenStart(self):
        print("Start listen")
    def onStatusChange(self, status):
        print("Client Status: " + status)

def onItemUpdate(update):
    print("onItemUpdate")
    print(update.getItemName())
    print(update.getFields())
    print("UPDATE " + update.getValue("BID") + " " + update.getValue("OFFER"))

def onSubscription():
    print("Subscribed")

def onUnsubscription():
    print("Unsubbed")

def onSubscriptionError(code, msg):
    print("Sub Error")
    print('subscription failure: ' + code + " message: " + msg)

def onItemUpdate(update):
    print("Update")
    print(update.getItemName())
    print(update.getFields())
    print("UPDATE " + update.getValue("BID") + " " + update.getValue("OFFER"))
def onListenStart(aSub):
    print(f"Starting sub listen {aSub}")



if __name__ == "__main__":

    client = LightstreamerClient(serverAddress="https://demo-apd.marketdatasystems.com/", adapterSet=None)

    client.connectionDetails.setUser('X49UQ')
    client.connectionDetails.setPassword("CST-55f772e4c002a943fbeabc41a88a11e0430428ba16de67bdcc40f06d337cefCU01112|XST-9726e1ce324817d7c34ee83b79bf41876bed29c36e0920a512ed79f414145bCD01112")

    client.addListener(ClientListener())

    print(f'server: {client.connectionDetails.getServerAddress()}')
    print(f'user: {client.connectionDetails.getUser()}')


    try:
        client.connect()
    except Exception as e:
        print("Unable to connect to Lightstreamer Server")
        print(e)


    sub = Subscription("MERGE",["MARKET:OP.D.SPXWED.3900C.IP"],["BID","OFFER"])
    # sub.setDataAdapter("QUOTE_ADAPTER")

    # sub.addListener(SubListener())
    sub.addListener()


    print("Attempting subscribe")
    client.subscribe(sub)
    print("finished subscribe")

    input(
            "{0:-^80}\n".format(
                "HIT ENTER TO UNSUBSCRIBE AND DISCONNECT FROM LIGHTSTREAMER"
            )
        )

    client.unsubscribe(sub)
    client.disconnect()

