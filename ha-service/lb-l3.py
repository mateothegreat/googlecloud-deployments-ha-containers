
"""Generates configuration for a network load balancer."""


def GenerateConfig(context):
  """Generates config."""

  prefix = context.env['name']

  hc_name = prefix + '-hc'
  tp_name = prefix + '-tp'
  fr_name = prefix + '-fr'

  port = context.properties['port']
  region = context.properties['region']

  resources = [{
      'name': hc_name,
      'type': 'compute.v1.httpHealthCheck',
      'properties': {
          'port': port,
          'requestPath': '/'
      }
  }, {
      'name': tp_name,
      'type': 'compute.v1.targetPool',
      'properties': {
          'region': region,
          'healthChecks': ['$(ref.' + hc_name + '.selfLink)']
      }
  }, {
      'name': fr_name,
      'type': 'compute.v1.forwardingRule',
      'properties': {
          'region': region,
          'portRange': port,
          'target': '$(ref.' + tp_name + '.selfLink)'
      }
  }]

  return {'resources': resources}
