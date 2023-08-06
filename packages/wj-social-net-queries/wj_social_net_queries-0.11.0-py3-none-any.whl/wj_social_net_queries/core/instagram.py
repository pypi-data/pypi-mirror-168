from email import message
from typing import Optional

from wj_social_net_queries.controllers.rapid_api_controller import (
    get_posts_info_by_location_id,
    get_ig_post_info
)
from wj_social_net_queries.controllers.meta_controller import (
    download_recent_media_ig,
    download_recent_media_ig_by_post,
    get_hashtag_media_ig,
    get_users_by_hashtag_media_ig,
    publish_ig_content_image
)
from wj_social_net_queries.utils.AWS.s3 import AwsS3
from wj_social_net_queries.utils.constants.api_graph_constants import (
    RECENT_MEDIA_OPTION,
    IG_PERMALINK,
    NO_LOCATION_DATA
)
from wj_social_net_queries.utils.constants.constants import TOKEN
from wj_social_net_queries.utils.ig_utils import get_shortcode_from_permalink
from wj_social_net_queries.utils.utils import (
    download_image,
    generate_file_name_with_datetime,
    save_data_on_json,
)


class Instagram:
    """
    Description
    ----------
    Allows the use of functions related with Instagram platform

    """

    token = None

    def __init__(self, token: Optional[str] = None) -> None:
        if token:
            self.token = token
        else:
            self.token = TOKEN

    def download_recent_all_media(self, query: str, file_type: str):
        download_recent_media_ig(query=query, token=self.token, file_type=file_type)

    def download_recent_media_ig_by_post(self, query: str):
        download_recent_media_ig_by_post(
            query=query,
            token=self.token,
        )

    def upload_hashtag_media_to_s3(
        self,
        query: str,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ):
        data, addional_data = get_hashtag_media_ig(
            query=query,
            token=self.token,
            hashtag_content=RECENT_MEDIA_OPTION,
            aditional_fields=True,
        )

        s3 = AwsS3(
            bucket=bucket_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        json_path = generate_file_name_with_datetime(extension="json")
        save_data_on_json(path=json_path, data=addional_data)
        s3.upload_file(local_file=json_path, s3_filename=json_path, directory="raw")
        for post in data:
            if not post or post["media_type"] != "IMAGE":
                continue
            shortcode = get_shortcode_from_permalink(permalink=post["permalink"])
            s3.upload_file_from_url_to_aws_s3(
                url=post["media_url"], directory="raw", file_name=shortcode
            )
        folders = s3.files_in_folder(folder="raw")
        print(folders)
    
    def get_users_profile_info(
        self,
        query: str,
    ):
        data, addional_data = get_users_by_hashtag_media_ig(
            query=query,
            token=self.token,
            hashtag_content=RECENT_MEDIA_OPTION,
        )
        return data, addional_data
    

    def get_post_data_by_short_code(
        self,
        short_code:str
    ):
        permalink = IG_PERMALINK.format(shortcode=short_code)
        post_info = get_ig_post_info(permalink=permalink)

        return post_info


    def get_posts_info_by_location_id(
        self,
        location_id: int,
        days_limit: Optional[int] = None,
        recusrsive_explore: Optional[bool] = None,
    ):
        content = get_posts_info_by_location_id(
            location_id=location_id,
            days_limit=days_limit,
            recusrsive_explore=recusrsive_explore,
        )
        return content
    

    def publish_image(
        self,
        caption: str,
        image_url: str,
        is_carousel_item: Optional[bool] = None,
        location_id: Optional[int] = None,
        user_tags: Optional[str] = None,
        product_tags: Optional[str] = None
    ):
        media_id = publish_ig_content_image(
            token=self.token,
            caption=caption,
            image_url=image_url,
            is_carousel_item=is_carousel_item,
            location_id=location_id,
            user_tags=user_tags,
            product_tags=product_tags
        )
        return media_id


    def upload_located_posts_media_to_s3(
        self,
        location_id: int,
        days_limit: int,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ):
        data = None

        data = get_posts_info_by_location_id(
            location_id=location_id,
            days_limit=days_limit,
            recusrsive_explore=True,
        )

        if not data:
            message = NO_LOCATION_DATA.format(
                days_limit=days_limit,
                location_id=location_id
            )
            print(message)
            return

        addional_data = []
        for post in data:
            if post["is_video"]:
                continue
            permalink = IG_PERMALINK.format(shortcode=post["shortcode"])
            post_data = self.get_post_data_by_short_code(
                short_code=post["shortcode"]
            )
            post["permalink"] = permalink
            addional_data.append(
                post_data
            )

        s3 = AwsS3(
            bucket=bucket_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        json_path = generate_file_name_with_datetime(extension="json")
        save_data_on_json(path=json_path, data=addional_data)
        s3.upload_file(local_file=json_path, s3_filename=json_path, directory="raw")
        for post in data:
            try:
                shortcode = get_shortcode_from_permalink(permalink=post["permalink"])
                s3.upload_file_from_url_to_aws_s3(
                    url=post["display_url"], directory="raw", file_name=shortcode
                )
            except:
                print("Cannot get metadata")
        print("done")
