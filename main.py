import logging
from thespian.actors import Actor, ActorSystem, ActorSystemConventionUpdate
import sys

from actors import RegistrationActor
logcfg = {
    "version": 1,
    "formatters": {"normal": {"format": "%(levelname)-8s %(message)s"}},
    "handlers": {
        "h": {
            "class": "logging.FileHandler",
            "filename": "pingpong.log",
            "formatter": "normal",
            "level": logging.INFO,
        }
    },
    "loggers": {"": {"handlers": ["h"], "level": logging.DEBUG}},
}




if __name__ == "__main__":
    portnum = int(sys.argv[1])
    capability_names = (sys.argv + [""])[2].split(", ")
    capabilities = dict(
        [
            ("Admin Port", portnum),
            ("Convention Address.IPv4", ("isabelle", 1900)),
        ]
        + list(zip(capability_names, [True] * len(capability_names)))
    )
    asys : ActorSystem = ActorSystem("multiprocTCPBase",logDefs=logcfg, capabilities=capabilities)
    reg = asys.createActor(RegistrationActor)
    asys.tell(reg, "register")
    