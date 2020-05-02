from math import sin, atan2, sqrt, cos


def pretty_request(request):
	headers = ''
	for header, value in request.META.items():
		if not header.startswith('HTTP'):
			continue
		header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
		headers += '{}: {}\n'.format(header, value)

	return (
		'{method} HTTP/1.1\n'
		'Content-Length: {content_length}\n'
		'Content-Type: {content_type}\n'
		'{headers}\n\n'
		'{body}'
	).format(
		method=request.method,
		content_length=request.META['CONTENT_LENGTH'],
		content_type=request.META['CONTENT_TYPE'],
		headers=headers,
		body=request.body,
	)


# print(distance("52.2296756,21.0122287", "52.406374,16.9251681"))

def trim_replace_wsp(string, replace_with='-'):
	import re
	return re.sub('\s+', replace_with, string.strip().lower())


def image_to_file(img_base64, file_id):
	import base64
	from django.core.files.base import ContentFile

	image_data = img_base64
	format, imgstr = image_data.split(';base64,')
	print("format", format)
	ext = format.split('/')[-1]

	data = ContentFile(base64.b64decode(imgstr))
	file_name = str(file_id) + '.' + ext
	return file_name, data


# user.image.save(file_name, data, save=True)  # image is User's model field


# ------------------- Pagination --------------------
def get_page_objects(qset, page, items_per_page=0):
	"""
	https://docs.djangoproject.com/en/2.2/topics/pagination/
	:param qset: queryset or array
	:param page: page no to view
	:param items_per_page: no of items per page
	:return: page object which is iterable
	"""
	if page is None or page == 0:
		page = 1
	if items_per_page is None or items_per_page == 0:
		from webAdmin.utils import get_no_items_per_page
		items_per_page = get_no_items_per_page()
	from django.core.paginator import Paginator
	return Paginator(qset, items_per_page).get_page(page)
