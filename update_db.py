# TODO: make fuctions which update existing posts when they updated. 

post_dir = os.path.abspath('../Myblog_posts/posts')
category_name_lists = os.listdir(post_dir)

# possible category lists:
# IT, Study, Hobby, My_Daily_Life, Development, Game = \
#     listdirname[0], listdirname[1], listdirname[2], listdirname[3], listdirname[4], listdirname[5]

for category in category_name_lists:
    post_dates = os.listdir(os.path.join(post_dir, category))

db_selected = Post.query.filter_by(tag=category).all()
db_dates = []
for post in db_selected:
    db_dates.append(post.get_exact_created())

for date in post_dates:
    year, month, day, hour, minute, sec = split_datestring_into_datetime(date)
    new_date = datetime(year, month, day, hour, minute, sec)

    # checking and add newest posts at selected categories
    if str(new_date) not in db_dates:
        post_created, post_title,post_thumbnail_url, post_content, post_content_preview\
            = get_new_post_data()

        new_post = Post(title=post_title, thumbnail_url=post_thumbnail_url, content=post_content, \
            content_preview=post_content_preview, created=post_created, tag=category)

        db.session.add(new_post)

db.session.commit()
