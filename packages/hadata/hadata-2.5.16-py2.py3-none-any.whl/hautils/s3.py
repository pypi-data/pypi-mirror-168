import logging
import os
import traceback

import boto3
from botocore.exceptions import ClientError

from dotenv import load_dotenv

from hautils.missconfig import MissingConfiguration
from hautils.logger import logger
from hautils.slack import slack_notify

load_dotenv(override=False)

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if ACCESS_KEY is None or SECRET_KEY is None:
    raise MissingConfiguration


def get_s3_client():
    logger.info("getting s3 client");
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='ap-southeast-1')
    return s3_client


def upload_file(file_obj, object_name=None):
    logger.info("uploading a file to s3 bucket %s" % (S3_BUCKET_NAME,))
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_obj
    try:
        s3_client = get_s3_client()
        logger.debug("uploading file %s " % f"{object_name}")
        result = s3_client.upload_fileobj(file_obj, S3_BUCKET_NAME, f"{object_name}")
        logger.debug("error upload %s " % (result,))
        return True
    except Exception as e:
        slack_notify("error uploading to s3 %s " % (traceback.format_exception(type(e), e, e.__traceback__)))
        logger.error(e)
        logger.debug(traceback.format_exception(type(e), e, e.__traceback__))

    raise Exception()



def upload_file_2(file_obj, object_name=None):
    # If S3 object_name was not specified, use file_name
    s3_client = get_s3_client()
    if object_name is None:
        object_name = file_obj
    try:
        s3_client.upload_file(file_obj, S3_BUCKET_NAME, f"{object_name}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_file(file_obj):
    logger.info("deleting a file from s3 %s " % (file_obj,))
    try:
        s3 = get_s3_client()
        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=file_obj)
        return True
    except Exception as ex:
        print(str(ex))
        return False


def create_presigned_url(object_name, expiration):
    logger.info("creating a pre signed url for object")
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': S3_BUCKET_NAME,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response


def download_file(bucket, local_file, s3_file):
    logger.info("downloading from s3")
    client = get_s3_client()
    client.download_file(bucket, s3_file, local_file)
    logger.info("Download Successful of remote file %s to local file %s" % (s3_file, local_file))
    return True