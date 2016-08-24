from DataObjects.DataObjectBase import DataObjectBase


class PostStatusRequest(DataObjectBase):
    status = None
    in_reply_to_status_id = None
    possibly_sensitive = None
    trim_user = None

    def __init__(self, status, trim_user=False, possibly_sensitive=None, in_reply_to_status_id=None):
        self.status = status
        self.trim_user = trim_user
        self.possibly_sensitive = possibly_sensitive
        self.in_reply_to_status_id = in_reply_to_status_id
