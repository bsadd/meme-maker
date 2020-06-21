"""
Contains utility functions to insert bulk data via `utils_db.py` functions for testing purposes
"""

from memesbd.utils_db import insert_post_path


def post_inserter(start, end):
    for i in range(start, end + 1):
        insert_post_path(caption='post' + str(i), keyword_list=['Frustrated', 'Angry', 'Iron Man', 'MCU'],
                         image_path='img/' + str(i) + '.jpg', user_id=2, is_adult=False)


def post_list_inserter(imglist=None, filefmt='png'):
    if imglist is None:
        imglist = []
    for i in imglist:
        insert_post_path(caption='post' + str(i), keyword_list=['Frustrated', 'Angry', 'Iron Man', 'MCU'],
                         image_path='img/' + str(i) + ('.%s' % filefmt), user_id=2, is_adult=False)
