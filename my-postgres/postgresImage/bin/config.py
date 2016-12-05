import os
import requests
import subprocess


def StartPostGresServer():
    PGDATA = os.getenv("PGDATA")

    if os.listdir(PGDATA).__len__() != 0 and os.path.isfile(os.path.join(PGDATA,"status")):
        ChangePriv(PGDATA)
        print ("Restart Server")
        RestartMember(PGDATA)
    else:
        FirstCreation(PGDATA)


def ChangePriv(PGDATA):
    RunCommand("chown -R postgres $PGDATA")
    RunCommand("chmod -R 0700 $PGDATA")


def FirstCreation(PGDATA):
    RunCommand("/usr/local/bin/cluster/repmgr_configure.sh")

    if os.getenv("INITIAL_NODE_TYPE") == "master":
        RunCommand("cp -f /usr/local/bin/cluster/primary.entrypoint.sh /docker-entrypoint-initdb.d/ /docker-entrypoint.sh postgres &")
    else:
        RunCommand("/usr/local/bin/cluster/standby.entrypoint.sh postgres &")

    print ("Register to Repmgr as " + os.getenv("INITIAL_NODE_TYPE"))
    RunCommand("gosu postgres repmgr $INITIAL_NODE_TYPE register --force")
    RunCommand("gosu postgres repmgr cluster show")
    RunCommand("rm -rf /tmp/repmgrd.pid")
    print ("Start Repmgr")
    RunCommand("gosu postgres repmgrd -vvv --pid-file=/tmp/repmgrd.pid")

    RunCommand("echo FirstCreation > $PGDATA/status")


def RestartMember(PGDATA):
    print ("Find Status for cluster")
    output = RunCommand("gosu postgres repmgr cluster show")

    #DOTO: Need to work here understand the cluster picture
    os.environ["INITIAL_NODE_TYPE"] = "standby"
    for line in output.splitlines():
        if not line.__contains__("FAILED"):
            os.environ["REPLICATION_PRIMARY_HOST"] = line.split(" host=")[1].split(" dbname=")
            FirstCreation(PGDATA)
    print("Exit for now")


def RunCommand(command):
    ## call date command ##
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()

    print "Command output : ", output
    print "Command exit status/return code : ", p_status

    return output

if __name__ == "__main__":
    StartPostGresServer()