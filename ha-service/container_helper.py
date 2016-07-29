"""Helper methods for working with containers in config."""

import yaml


def GenerateManifest(context):
  """Generates a Container Manifest given a Template context.

  Args:
    context: Template context, which must contain dockerImage and port
        properties, and an optional dockerEnv property.

  Returns:
    A Container Manifest as a YAML string.
  """
  env_list = []
  if 'dockerEnv' in context.properties:
    for key, value in context.properties['dockerEnv'].iteritems():
      env_list.append({'name': key, 'value': str(value)})

  manifest = {
    
    'apiVersion': 'v1',
    'kind': 'Pod',
    'metadata': {
      # 'name': context.env['name']
      'name': 'wordpress-nginx-ssh'

    },
    'spec': {
      
      'containers': [{
        
        # 'name': context.env['name'],
        'name': 'wordpress-nginx-ssh',
        
        # 'image': context.properties['dockerImage'],
        'image': 'oskarhane/docker-wordpress-nginx-ssh',
        
        'ports': [{
            
            'hostPort': 2222,
            'containerPort': 22
            
          }, {
            
            # 'hostPort': context.properties['port'],
            # 'containerPort': context.properties['port']
            'hostPort': 80,
            'containerPort': 80
            
        }],
        
        'imagePullPolicy': 'Always',
        # 'command': 'nc -p 8080 -l -l -e',
        
        'volumeMounts': [{
          
          'name': 'asia-east1-c-disk-5',
          'mountPath': '/var/www/html'
          
        }]
        
      }]
      
    }
    
  }

  if env_list:
    manifest['spec']['containers'][0]['env'] = env_list

  # We want to return string here, since it _is_ a string.
  return yaml.dump(manifest, default_flow_style=False)
