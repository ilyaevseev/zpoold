from cmparser import zpool_status

ztest = '''
  pool: tank
 state: UNAVAIL
status: One or more devices are faulted in response to IO failures.
action: Make sure the affected devices are connected, then run 'zpool clear'.
   see: http://www.sun.com/msg/ZFS-8000-HC
 scrub: scrub completed after 0h0m with 0 errors on Tue Sep  1 09:51:01 2009
config:

        NAME        STATE     READ WRITE CKSUM
        tank        UNAVAIL      0     0     0  insufficient replicas
          c1t0d0    ONLINE       0     0     0
          c1t1d0    UNAVAIL      4     1     0  cannot open

errors: Permanent errors have been detected in the following files: 

/tank/data/aaa
/tank/data/bbb
/tank/data/ccc
'''

def zpool_test():
    z = zpool_status()
    z.get_zpool_status('name', ztest)
if __name__ == '__main__':
    zpool_test()

