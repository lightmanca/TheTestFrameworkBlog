import urllib


class DataObjectBase:

    def create_query_string(self):
        payload = ""
        items = self.__dict__
        for key in items:
            if items[key]:
                payload += "{}={}&".format(key, urllib.parse.quote(str(items[key])))
        if payload:
            # removing trailing "&"
            payload = payload[:-1]
        return payload

    @classmethod
    def from_dict(cls, data_dict):
        cls = cls()
        for key in data_dict:
            cls.__dict__[key] = data_dict[key]
        return cls
