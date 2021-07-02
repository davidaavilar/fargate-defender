import json
import requests
import os
import yaml
import sys

# Global Parameters

inputFile = input('Your unprotected yaml filename (ie. "myfile.yaml": ')
if not inputFile:
	unprotected_fn = 'myTask_template.yaml'
	fn = unprotected_fn.split('.')[0]
else:
	unprotected_fn = inputFile
	fn = inputFile.split('.')[0]

protected_fn = fn + '-protected.yaml'

def convertTask():
	
	myyaml = ''
	with open(unprotected_fn, 'rb') as f:
		my_yaml = yaml.load(f, Loader=yaml.FullLoader)
		my_yaml.update({'AWSTemplateFormatVersion': '2010-09-09'})
	my_json_yaml = my_yaml
	for x, v in my_json_yaml['Resources'].items():
		if v['Type'] == 'AWS::ECS::TaskDefinition':

			# Get Variables

			family = v['Properties']['Family']
			cds = v['Properties']['ContainerDefinitions']
			cd = cds[0]
			cdName = cd['Name']
			cdImage = cd['Image']

			# Defender Update Current ContainerDefinition Entrypoint
			var = '/var/lib/twistlock/fargate/fargate_defender.sh'
			fargate = 'fargate'
			e = 'entrypoint'

			# Defender Update Current ContainerDefinition
			update_task = {"DependsOn":[{"Condition":"START","ContainerName":"TwistlockDefender"}],"Environment":[{"Name":"TW_IMAGE_NAME","Value":cdImage},{"Name":"TW_CONTAINER_NAME","Value":cdName},{"Name":"DEFENDER_TYPE","Value":"fargate"},{"Name":"FARGATE_TASK","Value":family}],"LinuxParameters":{"Capabilities":{"Add":["SYS_PTRACE"]}},"VolumesFrom":[{"ReadOnly":"false","SourceContainer":"TwistlockDefender"}]}
			
			# Add Defender CotainerDefinition
			defender = {"Name":"TwistlockDefender","EntryPoint":["/usr/local/bin/defender","fargate","sidecar"],"Essential":"true","Environment":[{"Name":"INSTALL_BUNDLE","Value":"eyJzZWNyZXRzIjp7InNlcnZpY2UtcGFyYW1ldGVyIjoiMWxoamdndVZtNVlzbEVXMG5rMG01TkI1ZmtaMWNpMWt3cUZrRnhJSFM0c0Z5SmpIc1JNaDNmWUozY3ZnVzlvQWswci94MTV3czdtUXY5SkRGVkhobUE9PSJ9LCJnbG9iYWxQcm94eU9wdCI6eyJodHRwUHJveHkiOiIiLCJub1Byb3h5IjoiIiwiY2EiOiIiLCJ1c2VyIjoiIiwicGFzc3dvcmQiOnsiZW5jcnlwdGVkIjoiIn19LCJjdXN0b21lcklEIjoidXMtMi0xNTgyOTA2MTQiLCJhcGlLZXkiOiJLQlBnUzhra2wzZUowS1hrM3lKa2d0SjFrbnJwSUhSTWFSbXVTblZLWmpvakdJMGMzVkhmdVdKb2swdzVUMC94ZUpZNWt2VHRPZko2cEVmZWN1a3QvQT09IiwibWljcm9zZWdDb21wYXRpYmxlIjpmYWxzZX0="},{"Name":"DEFENDER_TYPE","Value":"fargate"},{"Name":"FARGATE_TASK","Value":family},{"Name":"WS_ADDRESS","Value":"wss://us-east1.cloud.twistlock.com:443"}],"Image":"registry-auth.twistlock.com/tw_nondnxtmsu000lamye1y93szu8khcfhl/twistlock/defender:defender_21_04_421"}

			cd.update(update_task)
			ep = cd['EntryPoint']
			ep.insert(0,e)
			ep.insert(0,fargate)
			ep.insert(0,var)
			cds.append(defender)
	
	protected_file = open('%s' % protected_fn, 'w')
	yaml.dump(my_json_yaml, protected_file, default_flow_style=False)

convertTask()


