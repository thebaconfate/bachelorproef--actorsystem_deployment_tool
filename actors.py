import logging
from thespian.actors import Actor, ActorSystem, ActorSystemConventionUpdate

class RegistrationActor(Actor):


    def receiveMessage(self, msg, sender):
        if msg == "register":
            self.notifyOnSystemRegistrationChanges()
            logging.info("started registereing")
        if isinstance(msg, ActorSystemConventionUpdate):
            logging.info(msg)
        else:
            logging.info(msg)