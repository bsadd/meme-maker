from browse.utils_db import insert_post_path


def post_inserter(start, end):
	for i in range(start, end + 1):
		insert_post_path('post' + str(i), ['Frustrated', 'Angry', 'Iron Man', 'MCU'], 'Iron man',
		                 'img/' + str(i) + '.jpg', 2)
# insert_post_path('Iron man2',['Frustrated', 'Angry', 'Iron Man', 'MCU'],'Iron man','browse/2.jpg', 2)
