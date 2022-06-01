from app.models import Post
from app import db
from datetime import datetime

import os
import markdown

posts = Post.query.all()
for post in posts:
    db.session.delete(post)

# title_aboutme = 'About Me'
# content_aboutme = '''
# ## 👋 Hello world!

#  - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ )
#  - 대한민국 공군 ROKAF 병 825기 정보체계관리(30010 과정) (2021.04.12 ~ 2023.01.11)
#  - GiftMusic backend 개발자 (2020.09 ~ 2021.04)

# ## 🧑🏻‍💻 My Projects

#  - [Follow Link Here](https://github.com/bnbong/bnbong.github.io)

# ## 💻 My Stacks
  
#   - Language & Frameworks
# <div>
#   <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>
#   <img src="https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=C&logoColor=white"/>
#   <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=flat-sqaure&logo=c%2B%2B&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Java-F7DF1E?style=flat-square&logo=Java&logoColor=black"/>
#   <img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=r&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/>
#   <img src="https://img.shields.io/badge/firebase-ffca28?style=flat-square&logo=firebase&logoColor=black"/>
#   <img src="https://img.shields.io/badge/Junit5-25A162?style=flat-square&logo=junit5&logoColor=white"/>
#   <img src="https://img.shields.io/badge/JWT-000000?style=flat-square&logo=JSON%20web%20tokens&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white"/>
#   <img src="	https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=Postman&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Android%20Studio-FFFFFF?style=flat-square&logo=Android%20Studio"/>
# </div>

#   - Databases & Devops
# <div>
#   <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=flat-square&logo=MongoDB&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Mysql-005C84?style=flat-square&logo=MySql&logoColor=white"/>
#   <img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=PostgreSQL&logoColor=white"/>
#   <img src="https://img.shields.io/badge/elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white"/>
#   <img src="https://img.shields.io/badge/SQLite-07405E?style=flat-square&style=for-the-badge&logo=sqlite&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Github-092E20?style=flat-square&logo=Github&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=Git&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Jira-0052CC?style=flat-square&logo=Jira&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Jenkins-D24939?style=flat-sqaure&logo=Jenkins&logoColor=white"/>
# </div>

#   - IDE
# <div>
#   <img src="https://img.shields.io/badge/Eclipse-2C2255?style=flat-square&logo=eclipse&logoColor=white"/>
#   <img src="https://img.shields.io/badge/IntelliJ_IDEA-000000.svg?style=flat-square&logo=intellij-idea&logoColor=white"/>
#   <img src="	https://img.shields.io/badge/PyCharm-000000.svg?&style=flat-square&logo=PyCharm&logoColor=white"/>
#   <img src="https://img.shields.io/badge/RStudio-75AADB?style=flat-sqaure&logo=RStudio&logoColor=white"/>
#   <img src="https://img.shields.io/badge/VIM-%2311AB00.svg?&style=flat-square&logo=vim&logoColor=white"/>
#   <img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=flat-square&logo=visual%20studio%20code&logoColor=white"/>
# </div>
 
# ## 👀 I’m interested in ...

#  - Python Django 프레임워크 등을 이용한 웹 백앤드 개발
#  - React, Vue.js 등을 이용한 웹 프론트앤드 개발
#  - 음악과 관련된 웹 또는 앱 개발
#  - 게임 개발
#  - 딥러닝 등의 AI 기술

# ## 🌱 I’m currently learning ...

#  - GoLang
#  - JavaScript, Html
#  - Django & MongoDB를 활용한 사이트 혹은 백앤드 개발
#  - Algorithms (implemented with Python)

# ## 💞️ I’m looking to collaborate on ...

#  - 웹 백앤드 및 프론트앤드 개발 능력이 있으신 분
#  - 컨텐츠 기획에 풍부한 경험이 있으신 분
#  - 게임 프로그래머 이시거나 게임 프로그래밍을 해보신 분

# ## 📫 How to reach me ...

#  - MY WEBSITE :
# <div>
#   <a href="https://github.com/bnbong/"><img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub"/></a>&nbsp
#   <a href="https://bnbongdevstory.tistory.com/"><img src="https://img.shields.io/badge/my tistory-000000?style=flat-square&logo=About.me&logoColor=white"/></a>&nbsp
#   <a href="https://bnbong.pythonanywhere.com/"><img src="https://img.shields.io/badge/my website-000000?style=flat-square&logo=About.me&logoColor=white"/></a>&nbsp
# </div>

#  - EMAIL ME : 
# <div>
#    <a href="mailto:bbbong9@gmail.com"><img src="https://img.shields.io/badge/Gmail-d14836?style=flat-square&logo=Gmail&logoColor=white&link=bbbong9@gmail.com"/></a>&nbsp
#    <a href="mailto:bnbong@naver.com"><img src="https://img.shields.io/badge/Naver-2DB400?style=flat-square&logo=Naver&logoColor=white&link=bnbong@naver.com"/></a>&nbsp
# </div>

#  - Direct Message ME : 
# <div>
#    <a href="https://www.instagram.com/j_hyeok__lee/?hl=ko"><img src="https://img.shields.io/badge/Instagram-E4405F?style=flat-square&logo=Instagram&logoColor=white&link=https://www.instagram.com/j_hyeok__lee/?hl=ko"/></a>&nbsp
#    <a href="https://www.facebook.com/profile.php?id=100007712465866"><img src="https://img.shields.io/badge/Facebook-3b5998?style=flat-square&logo=Facebook&logoColor=white&link=https://www.facebook.com/profile.php?id=100007712465866"/></a>&nbsp
#    <a href="https://www.linkedin.com/in/%EC%A4%80%ED%98%81-%EC%9D%B4-669733231/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white"/></a>&nbsp
# </div>
# <br>
# '''

# content_aboutme = markdown.markdown(content_aboutme)

# post_aboutme = Post(title=title_aboutme, content=content_aboutme)
# db.session.add(post_aboutme)

# post_dir = os.path.abspath('../Myblog_posts/posts')
# dirname = os.path.dirname(post_dir)
# listdirname = os.listdir(post_dir)

#     # variable lists:
#     # IT, Study, Hobby, My_Daily_Life, Development, Game = \
#     #     listdirname[0], listdirname[1], listdirname[2], listdirname[3], listdirname[4], listdirname[5]

# for cat_name in listdirname:
#   post_dates = os.listdir(os.path.join(post_dir, cat_name))

#   db_selected = Post.query.filter_by(tag=cat_name).all()
#   db_dates = []
#   for post in db_selected:
#       db_dates.append(post.get_exact_created())

#   for date in post_dates:
#       year, month, day, hour, minute, sec = int(date[:4]), int(date[4:6]), int(date[6:8]),\
#           int(date[8:10]), int(date[10:12]), int(date[12:14])
#       new_date = datetime(year, month, day, hour, minute, sec)

#             # checking and add newest posts at selected categories
#       if str(new_date) not in db_dates:
#           post_created = new_date
#           with open(os.path.join(post_dir, cat_name, date, 'title.txt'), 'r') as f1:
#               post_title = f1.read()
#               f1.close()
#           with open(os.path.join(post_dir, cat_name, date, 'post.md'), 'r') as f2:
#               post_content = f2.read()
#               f2.close()
#           new_post = Post(title=post_title, content=post_content, created=post_created, tag=cat_name)
#           db.session.add(new_post)


db.session.commit()
