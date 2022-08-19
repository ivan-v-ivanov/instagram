import scrapy
import re
import json
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from urllib.parse import urlencode
from copy import deepcopy

class UserFirstSpider(scrapy.Spider):
    name = 'instagram_1'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'ijrevol'
    #inst_password = '#PWD_INSTAGRAM_BROWSER:10:1660366705:AexQAFMv3tePEQ0IgMG7ggLqtvqq+kByrfI26pqZmGirM1lEP4jKhjV8Bv5Mtg0Hd8rPA0FGBwamhIoqSej9+jDmFS3qpvzltcgqyHwYkVit+Ifpqt90dDFHeQt+Ho6T+8FzitmiZyDseET57nD4cG8='
    inst_password = '#PWD_INSTAGRAM_BROWSER:10:1660734466:AYlQADcXK5KxZtmqCq6spOkzvLyVVjTDKH10mQh4h6YYjlhql0iAR+xC94FvaJ5UMbhd/BrrQw3LrkipUFhVLf/MgyKzC4l6QymrMy9lo+a3AhKOIPvCs4hyNt9f2gUN0VkkBHz96i70+ZHrc3Qb8PE='
    user = 'python_code9.py' #'data_science_learn'
    user_id = '53735532112'#'17616713688'
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    inst_api_link = 'https://i.instagram.com/api/v1/friendships/'
    #posts_hash = '69cba40317214236af40e7efa697781d'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_password},
                                 headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            yield response.follow(
                f'/{self.user}/',
                callback=self.user_followers_parse,
                cb_kwargs={'username': self.user}
            )

    def user_followers_parse(self, response: HtmlResponse, username):
        user_id = self.user_id
        variables = {'count': 12}
        friendships_url = f'{self.inst_api_link}{user_id}/followers/?{urlencode(variables)}'

        yield response.follow(
            friendships_url,
            callback=self.followers_data_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def followers_data_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()

        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            friendships_url = f'{self.inst_api_link}{user_id}/followers/?{urlencode(variables)}'

            yield response.follow(
                friendships_url,
                callback=self.followers_data_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        friendships = j_data.get('users')

        for friend in friendships:
            item = InstaparserItem(
                user_id=user_id,
                username=username,
                friend_username=friend.get('username'),
                friend_fullname=friend.get('full_name'),
                friend_pic=friend.get('profile_pic_url')
            )
            yield item


    def user_following_parse(self, response: HtmlResponse, username):
        user_id = self.user_id
        variables = {'count': 12}
        following_url = f'{self.inst_api_link}{user_id}/following/?{urlencode(variables)}'

        yield response.follow(
            following_url,
            callback=self.following_data_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def following_data_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()

        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            following_url = f'{self.inst_api_link}{user_id}/followers/?{urlencode(variables)}'

            yield response.follow(
                following_url,
                callback=self.following_data_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )

        following = j_data.get('users')

        for follow in following:
            item = InstaparserItem(
                user_id=user_id,
                username=username,
                follow_username=follow.get('username'),
                follow_fullname=follow.get('full_name'),
                follow_pic=follow.get('profile_pic_url')
            )
            yield item

    # def user_parse_(self, response: HtmlResponse, username):
    #     user_id = self.user_id
    #     variables = {'id': user_id, 'first': 12}
    #     url_posts = f'{self.inst_graphql_link}query_hash={self.posts_hash}&{urlencode(variables)}'
    #
    #     yield response.follow(
    #         url_posts,
    #         callback=self.user_posts_parse,
    #         cb_kwargs={'username': username,
    #                    'user_id': user_id,
    #                    'variables': deepcopy(variables)}
    #     )
    #
    # def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
    #     j_data = response.json()
    #     page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
    #     if page_info.get('has_next_page'):
    #         variables['after'] = page_info.get('end_cursor')
    #         url_posts = f'{self.inst_graphql_link}query_hash={self.posts_hash}&{urlencode(variables)}'
    #
    #         yield response.follow(
    #             url_posts,
    #             callback=self.user_posts_parse,
    #             cb_kwargs={'username': username,
    #                        'user_id': user_id,
    #                        'variables': deepcopy(variables)}
    #         )
    #
    #     posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
    #     for post in posts:
    #         item = InstaparserItem(
    #             user_id=user_id,
    #             username=username,
    #             likes=post.get('node').get('edge_media_preview_like').get('count'),
    #             photo=post.get('node').get('display_url'),
    #             post_data=post.get('node')
    #         )
    #         yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')