import re

from Products.ZenRRD.CommandParser \
    import CommandParser
from Products.ZenUtils.Utils \
    import prepId

class status(CommandParser):

    def processResults(self, cmd, result):
        """
        Example healthy output:
        all pools are healthy

        Alt. example healthy output:
        pool 'pool1' is healthy

        Example unhealthy output:
          pool: zpool3
         state: DEGRADED
        status: One or more devices has been removed by the administrator.
            Sufficient replicas exist for the pool to continue functioning in a
            degraded state.
        action: Online the device using 'zpool online' or replace the device with
            'zpool replace'.
          scan: resilvered 856G in 22h23m with 0 errors on Thu Jul  7 17:26:46 2016
        config:

            NAME                                           STATE     READ WRITE CKSUM
            zpool3                                         DEGRADED 0     0     0
              raidz2-0                                     DEGRADED 0     0     0
                ata-ST2000LM007-1R8174_WCC08SPQ            REMOVED 0     0     0
                ata-ST2000LM003_HN-M201RAD_S362J9CH186029  ONLINE 0     0     0
                ata-ST2000LM003_HN-M201RAD_S34RJ9AG212597  ONLINE 0     0     0
                ata-ST2000LM003_HN-M201RAD_S34RJ9AG212657  ONLINE 0     0     0
            logs
              ata-ACSC2M064S25_986012880052                ONLINE 0     0     0

        errors: No known data errors 
        """
        pool_regex = r'^ state: (\w+)\s*?$'
        device_regex = r'^\s+\S+\s+(\S+)\s+.*'

        # Convert pool state to number for monitoring template
        # An event transform will have to make this human-readable again
        health_map = {
            'ONLINE': 0,
            'AVAIL': 0,
            'DEGRADED': 1,
            'FAULTED': 2,
            'OFFLINE': 3,
            'UNAVAIL': 4,
            'REMOVED': 5,
        }

        values = dict()
        for line in cmd.result.output.splitlines():
            if line.endswith('healthy'):
                values['health'] = 0
                break
            else:
                # Most of the time, the pool's probably going to be healthy
                # so no need to check the regexes unless it isn't
                pool_match = re.match(pool_regex, line)
                device_match = re.match(device_regex, line)

                if pool_match or device_match:
                    health = pool_match.groups()[0]
                    values['health'] = health_map.get(health)
                    break

        for point in cmd.points:
            if point.id in values:
                result.values.append((point, values[point.id]))