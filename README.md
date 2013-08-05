zpoold
======

zpool autochange disk daemon 

### functionality:
#### base structures:

 ```python
get_zpool_list_h() method returns:

[OrderedDict([('name', 'archive'),
('full_size', '159G'),
('m_size', '1016K'),
('full_size2', '159G'),
('usage', '0%'),
('speed', '1.00x'),
('status', 'ONLINE'),
('other_part',
'-')])]

get_zpool_status("archive") method returns:

OrderedDict([('pool', ['archive']),
('state', ['ONLINE']),
('scan', ['none', 'requested']),
('action', ''),
('see', ''),
('scrub', ''),
('status', ''),
('config',
[[OrderedDict([('name', 'archive'),
('state', 'ONLINE'),
('read', '0'),
('write', '0'),
('cksum', '0')]),
OrderedDict([('name', 'raidz1-0'),
('state', 'ONLINE'),
('read', '0'),
('write', '0'),
('cksum', '0')]),
OrderedDict([('name', 'sda'),
('state', 'ONLINE'),
('read', '0'),
('write', '0'),
('cksum', '0')]),
OrderedDict([('name', 'sdb'),
('state', 'ONLINE'),
('read', '0'),
('write', '0'),
('cksum', '0')]),
OrderedDict([('name', 'sdc'),
('state', 'ONLINE'),
('read', '0'),
('write', '0'),
('cksum', '0')]),
OrderedDict([('name', 'sdd'),
('state', 'ONLINE'), ('read', '0'),
('write', '0'), ('cksum', '0')])]]),
('errors', ['No', 'known', 'data', 'errors', []])])

get_autoreplace() method returns:

[OrderedDict([('name', 'archive'),
('property', 'autoreplace'),
('value', 'off'),
('source', 'default')])]
```
