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
        pass
    def onClearSnapshot(self, itemName, itemPos):
        print("Not Update1")
        pass
    def onCommandSecondLevelItemLostUpdates(self, lostUpdates, key):
        print("Not Update2")
        pass
    def onCommandSecondLevelSubscriptionError(self, code, message, key):
        print("Not Update3")
        pass
    def onEndOfSnapshot(self, itemName, itemPos):
        print("Not Update4")
        pass
    def onItemLostUpdates(self, itemName, itemPos, lostUpdates):
        print("Not Update5")
        pass
    def onListenEnd(self, subscription):
        print("Not Update6")
        pass
    def onListenStart(self, subscription):
        print("onListenStart")
        pass
    def onSubscription(self):
        print("subbed successfully")
        pass
    def onSubscriptionError(self, code, message):
        print("onSubscriptionError" + code + "    " + message)
        pass
    def onUnsubscription(self):
        print("Not Update10")
        pass
    def onRealMaxFrequency(self, frequency):
        print("Not Update11")
        pass

class ClientListener:
    def onListenStart(self):
        print("Start listen")
    def onStatusChange(self, status):
        print("Status shit " + status)


if __name__ == "__main__":

    client = LightstreamerClient("https://demo-apd.marketdatasystems.com", "")

    client.connectionDetails.setUser('X49UQ')
    client.connectionDetails.setPassword("CST-3d47a97a7e12616e7e4c0511ed4d2d015c4229d28d2bcf3208caedc9a300acCU01111|XST-cd5f95badc0ca97f3139ad55edbdf952c858106b83792070de32eda37166aaCD01111")

    client.addListener(ClientListener())



    try:
        client.connect()
    except Exception as e:
        print("Unable to connect to Lightstreamer Server")
        print(e)


    sub = Subscription("MERGE",["MARKET:EN.D.LCO.FWS2.IP"],["BID","OFFER"])
    sub.setDataAdapter("QUOTE_ADAPTER")

    sub.addListener(SubListener())


    print("Attempting subscribe")
    client.subscribe(sub)
    print("finished subscribe")

    input(
            "{0:-^80}\n".format(
                "HIT CR TO UNSUBSCRIBE AND DISCONNECT FROM \
        LIGHTSTREAMER"
            )
        )

    client.unsubscribe(sub)
    client.disconnect()

