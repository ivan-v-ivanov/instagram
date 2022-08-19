# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import pandas

class InstaparserPipeline:

    # def process_item(self, item, spider):
    #     print()
    #     return item

    def __init__(self):
        user_info = {'main_user_name': [],
                     'main_user_id': [],
                     'is_friend': [],
                     'is_follower': [],
                     'some_user_name': [],
                     'some_user_fig': []}
        self.user_info = user_info

    def process_item(self, item, spider):
        mainusername = item['username']
        mainuserid = item['user_id']

        if 'friend_fullname' in list(item.keys()) and 'follow_fullname' in list(item.keys()):
            is_friend = True
            is_follower = True
            userfullname = item['friend_fullname']
            username = item['friend_username']
            userfig = item['friend_pic']

        if 'friend_fullname' in list(item.keys()):
            is_friend = True
            is_follower = False
            userfullname = item['friend_fullname']
            username = item['friend_username']
            userfig = item['friend_pic']

        elif 'follow_fullname' in list(item.keys()):
            is_friend = False
            is_follower = True
            userfullname = item['follow_fullname']
            username = item['follow_username']
            userfig = item['follow_pic']

        else:
            is_follower = False
            is_friend = False
            userfullname = item['follow_fullname']
            username = item['follow_username']
            userfig = item['follow_pic']

        self.user_info['main_user_name'].append(mainusername)
        self.user_info['main_user_id'].append(mainuserid)
        self.user_info['is_friend'].append(is_friend)
        self.user_info['is_follower'].append(is_follower)
        self.user_info['some_user_name'].append(username)
        self.user_info['some_user_fig'].append(userfig)

        print(self.user_info)
        return self.user_info
