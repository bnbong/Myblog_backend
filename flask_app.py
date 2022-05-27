import os
import sqlite3
import markdown
from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_cors import CORS
from dotenv import load_dotenv

template_dir = os.path.abspath('../Myblog_frontend/templates')
static_dir = os.path.abspath('../Myblog_frontend/static')

load_dotenv()

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    db_notes = conn.execute('SELECT id, title, created, content FROM notes;').fetchall()
    conn.close()

    notes = []
    for note in db_notes:
        note = dict(note)
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)
    # # for setting newest post to the front.
    # notes = notes.reverse()

    # index.html from Myblog_frontend
    return render_template('index.html', notes=notes)

@app.route('/aboutme')
def aboutme():
    from datetime import datetime

    title = "About Me"
    content = """
    ![header](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=300&section=header&text=JunHyeok%20Lee&fontSize=90&animation=fadeIn) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fbnbong%2Fhit-counter&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com) ![My trophy](https://github-profile-trophy.vercel.app/?username=bnbong) [![Github Stats](https://github-readme-stats.vercel.app/api?username=bnbong&count_private=true&theme=dark)](https://github.com/anuraghazra/github-readme-stats) ![Most Used Language](https://github-readme-stats.vercel.app/api/top-langs/?username=bnbong) ## 👋 Hello world! - 한양대학교 ERICA 소프트웨어학부 19학번 (2019.03.02 ~ ) - 대한민국 공군 ROKAF 병 825기 정보체계관리(30010 과정) (2021.04.12 ~ 2023.01.11) - GiftMusic backend 개발자 (2020.09 ~ 2021.04) ## 🧑🏻‍💻 My Projects - [Follow Link Here](https://github.com/bnbong/bnbong.github.io) ## 💻 My Stacks - Language & Frameworks <div> <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=C&logoColor=white"/> <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=flat-sqaure&logo=c%2B%2B&logoColor=white"/> <img src="https://img.shields.io/badge/Java-F7DF1E?style=flat-square&logo=Java&logoColor=black"/> <img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=r&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/firebase-ffca28?style=flat-square&logo=firebase&logoColor=black"/> <img src="https://img.shields.io/badge/Junit5-25A162?style=flat-square&logo=junit5&logoColor=white"/> <img src="https://img.shields.io/badge/JWT-000000?style=flat-square&logo=JSON%20web%20tokens&logoColor=white"/> <img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white"/> <img src="	https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=Postman&logoColor=white"/> <img src="https://img.shields.io/badge/Android%20Studio-FFFFFF?style=flat-square&logo=Android%20Studio"/> </div> - Databases & Devops <div> <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=flat-square&logo=MongoDB&logoColor=white"/> <img src="https://img.shields.io/badge/Mysql-005C84?style=flat-square&logo=MySql&logoColor=white"/> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=PostgreSQL&logoColor=white"/> <img src="https://img.shields.io/badge/elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white"/> <img src="https://img.shields.io/badge/SQLite-07405E?style=flat-square&style=for-the-badge&logo=sqlite&logoColor=white"/> <img src="https://img.shields.io/badge/Github-092E20?style=flat-square&logo=Github&logoColor=white"/> <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=Git&logoColor=white"/> <img src="https://img.shields.io/badge/Jira-0052CC?style=flat-square&logo=Jira&logoColor=white"/> <img src="https://img.shields.io/badge/Jenkins-D24939?style=flat-sqaure&logo=Jenkins&logoColor=white"/> </div> - IDE <div> <img src="https://img.shields.io/badge/Eclipse-2C2255?style=flat-square&logo=eclipse&logoColor=white"/> <img src="https://img.shields.io/badge/IntelliJ_IDEA-000000.svg?style=flat-square&logo=intellij-idea&logoColor=white"/> <img src="	https://img.shields.io/badge/PyCharm-000000.svg?&style=flat-square&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/RStudio-75AADB?style=flat-sqaure&logo=RStudio&logoColor=white"/> <img src="https://img.shields.io/badge/VIM-%2311AB00.svg?&style=flat-square&logo=vim&logoColor=white"/> <img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=flat-square&logo=visual%20studio%20code&logoColor=white"/> </div> ## 👀 I’m interested in ... - Python Django 프레임워크 등을 이용한 웹 백앤드 개발 - React, Vue.js 등을 이용한 웹 프론트앤드 개발 - 음악과 관련된 웹 또는 앱 개발 - 게임 개발 - 딥러닝 등의 AI 기술 ## 🌱 I’m currently learning ... - GoLang - JavaScript, Html - Django & MongoDB를 활용한 사이트 혹은 백앤드 개발 - Algorithms (implemented with Python) ## 💞️ I’m looking to collaborate on ... - 웹 백앤드 및 프론트앤드 개발 능력이 있으신 분 - 컨텐츠 기획에 풍부한 경험이 있으신 분 - 게임 프로그래머 이시거나 게임 프로그래밍을 해보신 분 ## 📫 How to reach me ... - MY WEBSITE : <div> <a href="https://bnbongdevstory.tistory.com/"><img src="https://img.shields.io/badge/website-000000?style=flat-square&logo=About.me&logoColor=white"/></a>&nbsp </div> - EMAIL ME : <div> <a href="mailto:bbbong9@gmail.com"><img src="https://img.shields.io/badge/Gmail-d14836?style=flat-square&logo=Gmail&logoColor=white&link=bbbong9@gmail.com"/></a>&nbsp <a href="mailto:bnbong@naver.com"><img src="https://img.shields.io/badge/Naver-2DB400?style=flat-square&logo=Naver&logoColor=white&link=bnbong@naver.com"/></a>&nbsp </div> - Direct Message ME : <div> <a href="https://www.instagram.com/j_hyeok__lee/?hl=ko"><img src="https://img.shields.io/badge/Instagram-E4405F?style=flat-square&logo=Instagram&logoColor=white&link=https://www.instagram.com/j_hyeok__lee/?hl=ko"/></a>&nbsp <a href="https://www.facebook.com/profile.php?id=100007712465866"><img src="https://img.shields.io/badge/Facebook-3b5998?style=flat-square&logo=Facebook&logoColor=white&link=https://www.facebook.com/profile.php?id=100007712465866"/></a>&nbsp <a href="https://www.linkedin.com/in/%EC%A4%80%ED%98%81-%EC%9D%B4-669733231/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white"/></a>&nbsp </div> <br> ![footer](https://capsule-render.vercel.app/api?section=footer&type=waving&color=timeGradient) <!--- bnbong/bnbong is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile. You can click the Preview link to take a look at your changes. --->
    """
    notes = []
    date, time = (datetime.today().isoformat(timespec='seconds')).split('T')
    time_now = f'{date} {time}'
    notes.append(
        {"id":4, 
        "title":"About Me", 
        "created":time_now, 
        "content":markdown.markdown(content)}
        )
        
    return render_template('index.html', notes=notes)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
            return redirect(url_for('index'))

        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))

        conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# @app.route('/<int:id>/edit', methods=('GET', 'POST'))
# def edit(id):
#     pass

# @app.route('/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     pass

if __name__ == '__main__':
    app.run(debug=True)
