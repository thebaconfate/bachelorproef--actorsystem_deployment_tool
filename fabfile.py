from fabric import Connection, task
from time import sleep

hostnames = [
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
path = "cd bachelorproef/bachelorproef--actorsystem_deployment_tool"


@task
def deploy(c):
    open("pingpong.log", "w").close()
    result = c.run("hostname")
    c.run("tmux new-session -d 'python3 main.py 1900 \"isabelle\"'", pty=False)
    sleep(2)
    for hostname in hostnames:
        connection = Connection(hostname)
        with connection.prefix(path):
            result = connection.run("hostname")
            capabilities = f'"{hostname}, sensor"'
            connection.run(
                f"tmux new-session -d 'python3 start_actorsystem.py 1900 {capabilities}'",
                pty=False,
            )


@task
def retract(c):
    for hostname in hostnames:
        connection = Connection(hostname)
        with connection.prefix(path):
            connection.run("python3 stop_actorsystem.py 1900", pty=False)
            connection.run(f'echo "closed {hostname}"')
    hostname = c.run("hostname", hide=True).stdout.strip()
    c.run("tmux new-session -d 'python3 stop_actorsystem.py 1900'", pty=False)
    c.run(f'echo "closed {hostname}"')
