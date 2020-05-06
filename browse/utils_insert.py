from browse.utils_db import insert_template_post_path


def post_inserter(start, end):
    for i in range(start, end + 1):
        insert_template_post_path(caption='post' + str(i), genre_list=['Frustrated', 'Angry', 'Iron Man', 'MCU'],
                                  image_path='img/' + str(i) + '.jpg', user_id=2, is_adult=False)


# insert_post_path('Iron man2',['Frustrated', 'Angry', 'Iron Man', 'MCU'],'Iron man','browse/2.jpg', 2)
def post_list_inserter(imglist=None):
    if imglist is None:
        imglist = []
    for i in imglist:
        insert_template_post_path(caption='post' + str(i), genre_list=['Frustrated', 'Angry', 'Iron Man', 'MCU'],
                                  image_path='img/' + str(i) + '.jpg', user_id=2, is_adult=False)
