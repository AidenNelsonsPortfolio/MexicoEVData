# This file holds all test cases to run algorithms on
from definitions import TestCase, GraphType

ONE_THOUSAND_TEST_CASES: list[TestCase] = [
    # TestCase("20214", "20134", GraphType.ONE_THOUSAND_NODES),
    # TestCase("21146", "12032", GraphType.ONE_THOUSAND_NODES),
    TestCase("29048", "21074", GraphType.ONE_THOUSAND_NODES),
    # TestCase("20232", "20544", GraphType.ONE_THOUSAND_NODES),
    # TestCase("20023", "20169", GraphType.ONE_THOUSAND_NODES),
    # TestCase("21143", "29010", GraphType.ONE_THOUSAND_NODES),
    TestCase("15008", "21176", GraphType.ONE_THOUSAND_NODES),
    TestCase("17014", "21159", GraphType.ONE_THOUSAND_NODES),
    TestCase("16088", "16064", GraphType.ONE_THOUSAND_NODES),
    TestCase("15037", "13008", GraphType.ONE_THOUSAND_NODES),
    # TestCase("20425", "20223", GraphType.ONE_THOUSAND_NODES),
    # TestCase("21201", "17015", GraphType.ONE_THOUSAND_NODES),
    # TestCase("30042", "30071", GraphType.ONE_THOUSAND_NODES),
    # TestCase("12060", "12003", GraphType.ONE_THOUSAND_NODES),
    # TestCase("20098", "20498", GraphType.ONE_THOUSAND_NODES),
    # TestCase("12015", "21131", GraphType.ONE_THOUSAND_NODES),
    # TestCase("20267", "20157", GraphType.ONE_THOUSAND_NODES),
]

FIVE_HUNDRED_TEST_CASES: list[TestCase] = [
    # TestCase("01011", "32036", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("30161", "30155", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20372", "20050", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("27008", "30061", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("15103", "15025", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20050", "20133", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20464", "20047", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("30042", "30109", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("21128", "21096", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("24007", "24020", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20249", "20406", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("14099", "14110", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("08006", "08048", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20325", "20449", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("31063", "31101", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20379", "20050", GraphType.FIVE_HUNDRED_NODES),
    TestCase("02002", "02006", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20117", "20509", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("14050", "14030", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("19004", "19049", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("30074", "30138", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20349", "20118", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20524", "20089", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("17018", "17028", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20390", "20350", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("11004", "22014", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20138", "20442", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("24012", "24039", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20429", "20535", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("20125", "20512", GraphType.FIVE_HUNDRED_NODES),
    TestCase("08042", "08015", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("05032", "05028", GraphType.FIVE_HUNDRED_NODES),
    # TestCase("21176", "21165", GraphType.FIVE_HUNDRED_NODES),
]

ALL_SHORTEST_PATH_TEST_CASES: list[TestCase] = [
    TestCase(None, None, GraphType.FIVE_HUNDRED_NODES),
    # TestCase(None, None, GraphType.ONE_THOUSAND_NODES),
    # TestCase(None, None, GraphType.ALL_NODES),
]

TEST_CASES: list[TestCase] = ALL_SHORTEST_PATH_TEST_CASES
