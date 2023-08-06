from typing import Optional

from wj_social_net_queries.controllers.meta_controller import (
    publish_fb_image,
    publish_fb_message
)
from wj_social_net_queries.utils.constants.constants import TOKEN


class Facebook:
    """
    Description
    ----------
    Allows the use of functions related with Facebook platform

    """

    token = None

    def __init__(self, token: Optional[str] = None) -> None:
        if token:
            self.token = token
        else:
            self.token = TOKEN

    def publish_message(
        self,
        page_id: str,
        message: str,
    ):
        media_id = publish_fb_message(
            token=self.token,
            page_id=page_id,
            message=message
        )
        return media_id


    def publish_image(
        self,
        page_id: str,
        image_url: str,
    ):
        media_id = publish_fb_image(
            token=self.token,
            page_id=page_id,
            image_url=image_url
        )
        return media_id