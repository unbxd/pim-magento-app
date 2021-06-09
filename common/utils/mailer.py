import boto3
from botocore.exceptions import ClientError


def get_ses_client():
    return boto3.client('ses', region_name="AWS_REGION")


def send_email_message(to_address, subject, message):
    try:
        ses_client = get_ses_client()
        ses_client.send_email(
            Destination={
                'ToAddresses': to_address,
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': message,
                },
            },
            Source="",
            # If you are not using a configuration set, comment or delete the
            # following line
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
