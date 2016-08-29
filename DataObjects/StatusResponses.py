from DataObjects.StatusResponse import StatusResponse


class StatusResponses:
    status_list = []

    def __init__(self):
        # Nothing here, as everything gets loaded below
        pass

    @classmethod
    def list_from_dict(cls, data_list):
        cls = cls()
        cls.status_list = []
        for item in data_list:
            status = StatusResponse.from_dict(item)
            cls.status_list.append(status)
        return cls

    def find_record_with_status_text(self, status_text):
        return next((r for r in self.status_list if r.text == status_text), None)

    def find_record_by_id(self, id):
        return next((r for r in self.status_list if r.id == id), None)
