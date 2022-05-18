from api import wrapper
import re

# all of these generate a list of TG targets in a single query.
# NOTHING IS RATE LIMITED YET

client = wrapper.Client("Khronion-Testing API Queries")


def founded():
    """
    Newly founded nations
    :return:
    """
    return client.ns_request(params={'q':'newnations'})['newnations']

def region(target):
    """
    All residents of a region
    :return:
    """

    nations = client.ns_request(params={'region':f'{target}','q':'nations'})['NATIONS'].split(':')

def ejects(region=None):
    """
    Ejected nations

    :param region: region to filter by, otherwise pull all ejects
    :return:
    """

    if region is None:
        events = client.ns_request(params={'q':'happenings', 'filter':'eject'})
    else:
        events = client.ns_request(params={'q':'happenings', 'filter':'eject', 'view':f'region.{region}'})

    nations = []
    for event in events:
        nations.append(re.search('[\w-]+(?=@@ was)', event['text']).group(0))

    return nations

def exits(region):
    """
    All nations leaving a region.

    :param region: Region to check.
    :return:
    """


    events = client.ns_request(params={'q':'happenings', 'filter':'move', 'view':f'region.{region}'})

    nations = []
    for event in events:
        destination = re.search('[\w-]+(?=%%\.)', event['text']).group(0)
        source = re.search('[\w-]+(?=%% to)', event['text']).group(0)
        if source == region and destination != "the_rejected_realms":
            nations.append(re.search('[\w-]+(?=@@ relo)', event['text']).group(0))

    return nations

def entrances(region):
    """
    All nations entering a region.

    :param region: Region to check
    :return:
    """


    events = client.ns_request(params={'q':'happenings', 'filter':'move', 'view':f'region.{region}'})

    nations = []
    for event in events:
        destination = re.search('[\w-]+(?=%%\.)', event['text']).group(0)
        if destination == region:
            nations.append(re.search('[\w-]+(?=@@ relo)', event['text']).group(0))

    return nations

def wa_join(region=None):
    """
    All nations recently admitted to the WA.

    :param region: Region to check, optional
    :return:
    """
    if region is None:
        events = client.ns_request(params={'q':'happenings', 'filter':'member'})
    else:
        events = client.ns_request(params={'q':'happenings', 'filter':'member', 'view':f'region.{region}'})

    nations = []
    for event in events:
        check = re.search('[\w-]+(?=@@ was admitted)', event['text'])
        if check is not None:
            nations.append(check.group(0))

    return nations

def wa_resign(region=None):
    """
    All nations resigning from the WA

    :param region: region to check, optional
    :return:
    """

    if region is None:
        events = client.ns_request(params={'q':'happenings', 'filter':'member'})
    else:
        events = client.ns_request(params={'q':'happenings', 'filter':'member', 'view':f'region.{region}'})

    nations = []
    for event in events:
        check = re.search('[\w-]+(?=@@ resigned)', event['text'])
        if check is not None:
            nations.append(check.group(0))

    return nations

def wa_endorse(nation, region=None):
    """
    All nations endorsing a specified nation

    :param nation: nation that is being endorsed
    :param region: region to filter by, highly recommended unless you don't know where the endorsee is
    :return:
    """
    if region is None:
        events = client.ns_request(params={'q':'happenings', 'filter':'endo'})
    else:
        events = client.ns_request(params={'q':'happenings', 'filter':'endo', 'view':f'region.{region}'})

    nations = []
    for event in events:
        endorser = re.search('[\w-]+(?=@@ en)', event['text'])
        endorsee = re.search('[\w-]+(?=@@\.)', event['text'])

        if endorser is not None and endorsee.group(0) == nation:
            nations.append(endorser.group(0))

    return nations


def wa_unendorse(nation, region=None):
    """
    All nations withdrawing endorsement from a specified nation

    :param nation: nation losing endorsement
    :param region: region to filter by, highly recommended
    :return:
    """
    if region is None:
        events = client.ns_request(params={'q':'happenings', 'filter':'endo'})
    else:
        events = client.ns_request(params={'q':'happenings', 'filter':'endo', 'view':f'region.{region}'})

    nations = []
    for event in events:
        endorser = re.search('[\w-]+(?=@@ wi)', event['text'])
        endorsee = re.search('[\w-]+(?=@@\.)', event['text'])

        if endorser is not None and endorsee.group(0) == nation:
            nations.append(endorser.group(0))

    return nations

def residents(region):
    """
    all residents of a region

    :param region:
    :return:
    """
    return client.ns_request(params={'region': region, 'q': 'nations'})['NATIONS'].split(':')

def wa_delegates():
    """
    WA delegates
    :return:
    """
    return client.ns_request(params={'wa':'1', 'q': 'delegates'})['delegates']

def wa_members():
    """
    WA members
    :return:
    """
    return client.ns_request(params={'wa':'1', 'q': 'members'})['members']

