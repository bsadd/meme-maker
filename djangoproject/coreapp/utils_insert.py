"""
Contains utility functions to insert bulk data via `utils_db.py` functions for testing purposes
"""


#  ----------------------- Insert utils -------------------------
def insert_post_path(caption, keyword_list, image_path, is_adult, user_id):
    """
    :param text_boxes: a list of TextBox objects
    :param caption: caption
    :param keyword_list: list of keywords
    :param image_path: image path on server
    :param is_adult: is adult content
    :param user_id: author id
    """
    from memesbd.models import Post
    from memesbd.utils import trim_replace_wsp
    post = Post.objects.create(caption=trim_replace_wsp(caption), author_id=user_id)
    post.is_adult = is_adult
    for gen in keyword_list:
        from memesbd.models import Keyword, KeywordList
        gen = str(gen).strip().lower()
        keyword, _ = Keyword.objects.get_or_create(name=gen)
        KeywordList.objects.get_or_create(post=post, keyword=keyword)
    post.image = image_path
    post.save()
    return post


def insert_post(caption, user_id, image_base64, keyword_list=None, is_adult=False, is_violent=False, template_id=None):
    """
    :param text_boxes: a list of TextBox objects
    :param caption: caption
    :param keyword_list: list of keywords
    :param image_base64: js image data
    :param is_adult: is adult content
    :param is_violent: is violent content
    :param user_id: author id
    :param template_id: id of the meme on which it had been edited on
    """
    if keyword_list is None:
        keyword_list = []
    from memesbd.models import Post
    from memesbd.utils import trim_replace_wsp
    if template_id:
        template_id = Post.objects.get(id=template_id).get_template_id()
    post = Post.objects.create(caption=trim_replace_wsp(caption), author_id=user_id, template_id=template_id)
    post.is_adult = is_adult
    post.is_violent = is_violent
    for key in keyword_list:
        from memesbd.models import Keyword, KeywordList
        keyword, _ = Keyword.objects.get_or_create(name=str(key).strip().lower())
        KeywordList.objects.get_or_create(post=post, keyword=keyword)
    from memesbd.utils import image_to_file
    img_filename, img_data = image_to_file(img_base64=image_base64, file_id=post.id)
    post.image.save(img_filename, img_data, save=True)
    return post


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
