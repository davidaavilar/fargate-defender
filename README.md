# Convert a unprotected task to a protected task Definition (Fargate)

_This script help you to convert a YAML AWS CloudFormation with a Fargate Task Definition into a protected TaskDefinition with Prisma Cloud App-Embedded Defender for Fargate_

_The script will find the resource with "AWS::ECS::TaskDefinition" in the Cloudformation_

### Pre-requisitos 📋

_1. The script will ask for a YAML file name you have in the folder that you are running the script_

_2. You have to udpate your Defender parameters. You can find them in the Console:
tokenConsole = 'tokenConsole'
wssConsole = 'wss://us-east1.cloud.twistlock.com:443'
defenderImage = 'registry-auth.twistlock.com/tw_nondnxtmsu000lamye1y93szu8khcfhl/twistlock/defender:defender_21_04_421'_

### Output 🔧

_The output will put a new filename ending with "protected"_

