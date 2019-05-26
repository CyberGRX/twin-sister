from expects.matchers import Matcher


class contain_all_items_in(Matcher):

    def __init__(self, expect_dict, ignore_keys=None):
        if ignore_keys:
            filtered_expected = {k: v for (k, v) in expect_dict.items()
                                 if k not in ignore_keys}
            self._expected_items = filtered_expected.items()
        else:
            self._expected_items = expect_dict.items()

    def _match(self, actual):
        for expected in self._expected_items:
            matched = None
            for actual_item in actual.items():
                if expected == actual_item:
                    matched = True
                    break
            if not matched:
                return False, ['%s is missing', str(expected)]
        return True, ['All items are present']
