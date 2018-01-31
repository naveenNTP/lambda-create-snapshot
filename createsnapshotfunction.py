import boto3
#credits : originally sourced from Amir Boroumand https://www.linkedin.com/pulse/automated-ebs-snapshots-using-aws-lambda-cloudwatch-amir-boroumand/
#Slight Modification done 
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    result = ec2.describe_volumes( Filters=[
            {'Name': 'tag:lambdasnapshot', 'Values': ['enabled', 'Enabled']}])
    #print 'the result set is  ' + str(result)
    for volume in result['Volumes']:
        print "Backing up %s in %s" % (volume['VolumeId'], volume['AvailabilityZone'])
        result = ec2.create_snapshot(VolumeId=volume['VolumeId'],Description='Created by Lambda function volume-snapshot-create')
        ec2resource = boto3.resource('ec2')
        snapshot = ec2resource.Snapshot(result['SnapshotId'])
        #if 'Tags' in volume:
        for tags in volume['Tags']:
            if tags["Key"] == 'Name':
                volumename = tags["Value"]
                print str(volumename)
                snapshot.create_tags(Tags=[{'Key': 'Name','Value': volumename},{'Key': 'created-by', 'Value': 'lambda_snapshot_create'}])
            #print "Snapshots created id %s " %  snapshot
