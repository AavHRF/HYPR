from api import wrapper
import re

# This file contains a set of methods that can be used to identify campaign
# targets for commonly used scenarios. Each returns a list of nation names.


def founded(client: wrapper.Client) -> list:
    """
    Gets a list of recently founded nations.

    :param client: initialized client object that can be used to make API queries.
    :return: list of nation names
    """
    return client.ns_request(params={'q': 'newnations'})['newnations']


def residents(client: wrapper.Client, region: str) -> list:
    """
    Get list of all resident nations in a region

    :param client: initialized client object that can be used to make API queries.
    :param region: name of region
    :return: list of nation names
    """
    return client.ns_request(params={'region': region, 'q': 'nations'})['NATIONS'].split(':')


def ejects(client: wrapper.Client, region: str = None) -> list:
    """
    Gets a list of recently ejected nations

    :param client: initialized client object that can be used to make API queries.
    :param region: name of region to check for ejections; if not specified, will get all ejected nations
    :return: list of nation names
    """

    if region is None:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'eject'})
    else:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'eject', 'view': f'region.{region}'})

    nations = []
    for event in events:
        nations.append(re.search(r'[\w-]+(?=@@ was)', event['text']).group(0))

    return nations


def exits(client: wrapper.Client, region: str) -> list:
    """
    Gets a list of all nations leaving a region.

    :param client: initialized client object that can be used to make API queries.
    :param region: name of region to check for exiting nations.
    :return: list of nation names
    """

    events = client.ns_request(params={'q': 'happenings', 'filter': 'move', 'view': f'region.{region}'})

    nations = []
    for event in events:
        destination = re.search(r'[\w-]+(?=%%\.)', event['text']).group(0)
        source = re.search(r'[\w-]+(?=%% to)', event['text']).group(0)
        if source == region and destination != "the_rejected_realms":
            nations.append(re.search(r'[\w-]+(?=@@ relo)', event['text']).group(0))

    return nations


def entrances(client: wrapper.Client, region: str) -> list:
    """
    Gets a list of all nations entering a region.

    :param client: initialized client object that can be used to make API queries.
    :param region: name of region to check for entrances
    :return: list of nation names
    """

    events = client.ns_request(params={'q': 'happenings', 'filter': 'move', 'view': f'region.{region}'})

    nations = []
    for event in events:
        destination = re.search(r'[\w-]+(?=%%\.)', event['text']).group(0)
        if destination == region:
            nations.append(re.search(r'[\w-]+(?=@@ relo)', event['text']).group(0))

    return nations


def wa_join(client: wrapper.Client, region=None) -> list:
    """
    Gets a list of all nations recently admitted to the WA.
    :param client: initialized client object that can be used to make API queries.
    :param region: region to check for WA admissions; if not specified, will get all WA admissions
    :return: list of nation names
    """
    if region is None:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'member'})
    else:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'member', 'view': f'region.{region}'})

    nations = []
    for event in events:
        check = re.search(r'[\w-]+(?=@@ was admitted)', event['text'])
        if check is not None:
            nations.append(check.group(0))

    return nations


def wa_resign(client: wrapper.Client, region: str = None) -> list:
    """
    Gets a list of all nations recently resigning from the WA.

    :param client: initialized client object that can be used to make API queries.
    :param region: name of region to check for WA resignations; if omitted, will get all WA resignations
    :return: list of nation names
    """

    if region is None:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'member'})
    else:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'member', 'view': f'region.{region}'})

    nations = []
    for event in events:
        check = re.search(r'[\w-]+(?=@@ resigned)', event['text'])
        if check is not None:
            nations.append(check.group(0))

    return nations


def wa_endorse(client: wrapper.Client, nation: str, region: str = None) -> list:
    """
    Get list of all nations recently endorsing a specified nation

    :param client: initialized client object that can be used to make API queries.
    :param nation: name of nation to check for endorsements
    :param region: name of region to check endorsements, optional but recommended
    :return: list of nation names
    """
    if region is None:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'endo'})
    else:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'endo', 'view': f'region.{region}'})

    nations = []
    for event in events:
        endorser = re.search(r'[\w-]+(?=@@ en)', event['text'])
        endorsee = re.search(r'[\w-]+(?=@@\.)', event['text'])

        if endorser is not None and endorsee.group(0) == nation:
            nations.append(endorser.group(0))

    return nations


def wa_unendorse(client: wrapper.Client, nation: str, region: str = None) -> list:
    """
    Gets list of nations recently withdrawing their endorsement from a specified nation

    :param client: initialized client object that can be used to make API queries.
    :param nation: name of nation to check for withdrawn endorsements
    :param region: name of region to check endorsements, highly recommended
    :return: list of nation names
    """
    if region is None:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'endo'})
    else:
        events = client.ns_request(params={'q': 'happenings', 'filter': 'endo', 'view': f'region.{region}'})

    nations = []
    for event in events:
        endorser = re.search(r'[\w-]+(?=@@ wi)', event['text'])
        endorsee = re.search(r'[\w-]+(?=@@\.)', event['text'])

        if endorser is not None and endorsee.group(0) == nation:
            nations.append(endorser.group(0))

    return nations


def endorsements(client: wrapper.Client, nation: str) -> list:
    """
    Get a list of a nation's endorsements
    :param client: initialized client object that can be used to make API queries.
    :param nation: name of nation to check for endorsements
    :return: list of nation names
    """
    return client.ns_request(params={'nation': nation, 'q': 'endorsements'})['ENDORSEMENTS'].split(',')


def wa_delegates(client: wrapper.Client) -> list:
    """
    Get list of all World Assembly delegates
    :param client: initialized client object that can be used to make API queries.
    :return: list of nation names
    """
    return client.ns_request(params={'wa': '1', 'q': 'delegates'})['delegates']


def wa_members(client: wrapper.Client) -> list:
    """
    Get list of World Assembly nations
    :param client: initialized client object that can be used to make API queries.
    :return: list of nation names
    """
    return client.ns_request(params={'wa': '1', 'q': 'members'})['members']
