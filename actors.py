import logging
from thespian.actors import Actor, ActorSystem, ActorSystemConventionUpdate, requireCapability
import socket

def get_my_ip():
    """Return the ipaddress of the local host"""
    return socket.gethostbyname(socket.gethostname())

@requireCapability("sensor")
class Ping(Actor):

    def receiveMessage(self, msg, sender):
        self.send(sender, f"Ping from {get_my_ip()}")

class RegistrationActor(Actor):


    def receiveMessage(self, msg, sender):
        if msg == "register":
            self.notifyOnSystemRegistrationChanges()
            logging.info("started registereing")
        if isinstance(msg, ActorSystemConventionUpdate):
            logging.info(msg.remoteAdminAddress)
            logging.info(msg=msg.remoteCapabilities)
            logging.info(msg.remoteAdded)
            if msg.remoteAdded and msg.remoteCapabilities.get('isabelle-b'):
                remote_actor = self.createActor(Ping, {"isabelle-b": True})
                self.send(remote_actor, "Ping")
        else:
            logging.info(msg)