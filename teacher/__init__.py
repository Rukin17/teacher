
from flask import Flask, render_template, request
from teacher.model import db, Student, Group


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)


    @app.route('/')
    def hello_teacher():
        return render_template('menu.html')
    

    @app.route('/class', methods=('POST', 'GET'))
    def students_in_class():
        return render_template('class.html', title='Класс')
    

    @app.route('/edit_journal', methods=('POST', 'GET'))
    def edit_journal():
        if request.method == 'POST':
            #TODO проверка корректности данных
            try:
                group = Group.query.filter(Group.group_name == request.form['group_name']).first()

                if group:
                    # если класс существует, привязываем Студента к существующему классу
                    student = Student(fullname=request.form['fullname'], group_id=group.id)         
                    db.session.add(student)
                    
                else:
                    # Иначе создаем новый класс и привязываем к нему Студента
                    new_group = Group(group_name=request.form['group_name'])
                    db.session.add(new_group)
                    db.session.flush()

                    group = Group.query.filter(Group.group_name == request.form['group_name']).first()

                    student = Student(fullname=request.form['fullname'], group_id=group.id)
                    db.session.add(student)
                 
                db.session.commit()
            
            except:
                db.session.rollback()
                print('Ошибка добавления в БД')

        return render_template('edit_journal.html', title='Добавить студента')
    

    return app