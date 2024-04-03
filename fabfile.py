from fabric import Connection, task

hostnames = ['isabelle-b', 'isabelle-c', 'isabelle-d', 'isabelle-e', 'isabelle-f', 'isabelle-g', 'isabelle-h', 'isabelle-i', 'isabelle-j']
path = "cd bachelorproef/bachelorproef--actorsystem_deployment_tool"

@task
def deploy(c):
    result = c.run('hostname')
    print(result)
    for hostname in hostnames:
        connection = Connection(hostname)
        with connection.prefix(path):
            result = connection.run("hostname")
            connection.run("tmux new-session -d 'python3 start_actorsystem.py 1900'", pty=False)

@task
def retract(c):
    for hostname in hostnames:
        connection = Connection(hostname)
        with connection.prefix(path):
            connection.run("hostname")
            connection.run("python3 stop_actorsystem.py 1900")