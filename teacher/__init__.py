
from flask import Flask, render_template, request, redirect, url_for
from teacher.model import db, Student, Group, Estimate, Course


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)


    @app.route('/')
    def hello_teacher():
        return render_template('menu.html')
    

    @app.route('/edit_journal', methods=('POST', 'GET'))
    def edit_journal():
        all = []
        try:
            all_students = Student.query.all()
            groups = Group.query.all()
        except:
            print('Ошибка чтения БД')

        return render_template('edit_journal.html', title='Редактировать журнал', all_students=all_students, groups=groups)
    

    @app.route('/add_student_and_class', methods=('POST', 'GET'))
    def add_student_and_class():
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

        return render_template('add_student_and_class.html', title='Добавить студента')
    

    @app.route('/delete_student', methods=('POST', 'GET'))
    def delete_student():
        if request.method == "POST":
            id = request.form['delete_student']
            student = db.get_or_404(Student, id)
            db.session.delete(student)
            db.session.commit()

        return render_template("delete_student.html", title='Удалить студента')

    
    @app.route('/add_course', methods=('POST', 'GET'))
    def add_course():
        if request.method == 'POST':
            course = Course(course_name=request.form['course'])         
            db.session.add(course)
            db.session.commit()

        return render_template('add_course.html', title='Добавить предмет') 
    

    @app.route('/journal', methods=('POST', 'GET'))
    def journal():
        groups = Group.query.all()
        if request.method == 'POST':
            group = request.form['group_name']
            if group:
                return redirect(f'/journal/{group}', code=302)
        return render_template('journal.html', title='Журнал', groups=groups)


    @app.route('/journal/<group>', methods=('POST', 'GET'))
    def get_group(group):
        group_in_database = Group.query.filter(Group.group_name == group).first()
        students = Student.query.filter(Student.group_id==group_in_database.id).all()
        courses = Course.query.all()
        return render_template('groups.html', group=group, students=students, courses=courses)   


    @app.route('/journal/<group>/<course>', methods=('POST', 'GET'))
    def get_estimates_table(group, course):
        group_in_database = Group.query.filter(Group.group_name == group).first()
        students = Student.query.filter(Student.group_id == group_in_database.id).all()
        course_in_database = Course.query.filter(Course.course_name == course).first()
        estimates = Estimate.query.filter(Estimate.course_id == course_in_database.id).all()

        return render_template('estimates.html', students=students, course=course, group=group, estimates=estimates)


    @app.route('/journal/<group>/<course>/add_estimate', methods=('POST', 'GET'))
    def add_estimate(group, course):
        group_in_database = Group.query.filter(Group.group_name == group).first()
        students = Student.query.filter(Student.group_id == group_in_database.id).all()
        if request.method == 'POST':
            course_in_database = Course.query.filter(Course.course_name == course).first()
            new_estimate = Estimate(estimate=request.form['estimate'], student_id=request.form['student_id'], course_id=course_in_database.id)
            db.session.add(new_estimate)
            db.session.commit()
            return  redirect(url_for('get_estimates_table', group=group, course=course))
        return render_template('add_estimate.html', students=students)
    

    return app

   