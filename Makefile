.PHONY: import-posts
import-posts:
	python backend/manage.py import_insta_content posts --path data/posts_1.json 