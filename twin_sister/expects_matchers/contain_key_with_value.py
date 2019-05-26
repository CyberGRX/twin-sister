from expects.matchers import Matcher


class contain_key_with_value(Matcher):

    def __init__(self, expected_key, expected_value):
        self._expected_key = expected_key
        self._expected_value = expected_value

    def _match(self, actual_dict):
        if self._expected_key in actual_dict.keys():
            actual_value = actual_dict[self._expected_key]
            return (
                self._expected_value == actual_dict[self._expected_key],
                ['%s contains "%s" == "%s"' % (
                    actual_dict, self._expected_key, actual_value)])
        return False, ['%s does not contain "%s"' % (
            actual_dict, self._expected_key)]
