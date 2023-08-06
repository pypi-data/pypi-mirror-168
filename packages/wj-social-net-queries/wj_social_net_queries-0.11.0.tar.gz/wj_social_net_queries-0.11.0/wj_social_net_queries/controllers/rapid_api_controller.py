import datetime as dt
from datetime import timedelta
from typing import Optional

from wj_social_net_queries.connectors.rapid_api_connector import RapidAPIConnector


def get_ig_post_info(permalink: str):
    """
    Description
    ----------
    Given a Facbook account token, this function searches if there is a
    business account id related with this account.

    Arguments
    ---------
    token: str
        Facebook token

    Return
    -------
    is_business: bool, str | bool, error_message

    """
    rapid_api = RapidAPIConnector()
    post_success, data = rapid_api.instagram_data_post_metadata(permalink=permalink)
    if not post_success:
        return

    return data


def get_ig_user_info_by_username(username: str):
    """
    Description
    ----------
    Given a valid ig username, this function searches the information profile info
    from a instagram user.

    Arguments
    ---------
    username: str
        Instagram username

    Return
    -------
    is_business: bool, str | bool, error_message

    """
    rapid_api = RapidAPIConnector()
    search_success, data = rapid_api.instagram_data_user_by_username_metadata(
        username=username
    )
    if not search_success:
        return

    return data


def get_posts_info_by_location_id(
        location_id: int,
        days_limit: Optional[int] = None,
        recusrsive_explore: Optional[bool] = None,
):
    """
    Description
    ----------
    Given an Instagram location_id, gets posts related sorted by last date
    ---------
    username: int
    end_cursor: int

    Return
    -------
    is_business: bool, str | bool, error_message

    """
    posts = []
    rapid_api = RapidAPIConnector()
    search_success, data = rapid_api.instagram_posts_by_location_id(
        location_id=location_id
    )

    if not search_success:
        return

    #TODO: Desacoplar la comprobación de días
    if days_limit:
        datetime_limit = dt.datetime.now() - timedelta(days=days_limit)
        for post in data["collector"]:
            post_date = dt.datetime.fromtimestamp(post["taken_at_timestamp"])
            if post_date > datetime_limit:
                posts.append(post)
            else:
                recusrsive_explore = False
                break
    else:
        for post in data["collector"]:
            posts.append(post)

    if recusrsive_explore and data["has_more"]:
        has_more = data["has_more"]
        while has_more:
            search_success, data = rapid_api.instagram_posts_by_location_id(
                location_id=location_id,
                end_cursor=data["end_cursor"]
            )

            if not search_success:
                break
            has_more = data["has_more"]
            if days_limit:
                datetime_limit = dt.datetime.now() - timedelta(days=days_limit)
                for post in data["collector"]:
                    post_date = dt.datetime.fromtimestamp(
                        post["taken_at_timestamp"]
                    )
                    if post_date > datetime_limit:
                        posts.append(post)
                    else:
                        has_more = False
                        break
            else:
                for post in data["collector"]:
                    posts.append(post)

    if not search_success:
        return

    return posts
