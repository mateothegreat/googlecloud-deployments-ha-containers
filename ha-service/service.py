
"""Creates autoscaled IGM running specified docker image."""


def GenerateConfig(context):
  """Generate YAML resource configuration."""

  name = context.env['name']
  port = context.properties['port']
  target_pool = context.properties['targetPool']
  zone = context.properties['zone']

  igm_name = name + '-igm'
  it_name = name + '-it'

  it = {
      'name': it_name,
      'type': 'container_instance_template.py',
      'properties': {
          'containerSize': context.properties['containerSize'],
          'containerImage': context.properties['containerImage'],
          'dockerEnv': context.properties['dockerEnv'],
          'dockerImage': context.properties['dockerImage'],
          'port': port
      }
  }

  igm = {
      'name': igm_name,
      'type': 'compute.v1.instanceGroupManager',
      'properties': {
          'baseInstanceName': name + '-instance',
          'instanceTemplate': '$(ref.' + it_name + '.selfLink)',
          'targetSize': context.properties['minSize'],
          'zone': zone
      }
  }

  # Set target pool if one was provided.
  if target_pool:
    igm['properties']['targetPools'] = ['$(ref.' + target_pool + '.selfLink)']

  autoscaler = {
      'name': name + '-as',
      'type': 'compute.v1.autoscaler',
      'properties': {
          'autoscalingPolicy': {
              'minNumReplicas': context.properties['minSize'],
              'maxNumReplicas': context.properties['maxSize']
          },
          'target': '$(ref.' + igm_name + '.selfLink)',
          'zone': zone
      }
  }

  return {
      'resources': [
          it,
          igm,
          autoscaler
      ],
      'outputs': [{
          'name': 'group',
          'value': '$(ref.' + igm_name + '.instanceGroup)'
      }]
  }

