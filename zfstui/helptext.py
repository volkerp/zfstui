
texts = [
('available',
"""The  amount  of  space  available to the dataset and all 
its children, assuming that there is no other activity in the pool.
Because space is shared within a pool, availability can be 
limited by any number of factors, including  physical pool size,
quotas, reservations, or other datasets within the pool.

This property can also be referred to by its shortened column name, avail.
"""),
('compressratio',
"""For  non-snapshots, the compression ratio achieved for the used space
of this dataset, expressed as a multiplier. The used property
includes descendant datasets, and, for clones, does not include 
the space shared with the  origin  snapshot. 
For snapshots, the compressratio is the same as the refcompressratio
property. Compression can be turned on by running: 
zfs set compression=on dataset. The default value is off.
"""),
('creation',
"""The time this dataset was created.
"""),
('clones',
"""For snapshots, this property is a comma-separated list of filesystems 
or volumes which are clones of this snapshot.
The clones' origin property is this snapshot.  If the clones property 
is not empty, then this snapshot can not be destroyed (even with 
the -r or -f options).
"""),
(
'defer_destroy',
"""This  property is on if the snapshot has been marked for deferred destruction 
by using the zfs destroy -d command. Otherwise, the property is off.
"""),
(
'filesystem_count',
"""The total number of filesystems and volumes that exist under this location 
in the dataset tree. This value is only available when a filesystem_limit 
has been set somewhere in the tree under which the dataset resides.
"""),
(
'logicalreferenced',
"""The amount of space that is "logically" accessible by this dataset. 
See the referenced property. The logical space ignores the effect of the 
compression and copies properties, giving a quantity closer to the amount 
of data that applications see. However, it does include space consumed by 
metadata.

This property can also be referred to by its shortened column name, lrefer.
"""),
(
'logicalused',
"""The amount of space that is "logically" consumed by this dataset and all its 
descendents. See the used property. The logical space ignores the effect of
the compression and copies properties, giving a quantity closer to the 
amount of data that applications see. However, it does include space consumed
by metadata.

This property can also be referred to by its shortened column name, lused.
"""),
(
'mounted',
"""For file systems, indicates whether the file system is currently mounted.
This property can be either yes or no.
"""),
(
'origin',
"""For cloned file systems or volumes, the snapshot from which the clone 
was created. See also the clones property.
"""),
(
'referenced',
"""The amount of data that is accessible by this dataset, 
which may or may not be shared with other datasets in the pool.
When  a  snapshot or clone is created, it initially references the same 
amount of space as the file system or snapshot it was created from, 
since its contents are identical.

This property can also be referred to by its shortened column name, refer.
"""),
(
'refcompressratio',
"""The compression ratio achieved for the referenced space of this dataset, 
expressed as a multiplier. See also the compressratio property.
"""),
(
'snapshot_count',
"""The total number of snapshots that exist under this location in the 
dataset tree.  This value is only available when a snapshot_limit has 
been set somewhere in the tree under which the dataset resides.
"""),
(
'type',
"""The type of dataset: filesystem, volume, or snapshot.
"""),
(
'used',
"""The  amount  of  space  consumed  by  this  dataset  and  all its 
descendents. This is the value that is checked against this dataset's
quota and reservation. The space used does not include this dataset's 
reservation, but does take into  account the reservations of any 
descendent datasets. The amount of space that a dataset consumes 
from its parent, as well as the amount of space that are freed if 
this dataset is recursively destroyed, is the greater of its space
used and its reservation.

When snapshots (see the "Snapshots" section) are created, their space
is initially shared between the snapshot and the file system, and possibly
with previous snapshots. As the file system changes, space that was 
previously shared becomes unique to the snapshot, and counted in the 
snapshot's space used. Additionally, deleting snapshots can increase 
the amount of space unique to (and used by) other snapshots.

The amount of space used, available, or referenced does not take into
account pending changes. Pending changes are generally accounted for
within a few seconds. Committing a change to a disk using fsync(2) 
or O_SYNC  does not necessarily guarantee that the space usage information
is updated immediately.
"""),
(
'usedby*',
"""The usedby* properties decompose the used properties into the various
reasons that space is used. Specifically, 
used = used‐ bychildren + usedbydataset + usedbyrefreservation +,
usedbysnapshots. These properties are only available for datasets created 
on zpool "version 13" pools.
"""),
(
'usedbychildren',
"""The amount of space used by children of this dataset, which would be freed
if all the dataset's children were destroyed.
"""),
(
'usedbydataset',
"""The amount of space used by this dataset itself, which would be freed
if the dataset were destroyed (after first removing any refreservation and
destroying any necessary snapshots or descendents).
"""),
(
'usedbyrefreservation',
"""The amount of space used by a refreservation set on this dataset, 
which would be freed if the refreservation was removed.
"""),
(
'usedbysnapshots',
"""The amount of space consumed by snapshots of this dataset. 
In particular, it is the amount of space that would be freed if all of this
dataset's snapshots were destroyed. Note that this is not simply the sum 
of the snapshots' used properties because space can be shared by 
multiple snapshots.
"""),
(
'userused@user',
"""The amount of space consumed by the specified user in this dataset. 
Space is charged to the owner of each file, as displayed by ls -l. 
The amount of space charged is displayed by du and ls -s. See the zfs 
userspace subcommand for more information.

Unprivileged users can access only their own space usage. The root user, 
or a user who has been granted the userused privilege with zfs allow, 
can access everyone's usage.

The userused@... properties are not displayed by zfs get all. The user's 
name must be appended after the @ symbol, using one of the following forms:

           o      POSIX name (for example, joe)

           o      POSIX numeric ID (for example, 789)

           o      SID name (for example, joe.smith@mydomain)

           o      SID numeric ID (for example, S-1-123-456-789)
"""),
(
'userrefs',
"""This property is set to the number of user holds on this snapshot.
User holds are set by using the zfs hold command.
"""),
(
'groupused@group',
"""The amount of space consumed by the specified group in this dataset.
Space is charged to the group of each file, as displayed by ls -l. 
See the userused@user property for more information.

Unprivileged users can only access their own groups' space usage. 
The root user, or a user who has been granted the groupused privilege 
with zfs allow, can access all groups' usage.
"""),
(
'volblocksize=blocksize',
"""For  volumes, specifies the block size of the volume. The blocksize
cannot be changed once the volume has been written, so it should be set
at volume creation time. The default blocksize for volumes is 8 Kbytes. 
Any power of 2 from 512 bytes to 128 Kbytes is valid.

This property can also be referred to by its shortened column name, volblock.
"""),
(
'written',
"""The amount of referenced space written to this dataset since the 
previous snapshot.
"""),
(
'written@snapshot',
"""The amount of referenced space written to this dataset since the 
specified snapshot. This is the space that is referenced by this dataset
but was not referenced by the specified snapshot.

The snapshot may be specified as a short snapshot name (just the part
after the @), in which case it will be interpreted as a snapshot in the same
filesystem as this dataset. The snapshot be a full snapshot name 
(filesystem@snapshot), which for clones may be a snapshot in the origin's
filesystem (or the origin of the origin's filesystem, etc).
""")
]


pooltexts = [
(
'available',
"""Amount of storage available within the pool. 
This property can also be referred to by its shortened column name "avail".
"""),
(
'capacity',
"""Percentage of pool space used. 
This property can also be referred to by its shortened column name, "cap".
"""),
(
'expandsize',
"""Amount of uninitialized space within the pool or device that can be used 
to increase the total capacity of the pool. Uninitialized  space  consists 
of any space on an EFI labeled vdev which has not been brought online (i.e.
zpool online -e). This space occurs when a LUN is dynamically expanded.
"""),
(
'fragmentation',
"""The amount of fragmentation in the pool.
"""),
(
'free',
"""The amount of free space available in the pool.
"""),
(
'freeing',
"""After a file system or snapshot is destroyed, the space it was using 
is returned to the pool asynchronously. freeing is the amount of space remaining
to be reclaimed. Over time freeing will decrease while free increases.
"""),
(
'health',
"""The current health of the pool. Health can be "ONLINE", "DEGRADED", 
"FAULTED", " OFFLINE", "REMOVED", or "UNAVAIL".
"""),
(
'guid',
"""A unique identifier for the pool.
"""),
(
'size',
"""Total size of the storage pool.
"""),
(
'unsupported@feature_guid',
"""Information about unsupported features that are enabled on the pool. 
See zpool-features(5) for details.
"""),
(
'used',
"""Amount of storage space used within the pool.
The space usage properties report actual physical space available to the 
storage pool. The physical space can be different from the total amount 
of space that any contained datasets can actually use. The amount of space
used in a raidz configuration depends on the  characteristics of the data 
being written. In addition, ZFS reserves some space for internal accounting 
that the zfs(8) command takes into account, but the zpool command does not. 
For non-full pools of a reasonable size, these effects should be invisible. 
For small pools, or pools that are close to being completely full, 
these discrepancies may become more noticeable.
""")
]


def gen_help():
    out = []
    index = {}
    lineno = 0
    for key, text in texts:
        index[key] = lineno
        out.append(key)
        out.append('')
        lineno += 2
        for line in text.split('\n'):
            out.append('    ' + line)
            lineno += 1

    return out, index


fulltext, index = gen_help()



