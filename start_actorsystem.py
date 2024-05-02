import logging
from thespian.actors import ActorSystem, Actor
import sys

from actors import Ping, RegisterToLeader, RegistrationActor


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
    asys = ActorSystem("multiprocTCPBase", capabilities=capabilities)
    reg = asys.createActor(RegisterToLeader)
    reg = asys.ask(reg, "register")
    ping = asys.createActor(Ping)
    asys.tell(reg, f"register {ping}")
