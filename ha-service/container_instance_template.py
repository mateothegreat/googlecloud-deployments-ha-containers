
"""Creates a Container VM with the provided Container manifest."""

from container_helper import GenerateManifest


def GenerateConfig(context):
    """Generates config."""
    
    image = ''.join(['https://www.googleapis.com/compute/v1/','projects/google-containers/global/images/',context.properties['containerImage']])
    default_network = ''.join(['https://www.googleapis.com/compute/v1/projects/',context.env['project'], '/global/networks/default'])
    
    instance_template = {
        
        'name': context.env['name'],
        'type': 'compute.v1.instanceTemplate',
        
        'properties': {
            
            'properties': {
                
                'metadata': {
                    
                    'items': [{
                        
                        'key': 'google-container-manifest',
                        'value': GenerateManifest(context)
                        
                    }]
                    
                },
                
                'machineType': 'g1-small',
                
                'disks': [{
                    
                    'deviceName': 'boot',
                    'boot': True,
                    'autoDelete': True,
                    'mode': 'READ_WRITE',
                    'type': 'PERSISTENT',
                    
                    'initializeParams': {
                        
                        'sourceImage': image
                        
                    }
                    
                }
                # {
                # #   "kind": "compute#attachedDisk",
                # #   "index": 1,
                #   "type": "PERSISTENT",
                #   "mode": "READ_WRITE",
                #   "source": "asia-east1-c-disk-5",
                #   "deviceName": "asia-east1-c-disk-5",
                #   "boot": False,
                #   "autoDelete": False
                # #   "interface": "SCSI"
                # }
                
                ],
                
                'networkInterfaces': [{
                    
                    'accessConfigs': [{
                        
                        'name': 'external-nat',
                        'type': 'ONE_TO_ONE_NAT'
                        
                    }],
                    
                    'network': default_network
                    
                }]
                
            }
            
        }
        
    }
    
    return {'resources': [instance_template]}