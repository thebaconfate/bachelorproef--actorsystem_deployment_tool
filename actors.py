import logging
from pkg_resources import require
from thespian.actors import (
    Actor,
    ActorSystem,
    ActorSystemConventionUpdate,
    requireCapability,
    ActorAddress,
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
        if isinstance(msg, PingToAddr):
            self.send(msg.addr, f"Ping from {get_my_ip()}")


class SensorActor(Actor):
    def receiveMessage(self, msg, sender):
        if isinstance(msg, PingToAddr):
            self.send(msg.addr, f"SensorActor pings from {get_my_ip()}")


class RegisterRemoteTopLevelActorToLeader:
    def __init__(self, hostname, remoteTopLevelAddress):
        self.hostname = hostname
        self.remoteTopLevelAddress = remoteTopLevelAddress


class RegisterActorToLeader:
    def __init__(self, ActorClass, actorAddress):
        self.ActorClass = ActorClass
        self.actorAddress = actorAddress


class SpawnActor:
    def __init__(self, actorClass) -> None:
        self.actorClass = actorClass


class PingToAddr:
    def __init__(self, addr: ActorAddress) -> None:
        self.addr = addr


class RemoteTopLevelActor(Actor):
    def __init__(self):
        self.registrator = None

    def receiveMessage(self, msg, sender):
        if self.registrator is None and isinstance(
            msg, RegisterRemoteTopLevelActorToLeader
        ):
            self.registrator = self.createActor(
                RegistrationActor, globalName="registration"
            )
            self.send(self.registrator, msg)
        elif isinstance(msg, SpawnActor):
            addr = self.createActor(msg.actorClass)
            self.send(addr, PingToAddr(self.registrator))


@requireCapability("isabelle")
class RegistrationActor(Actor):
    def __init__(self):
        self.remoteSystemCapabilities = {}
        self.remoteSystemTopLevelActors = {}

    def receiveMessage(self, msg, sender):
        if msg == "notifyOnSystemRegistrationChanges":
            self.notifyOnSystemRegistrationChanges()
            logging.info(self.myAddress)
            logging.info("started registereing")
        elif isinstance(msg, ActorSystemConventionUpdate):
            logging.info(self.myAddress)
            logging.info(msg.remoteAdminAddress)
            logging.info(msg=msg.remoteCapabilities)
            if msg.remoteAdded:
                for capability in msg.remoteCapabilities:
                    if capability in HOSTNAMES:
                        self.remoteSystemCapabilities[capability] = msg.remoteCapabilities
            elif not msg.remoteAdded:
                for capability in msg.remoteCapabilities:
                    if capability in HOSTNAMES:
                        del self.remoteSystemCapabilities[capability]
                        del self.remoteSystemTopLevelActors[capability]
        elif isinstance(msg, RegisterRemoteTopLevelActorToLeader):
            hostname = msg.hostname
            if hostname in self.remoteSystemCapabilities.keys():
                self.remoteSystemTopLevelActors[hostname] = msg.remoteTopLevelAddress
                if len(self.remoteSystemTopLevelActors) == len(HOSTNAMES) - 1:
                    logging.info("All remote systems registered")
                    # self.broadcastSpawnAll(Ping)
                    self.broadcastSpawnCapability(SensorActor, "sensor")
        else:
            logging.info(self.myAddress)
            logging.info(msg)

    def broadcastSpawnAll(self, actorClass):
        for address in self.remoteSystemTopLevelActors.values():
            self.send(address, SpawnActor(actorClass))

    def broadcastSpawnCapability(self, actorClass, capability):
        for hostname, capabilities in self.remoteSystemCapabilities.items():
            logging.info(f"{hostname} has capabilities: {capabilities}")
            if capability in capabilities.keys():
                self.send(
                    self.remoteSystemTopLevelActors[hostname], SpawnActor(actorClass)
                )
