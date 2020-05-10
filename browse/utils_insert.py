from browse.utils_db import insert_template_post_path


def post_inserter(start, end):
    for i in range(start, end + 1):
        insert_template_post_path(caption='post' + str(i), keyword_list=['Frustrated', 'Angry', 'Iron Man', 'MCU'],
                                  image_path='img/' + str(i) + '.jpg', user_id=2, is_adult=False)


def post_list_inserter(imglist=None):
    if imglist is None:
        imglist = []
    for i in imglist:
        insert_template_post_path(caption='post' + str(i), keyword_list=['Frustrated', 'Angry', 'Iron Man', 'MCU'],
                                  image_path='img/' + str(i) + '.jpg', user_id=2, is_adult=False)
