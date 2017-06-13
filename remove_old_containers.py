#!/usr/bin/python

import boto3
from collections import namedtuple
#before you shoul auth in ecr $(aws ecr --login)
REGION='change it'
REPO='change it'
REGISTRY='change it'



def delete_containers(data, cli):
    counter = 0
    for d in data:
        counter += 1
        if counter > 4:
            cli.batch_delete_image(
                 registryId=REGISTRY,
                 repositoryName=REPO,
                 imageIds=[
                    {
                        'imageDigest': d.imageDigest
                    }
                 ]
            )
            print "deleted " + d.imageDigest + " pushed date: " + str(d.imagePushedAt)


def get_list(cli):
    response = cli.describe_images(
      registryId=REGISTRY,
      repositoryName=REPO,
      filter={
        'tagStatus': 'UNTAGGED'
      }
    )
    data = []
    for e in response[u'imageDetails']:
        data.append(namedtuple('image', e.keys())(*e.values()))
    data.sort(key=lambda x: x.imagePushedAt, reverse=True)
    return data


def rem():
    cli = boto3.client('ecr', region_name=REGION)
    data = get_list(cli)
    delete_containers(data, cli)

rem()
