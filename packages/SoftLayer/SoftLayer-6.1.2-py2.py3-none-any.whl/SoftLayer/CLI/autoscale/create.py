"""Order/Create a scale group."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import exceptions
from SoftLayer.CLI import formatting
from SoftLayer.CLI import helpers
from SoftLayer.managers.autoscale import AutoScaleManager


@click.command()
@click.option('--name', required=True, prompt=True, help="Scale group's name.")
@click.option('--cooldown', required=True, prompt=True, type=click.INT,
              help="The number of seconds this group will wait after lastActionDate before performing another action.")
@click.option('--min', 'minimum', required=True, prompt=True, type=click.INT, help="Set the minimum number of guests")
@click.option('--max', 'maximum', required=True, prompt=True, type=click.INT, help="Set the maximum number of guests")
@click.option('--regional', required=True, prompt=True, type=click.INT,
              help="The identifier of the regional group this scaling group is assigned to.")
@click.option('--postinstall', '-i', help="Post-install script to download")
@click.option('--os', '-o', required=True, prompt=True, help="OS install code. Tip: you can specify <OS>_LATEST")
@click.option('--datacenter', '-d', required=True, prompt=True, help="Datacenter shortname")
@click.option('--hostname', '-H', required=True, prompt=True, help="Host portion of the FQDN")
@click.option('--domain', '-D', required=True, prompt=True, help="Domain portion of the FQDN")
@click.option('--cpu', required=True, prompt=True, type=click.INT,
              help="Number of CPUs for new guests (existing not effected")
@click.option('--memory', required=True, prompt=True, type=click.INT,
              help="RAM in MB or GB for new guests (existing not effected")
@click.option('--policy-relative', required=True, prompt=True,
              help="The type of scale to perform(ABSOLUTE, PERCENT, RELATIVE).")
@click.option('--termination-policy',
              help="The termination policy for the group(CLOSEST_TO_NEXT_CHARGE=1, NEWEST=2, OLDEST=3).")
@click.option('--policy-name', help="Collection of policies for this group. This can be empty.")
@click.option('--policy-amount', help="The number to scale by. This number has different meanings based on type.")
@click.option('--userdata', help="User defined metadata string")
@helpers.multi_option('--key', '-k', help="SSH keys to add to the root user")
@helpers.multi_option('--disk', required=True, prompt=True, help="Disk sizes")
@environment.pass_env
def cli(env, **args):
    """Order/Create a scale group.

    E.g.

    'slcli autoscale create --name test --cooldown 3600 --min 1 --max 2 -o CENTOS_7_64 --datacenter dal10
    --termination-policy 2 -H testvs -D test.com --cpu 2 --memory 1024 --policy-relative absolute
    --policy-name policytest --policy-amount 3 --regional 102 --disk 25 --disk 30 --disk 25'

    """
    scale = AutoScaleManager(env.client)
    network = SoftLayer.NetworkManager(env.client)

    datacenter = network.get_datacenter(args.get('datacenter'))

    ssh_keys = []
    for key in args.get('key'):
        resolver = SoftLayer.SshKeyManager(env.client).resolve_ids
        key_id = helpers.resolve_id(resolver, key, 'SshKey')
        ssh_keys.append(key_id)
    scale_actions = [
        {
            "amount": args['policy_amount'],
            "scaleType": args['policy_relative']
        }
    ]
    policy_template = {
        'name': args['policy_name'],
        'scaleActions': scale_actions

    }
    policies = []
    policies.append(policy_template)
    block = []
    number_disk = 0
    for guest_disk in args['disk']:
        if number_disk == 1:
            number_disk = 2
        disks = {'diskImage': {'capacity': guest_disk}, 'device': number_disk}
        block.append(disks)
        number_disk += 1

    virt_template = {
        'localDiskFlag': False,
        'domain': args['domain'],
        'hostname': args['hostname'],
        'sshKeys': ssh_keys,
        'postInstallScriptUri': args.get('postinstall'),
        'operatingSystemReferenceCode': args['os'],
        'maxMemory': args.get('memory'),
        'datacenter': {'id': datacenter[0]['id']},
        'startCpus': args.get('cpu'),
        'blockDevices': block,
        'hourlyBillingFlag': True,
        'privateNetworkOnlyFlag': False,
        'networkComponents': [{'maxSpeed': 100}],
        'typeId': 1,
        'userData': [{
            'value': args.get('userdata')
        }],
        'networkVlans': [],

    }

    order = {
        'name': args['name'],
        'cooldown': args['cooldown'],
        'maximumMemberCount': args['maximum'],
        'minimumMemberCount': args['minimum'],
        'regionalGroupId': args['regional'],
        'suspendedFlag': False,
        'balancedTerminationFlag': False,
        'virtualGuestMemberTemplate': virt_template,
        'virtualGuestMemberCount': 0,
        'policies': policies,
        'terminationPolicyId': args['termination_policy']
    }

    if not (env.skip_confirmations or formatting.confirm(
            "This action will incur charges on your account. Continue?")):
        raise exceptions.CLIAbort('Aborting scale group order.')

    result = scale.create(order)

    table = formatting.KeyValueTable(['name', 'value'])
    vsi_table = formatting.KeyValueTable(['Id', 'Domain', 'Hostmane'])
    table.align['name'] = 'r'
    table.align['value'] = 'l'
    table.add_row(['Id', result['id']])
    table.add_row(['Created', result['createDate']])
    table.add_row(['Name', result['name']])
    for vsi in result['virtualGuestMembers']:
        vsi_table.add_row([vsi['virtualGuest']['id'], vsi['virtualGuest']['domain'], vsi['virtualGuest']['hostname']])

    table.add_row(['VirtualGuests', vsi_table])
    output = table

    env.fout(output)
