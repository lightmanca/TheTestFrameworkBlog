from DataObjects.DataObjectBase import DataObjectBase


class StatusResponse(DataObjectBase):
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

    def __init__(self):
        # Nothing here, as everything gets loaded via base class routines.
        pass

