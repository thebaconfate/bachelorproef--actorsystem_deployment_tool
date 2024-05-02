import logging
from pkg_resources import require
from thespian.actors import (
    Actor,
    ActorSystem,
    ActorSystemConventionUpdate,
    requireCapability,
)
import socket

HOSTNAMES: list[str] = [
    "isabelle",
    "isabelle-b",
    "isabelle-c",
    "isabelle-d",
    "isabelle-e",
    "isabelle-f",
    "isabelle-g",
    "isabelle-h",
    "isabelle-i",
    "isabelle-j",
]


def get_my_ip():
    """Return the ipaddress of the local host"""
    return socket.gethostbyname(socket.gethostname())


class Ping(Actor):
    def receiveMessage(self, msg, sender):
        self.send(sender, f"Ping from {get_my_ip()}")


class RegisterToLeader(Actor):
    def receiveMessage(self, msg, sender):
        reg = self.createActor(RegistrationActor, globalName="registration")
        self.send(sender, reg)


@requireCapability("isabelle")
class RegistrationActor(Actor):
    def __init__(self):
        self.remoteSystems = {}

    def receiveMessage(self, msg, sender):
        if msg == "notifyOnSystemRegistrationChanges":
            self.notifyOnSystemRegistrationChanges()
            logging.info(self.myAddress)
            logging.info("started registereing")
        elif isinstance(msg, ActorSystemConventionUpdate):
            logging.info(self.myAddress)
            logging.info(msg.remoteAdminAddress)
            logging.info(msg=msg.remoteCapabilities)
            logging.info(msg.remoteAdded)
            if msg.remoteAdded:
                for capability in msg.remoteCapabilities:
                    if capability in HOSTNAMES:
                        self.remoteSystems[capability] = None
            elif not msg.remoteAdded:
                for capability in msg.remoteCapabilities:
                    if capability in HOSTNAMES:
                        del self.remoteSystems[capability]
        else:
            logging.info(self.myAddress)
            logging.info(msg)
