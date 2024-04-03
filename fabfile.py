from fabric import Connection, task

hostnames = ['isabelle-b', 'isabelle-c', 'isabelle-d', 'isabelle-e', 'isabelle-f', 'isabelle-g', 'isabelle-h', 'isabelle-i', 'isabelle-j']

@task
def deploy(c):
    result = c.run('hostname')
    print(result)
    for hostname in hostnames:
        with Connection(hostname) as conn:
            result = conn.run(f'hostname')
            print(result)