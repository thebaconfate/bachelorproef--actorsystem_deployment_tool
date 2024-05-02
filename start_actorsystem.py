from thespian.actors import ActorSystem
import sys

from actors import (
    Ping,
    RegisterRemoteTopLevelActorToLeader,
    RemoteTopLevelActor,
)


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
    reg = asys.createActor(RemoteTopLevelActor)
    asys.tell(reg, RegisterRemoteTopLevelActorToLeader(capability_names[0], reg))
