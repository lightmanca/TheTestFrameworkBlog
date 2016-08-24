from DataObjects.DataObjectBase import DataObjectBase


class PostStatusResponse(DataObjectBase):
    created_at = None
    id = None
    id_str = None
    text = None
    truncated = False
    entities = {}
    source = None
    in_reply_to_status_id = None
    in_reply_to_status_id_str = None
    in_reply_to_user_id = None
    in_reply_to_user_id_str = None
    in_reply_to_screen_name = None
    user = {}
    geo = None
    coordinates = None
    place = None
    contributors = None
    is_quote_status = None
    retweet_count = None
    favorite_count = None
    favorited = None
    retweeted = None
    lang = None

    status_list = []

    def __init__(self):
        # Nothing here, as everything gets loaded below
        pass

    @classmethod
    def list_from_dict(cls, data_list):
        cls = cls()
        cls.status_list = []
        for item in data_list:
            status = cls.from_dict(item)
            cls.status_list.append(status)
        return cls

    def find_record_with_status_text(self, status_text):
        return next((r for r in self.status_list if r.text == status_text), None)

    def find_record_by_id(self, id):
        return next((r for r in self.status_list if r.id == id), None)
