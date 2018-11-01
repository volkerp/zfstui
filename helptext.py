
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
('type',
"""The type of dataset: filesystem, volume, or snapshot.
"""
)
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



