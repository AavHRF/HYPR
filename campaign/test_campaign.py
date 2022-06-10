from unittest import TestCase

import api
import campaign

# mediocre "unit tests" that I'm using to test each campaign and make sure their search functions work
# if they don't work as behaved check their search_param arguments and see if they still make sense, since most
# test cases are hardcoded to the pacific


class TestNewlyFounded(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")
        test_campaign = campaign.NewlyFounded(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={},
        )
        test_campaign.update_deque()
        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestResidents(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")
        test_campaign = campaign.Residents(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"region": "the_pacific"},
        )
        test_campaign.update_deque()
        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestEjections(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")
        test_campaign = campaign.Ejections(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"region": "the_pacific"},
        )
        test_campaign.update_deque()
        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestExits(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")
        test_campaign = campaign.Exits(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"region": "the_pacific"},
        )
        test_campaign.update_deque()
        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestEntrances(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")
        test_campaign = campaign.Entrances(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"region": "the_pacific"},
        )
        test_campaign.update_deque()
        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestWorldAssemblyAdmissions(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")
        test_campaign = campaign.WorldAssemblyAdmissions(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={},
        )
        test_campaign.update_deque()

        test_campaign2 = campaign.WorldAssemblyAdmissions(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"region": "the_pacific"},
        )
        test_campaign2.update_deque()

        print("Deque 1 Contents - world")
        print(test_campaign.deque)

        print("Deque 2 Contents - specific region")
        print(test_campaign2.deque)

        self.assertGreater(len(test_campaign.deque), 0)
        self.assertGreater(len(test_campaign2.deque), 0)


class TestWorldAssemblyResignations(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")
        test_campaign = campaign.WorldAssemblyResignations(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={},
        )
        test_campaign.update_deque()

        test_campaign2 = campaign.WorldAssemblyResignations(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"region": "the_pacific"},
        )
        test_campaign2.update_deque()

        print("Deque 1 Contents - world")
        print(test_campaign.deque)

        print("Deque 2 Contents - specific region")
        print(test_campaign2.deque)

        self.assertGreater(len(test_campaign.deque), 0)
        self.assertGreater(len(test_campaign2.deque), 0)


class TestNewEndorsements(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")

        test_campaign = campaign.NewEndorsements(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"nation": "east_durthang", "region": "the_pacific"},
        )
        test_campaign.update_deque()

        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestNewWithdrawnEndorsements(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")

        test_campaign = campaign.NewWithdrawnEndorsements(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={"nation": "east_durthang", "region": "the_pacific"},
        )
        test_campaign.update_deque()

        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreaterEqual(len(test_campaign.deque), 0)


class TestEndorsements(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")

        test_campaign = campaign.Endorsements(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={
                "nation": "east_durthang",
            },
        )
        test_campaign.update_deque()

        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestWorldAssemblyDelegates(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")

        test_campaign = campaign.WorldAssemblyDelegates(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={},
        )
        test_campaign.update_deque()

        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)


class TestWorldAssemblyMembers(TestCase):
    def test__search(self):
        api_handler = api.Client(useragent="HYPR Unit Tests - Khronion")

        test_campaign = campaign.WorldAssemblyMembers(
            name="test",
            priority=0,
            tgid=0,
            recruitment=False,
            handler=api_handler,
            search_params={},
        )
        test_campaign.update_deque()

        print("Deque Contents")
        print(test_campaign.deque)

        self.assertGreater(len(test_campaign.deque), 0)
