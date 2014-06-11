

class clean(object):
    def __init__(self, cleaner, keys=None, values=None, raises=False):
        self.cleaner = cleaner
        self.keys = keys
        self.values = values
        self.raises = raises

    def __call__(self, val):
        if self.cleaner is list:
            return self._clean_list(val)
        elif self.cleaner is dict:
            return self._clean_dict(val)
        else:
            return self.cleaner(val)

    def _clean_list(self, val):
        # apply cleaner to val
        result = list(val)

        # clean values
        if self.values is not None:
            if callable(self.values):
                # apply cleaner to all elements
                cleaner = self.values
                for i, element in enumerate(result):
                    result[i] = cleaner(element)
            else:
                # apply cleaners to specific values
                for i, cleaner in self.values.items():
                    try:
                        result[i] = cleaner(result[i])
                    except IndexError as e:
                        if self.raises:
                            raise e

        return result

    def _clean_dict(self, val):
        # apply clceaner to root
        result = dict(val)

        # clean keys
        if self.keys is not None:
            tmp = {}
            if callable(self.keys):
                # apply cleaner to all keys
                cleaner = self.keys
                for k, v in result.items():
                    tmp[cleaner(k)] = v
            else:
                # apply cleaners to specific keys
                for k, v in result.items():
                    cleaner = self.keys.get(k, lambda x: x)
                    tmp[cleaner(k)] = result[k]
            result = tmp

        # clean values
        if self.values is not None:
            if callable(self.values):
                # apply cleaner to all elements
                cleaner = self.values
                for k, v in result.items():
                    result[k] = cleaner(result[k])
            else:
                # apply cleaners to specific values
                for k, cleaner in self.values.items():
                    result[k] = cleaner(result[k])

        return result
