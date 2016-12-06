import os
import subprocess


def StartPostGresServer():
    PGDATA = os.getenv("PGDATA")
    print ("PGDATA = " + PGDATA)
    ChangePriv()
    if os.path.isfile(os.path.join(PGDATA,"postmaster.pid")):
        print ("Restart Server")
        RestartMember(PGDATA)
    else:
        print("Start FirstCreation")
        FirstCreation(PGDATA)


def ChangePriv():
    RunCommand("chown -R postgres $PGDATA")
    RunCommand("chmod -R 0700 $PGDATA")
    RunCommand("chown postgres /master")
    RunCommand("chmod 0700 /master")


def FirstCreation(PGDATA):
    RunCommand("/usr/local/bin/cluster/repmgr_config.sh")

    print ("Node Type " + os.getenv("INITIAL_NODE_TYPE"))

    if os.getenv("INITIAL_NODE_TYPE") == "master":
        print ("Start Master INITIAL")
        RunCommand("echo " + os.getenv("CLUSTER_NODE_NETWORK_NAME") + "> /master")
        RunCommand("cp -f /usr/local/bin/cluster/primary.entrypoint.sh /docker-entrypoint-initdb.d/")
        RunCommand("/docker-entrypoint.sh \"postgres\"")
        #p = subprocess.Popen("/docker-entrypoint.sh \"postgres\" &", stdout=subprocess.PIPE, shell=True)
        p = subprocess.Popen("exec gosu postgres \"postgres\"", stdout=subprocess.PIPE, shell=True)

    else:
        #p = subprocess.Popen("/usr/local/bin/cluster/standby.entrypoint.sh \"postgres\" &", stdout=subprocess.PIPE, shell=True)
        print ("Delete files in folder: " + PGDATA)
        RunCommand("rm -rf " + PGDATA + "/*")
        print ("INITIAL_NODE_TYPE Env: " + os.getenv("INITIAL_NODE_TYPE"))
        print ("REPLICATION_PRIMARY_HOST Env: " + os.getenv("REPLICATION_PRIMARY_HOST"))
        p = subprocess.Popen("/usr/local/bin/cluster/standby.entrypoint.sh \"postgres\" &", stdout=subprocess.PIPE,
                         shell=True,env=os.environ)

    print ("Start WaitDB")
    RunCommand("wait_db $CLUSTER_NODE_NETWORK_NAME $REPLICATION_PRIMARY_PORT $REPLICATION_USER $REPLICATION_PASSWORD $REPLICATION_DB")
    print ("End WaitDB")

    print ("Register to Repmgr as " + os.getenv("INITIAL_NODE_TYPE"))
    RunCommand("gosu postgres repmgr $INITIAL_NODE_TYPE register --force")
    RunCommand("gosu postgres repmgr cluster show")
    RunCommand("rm -rf /tmp/repmgrd.pid")

    print ("Start Repmgr")
    RunCommand("gosu postgres repmgrd -vvv --pid-file=/tmp/repmgrd.pid")

    #RunCommand("echo FirstCreation > $PGDATA/status")

    print ("communicate")
    (output, err) = p.communicate()
    print ("wait")
    p_status = p.wait()

def RestartMember(PGDATA):
    #DOTO: Need to work here understand the cluster picture
    os.environ["INITIAL_NODE_TYPE"] = "standby"
    os.environ["REPLICATION_PRIMARY_HOST"] = RunCommand("cat /master")
    # RunCommand("tempPrimaryHost=`cat /master`")
    # RunCommand("REPLICATION_PRIMARY_HOST=$tempPrimaryHost")
    FirstCreation(PGDATA)
    print("Exit for now")


def RunCommand(command,env=os.environ):
    ## call date command ##
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True,env=env)
    (output, err) = p.communicate()

    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()

    print ("Command output : ", output)
    print ("Command exit status/return code : ", p_status)

    return output

if __name__ == "__main__":
    StartPostGresServer()
