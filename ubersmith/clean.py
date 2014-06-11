

class clean(object):
    def __init__(self, cleaner, keys=None, values=None, raises=False):
        self.cleaner = cleaner
        self.keys = keys
        self.values = values
        self.raises = raises

    def apply(self, val):
        if self.cleaner is list:
            return self._clean_list(val)
        elif self.cleaner is dict:
            return self._clean_dict(val)
        else:
            return self.cleaner(val)

    def _clean_list(self, val):
        result = list(val)
        if self.values is not None:
            if type(self.values) is list:
                for i, cleaner in self.values:
                    try:
                        if isinstance(cleaner, clean):
                            result[i] = cleaner.apply(result[i])
                        else:
                            result[i] = cleaner(result[i])
                    except IndexError as e:
                        if self.raises:
                            raise e
            else:
                for i, el in enumerate(result):
                    result[i] = self.values(el)
        return result

    def _clean_dict(self, val):
        val = dict(val)
        result = {}
        if self.keys is not None:
            if type(self.keys) is dict:
                for k, cleaner in self.keys.items():
                    result[cleaner(k)] = val[k]
            else:
                for k, v in val.items():
                    result[self.keys(k)] = v
        else:
            result = val

        if self.values is not None:
            if type(self.values) is dict:
                for k, cleaner in self.values.items():
                    if isinstance(cleaner, clean):
                        result[k] = cleaner.apply(result[k])
                    else:
                        result[k] = cleaner(result[k])
            elif isinstance(self.values, clean):
                for k, v in result.items():
                    result[k] = self.values.apply(result[k])
        return result
