from cmparser import zpool_status, zpool_autoreplace, zpool_list_h

zpool_list_str = '''
archive 464G    167G    297G    35%     1.00x   ONLINE  -
ssd     69,5G   28,1G   41,4G   40%     1.00x   ONLINE  -
'''

zpool_status_str = '''
pool: archive
 state: ONLINE
  scan: none requested
config:

        NAME                                            STATE     READ WRITE CKSUM
        archive                                         ONLINE       0     0     0
          mirror-0                                      ONLINE       0     0     0
            ata-Hitachi_HUA722050CLA330_JPW9K0J826PUZL  ONLINE       0     0     0
            ata-Hitachi_HUA722050CLA330_JPW9K0J826Y44L  ONLINE       0     0     0
          mirror-1                                      ONLINE       0     0     0
            ata-WDC_WD5003ABYX-01WERA1_WD-WMAYP2901450  ONLINE       0     0     0
            ata-WDC_WD5003ABYX-01WERA1_WD-WMAYP2924234  ONLINE       0     0     0

errors: No known data errors
'''

zpool_autoreplace_str = '''
NAME     PROPERTY     VALUE    SOURCE
archive  autoreplace  on       local    default
tank     autoreplace  on       local    
mgb      not-autoreplace off   local
'''

def zpool_test():
    zl = zpool_list_h()
    zs = zpool_status()
    za = zpool_autoreplace()
    print zl.get_zpool_list_h()
    print zs.get_zpool_status("archive")
    print za.get_autoreplace()



if __name__ == '__main__':
    zpool_test()

