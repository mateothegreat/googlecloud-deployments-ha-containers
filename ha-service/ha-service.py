
"""Creates an HA service configuration."""


def GenerateConfig(context):
  """Generates config."""

  lb_name = context.env['deployment'] + '-lb'
  region = context.properties['zones'][0][:-2]
  port = context.properties['port']
  dockerImage = context.properties['dockerImage']
  
  # YAML config.
  config = {'resources': []}
  
  for zone in context.properties['zones']:
    service = {
        'name': context.env['deployment'] + '-service-' + zone,
        'type': 'service.py',
        'properties': {
            'containerSize': context.properties['containerSize'],
            'dockerImage': context.properties['dockerImage'],
            'port': context.properties['port'],
            'targetPool': lb_name + '-tp',
            'zone': zone
        },
        'disks': [{
          'name': 'wordpress-persistent-storage',
          'gcePersistentDisk': {
            # This GCE persistent disk must already exist.
              'pdName': 'disk-3',
              'fsType': 'ext4'
          }
        }]
    }

    config['resources'].append(service)

  lb = {
      'name': lb_name,
      'type': 'lb-l3.py',
      'properties': {
          'port': port,
          'region': region
      }
  }

  config['resources'].append(lb)

  return config

