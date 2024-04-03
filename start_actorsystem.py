from thespian.actors import ActorSystem, Actor
import sys

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
    ActorSystem("multiprocTCPBase", capabilities=capabilities)