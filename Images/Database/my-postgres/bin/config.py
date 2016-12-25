import os
import subprocess


def StartPostGresServer():
    ChangePriv()
    if os.path.isfile(os.path.join(os.getenv("PGDATA"),"postmaster.pid")):
        print ("Files are exits in " + os.getenv("PGDATA") + " Restart Server")
        RestartMember()
    else:
        print("First time running Start creating database")
        FirstCreation()


def ChangePriv():
    # Postgres Data
    RunCommand("chown -R postgres $PGDATA")
    RunCommand("chmod -R 0700 $PGDATA")

    # Archive
    RunCommand("chown -R postgres:postgres /var/lib/postgresql/archive")
    RunCommand("chmod -R 0700 /var/lib/postgresql/archive")

    # Master File
    RunCommand("chown postgres /master")
    RunCommand("chmod 0700 /master")


def RunRepConfigFile():
    print ("Run RepMgr_Config.sh with the follow Args")
    print ("CLUSTER_NODE_NETWORK_NAME= " + os.getenv("CLUSTER_NODE_NETWORK_NAME") +
           "\n NODE_ID= " + os.getenv("NODE_ID") +
           "\n NODE_NAME= " + os.getenv("NODE_NAME") +
           "\n CLUSTER_NAME= " + os.getenv("CLUSTER_NAME"))
    RunCommand("/usr/local/bin/cluster/repmgr_config.sh")
    print ("Finnish running repmgr_config.sh")


def FirstCreation():
    RunRepConfigFile()

    print ("Node Type " + os.getenv("INITIAL_NODE_TYPE"))
    if os.getenv("INITIAL_NODE_TYPE") == "master":

            print ("Start Master INITIAL First Time")

            while not RunCommand("cat /master").__contains__(os.getenv("CLUSTER_NODE_NETWORK_NAME")):
                print("Write hostname to master file")
                RunCommand("echo \"" + os.getenv("CLUSTER_NODE_NETWORK_NAME") + "\"> /master")

            RunCommand("cp -f /usr/local/bin/cluster/primary.entrypoint.sh /docker-entrypoint-initdb.d/")
            RunCommand("/docker-entrypoint.sh \"postgres\"")
            p = subprocess.Popen("exec gosu postgres \"postgres\"", stdout=subprocess.PIPE, shell=True)

    else:
        print ("Delete files in folder: " + os.getenv("PGDATA"))
        RunCommand("rm -rf " + os.getenv("PGDATA") + "/*")

        print ("Delete files in folder: /var/lib/postgresql/archive")
        RunCommand("rm -rf /var/lib/postgresql/archive/*")


        print ("INITIAL_NODE_TYPE Env: " + os.getenv("INITIAL_NODE_TYPE"))
        if RunCommand("cat /master") == '':
            print ("Primary server not found")
            raise Exception("Primary server not found")
        else:
            os.environ["REPLICATION_PRIMARY_HOST"] = RunCommand("cat /master")

        print ("REPLICATION_PRIMARY_HOST Env: " + os.getenv("REPLICATION_PRIMARY_HOST"))
        print ("Run Wait_DB, Waiting for Master to go up")
        RunCommand(
            "wait_db $REPLICATION_PRIMARY_HOST $REPLICATION_PRIMARY_PORT $REPLICATION_USER $REPLICATION_PASSWORD $REPLICATION_DB")
        p = subprocess.Popen("/usr/local/bin/cluster/standby.entrypoint.sh \"postgres\"", stdout=subprocess.PIPE,
                         shell=True,env=os.environ)


    print ("Run Wait_DB, Waiting for this dataBase")
    print ("CLUSTER_NODE_NETWORK_NAME= " + os.getenv("CLUSTER_NODE_NETWORK_NAME"))
    RunCommand("wait_db $CLUSTER_NODE_NETWORK_NAME $REPLICATION_PRIMARY_PORT $REPLICATION_USER $REPLICATION_PASSWORD $REPLICATION_DB")
    print ("End WaitDB")

    print ("Register to Repmgr as " + os.getenv("INITIAL_NODE_TYPE"))
    RunCommand("gosu postgres repmgr $INITIAL_NODE_TYPE register --force")
    RunCommand("gosu postgres repmgr cluster show")
    RunCommand("rm -rf /tmp/repmgrd.pid")

    print ("Start Repmgr")
    RunCommand("gosu postgres repmgrd -vvv --pid-file=/tmp/repmgrd.pid")


def RunDataBase():
    print ("Start Running database")
    p = subprocess.Popen("exec gosu postgres \"postgres\"", stdout=subprocess.PIPE, shell=True)

    print ("Start WaitDB")
    RunCommand(
        "wait_db $CLUSTER_NODE_NETWORK_NAME $REPLICATION_PRIMARY_PORT $REPLICATION_USER $REPLICATION_PASSWORD $REPLICATION_DB")
    print ("End WaitDB")

    print ("Register to Repmgr as " + os.getenv("INITIAL_NODE_TYPE"))
    RunCommand("gosu postgres repmgr $INITIAL_NODE_TYPE register --force")
    RunCommand("gosu postgres repmgr cluster show")
    RunCommand("rm -rf /tmp/repmgrd.pid")

    print ("Start Repmgr")
    RunCommand("gosu postgres repmgrd -vvv --pid-file=/tmp/repmgrd.pid")


def RestartMember():
    #RunRepConfigFile()

    if RunCommand("cat /master").__contains__(os.environ["CLUSTER_NODE_NETWORK_NAME"]):
        print ("This was the master on shutdown, Start the server like master")
        os.environ["INITIAL_NODE_TYPE"] = "master"
        RunRepConfigFile()
        RunDataBase()

    else:
        os.environ["INITIAL_NODE_TYPE"] = "standby"
        os.environ["REPLICATION_PRIMARY_HOST"] = RunCommand("cat /master")

        FirstCreation()


def RunCommand(command,env=os.environ):
    ## call date command ##
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True,env=env)
    (output, err) = p.communicate()

    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()

    print ("Command output : ", output)

    return output


if __name__ == "__main__":
    StartPostGresServer()
