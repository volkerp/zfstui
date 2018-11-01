import subprocess
import sys



def zfsListDatasets():
    cmd = ["zfs", "list", "-r", "-o", "name,used,avail,refer,type"]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def zfsListVolumes():
    cmd = ["zfs", "list", "-t", "volume", "-r", "-o", "name,volsize,used,avail,refer,ratio,reserv"]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def zfsListFilesystems():
    cmd = ["zfs", "list", "-t", "filesystem", "-r", "-o", "name,used,avail,refer,ratio,quota,reserv,mountpoint"]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def zfsListSnapshots():
    cmd = ["zfs", "list", "-r", "-o", "name,used,creation,compressratio,referenced,written", "-t", "snap"]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    return stdout.splitlines()


def zfsListSnapshotsOf(dataset):
    cmd = ["zfs", "list", "-r", "-o", "name,creation,used,compressratio,referenced,written", "-t", "snap", dataset]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    return stdout.splitlines()


def zfsListPools():
    cmd = ["zpool", "list", "-o", "name,size,alloc,free,cap,frag,dedup,health"]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def zfsPoolProperties(poolname):
    cmd = ["zpool", "get", "all", poolname]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def zfsPoolHistory(poolname):
    cmd = ["zpool", "history", poolname]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def zfsPoolIostat(poolname):
    cmd = ["zpool", "iostat", "-v", poolname]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()



def zfsDatasetProperties(datasetname):
    cmd = ["zfs", "get", "all", datasetname]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def zfsSnapshotProperties(snapshotname):
    cmd = ["zfs", "get", "all", snapshotname]
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    
    return stdout.splitlines()


def check_zfs_executables():
    try:
        cmd = ["/sbin/zpool", "list"]
        stdout = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
    except FileNotFoundError as e:
        sys.exit("zpool command not found in path")
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)
    
    try:
        cmd = ["/sbin/zfs", "list"]
        stdout = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
    except FileNotFoundError as e:
        sys.exit("zfs command not found in path")
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)
