from django.http import HttpResponse
from django.shortcuts import render, redirect
from utils import sql_hp
import pymysql
import json
import time


def classes(request):
    tk = request.COOKIES.get('ticket')
    if not tk:
        return redirect('/login/')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035', db='stuManage', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'classes.html', {'class_list': class_list})


def add_class(request):
        if request.method == "GET":
            return render(request, 'add_class.html')
        else:
            # print(request.POST)
            v = request.POST.get('title')
            if len(v) > 0:
                conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035',
                                       db='stuManage', charset='utf8')
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                cursor.execute("insert into class(title) values(%s)", [v])
                conn.commit()
                cursor.close()
                conn.close()
                return redirect('/classes/')
            else:
                return render(request, 'add_student.html', {'msg': '班级名称不能为空'})


def del_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035', db='stuManage', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id = %s", [nid])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')


def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035',
                               db='stuManage', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class where id = %s", [nid])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(result)
        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.GET.get('nid')
        title = request.POST.get('title')

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035',
                               db='stuManage', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set title=%s where id=%s ", [title, nid])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/classes/')


def students(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035',
                           db='stuManage', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("SELECT student.id,student.name,student.class_id,class.title FROM student"
                   " LEFT JOIN class on student.class_id = class.id")
    student_list = cursor.fetchall()
    cursor.close()
    conn.close()

    class_list = sql_hp.get_list("select id,title from class", [])
    return render(request, 'students.html', {"student_list": student_list, "class_list": class_list})


def add_student(request):
    if request.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035',
                               db='stuManage', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT id,title from class")
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()

        return render(request, 'add_student.html', {'class_list': class_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='026035',
                               db='stuManage', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student(name,class_id) values(%s,%s)", [name, class_id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/students/')


def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        class_list = sql_hp.get_list("select id,title from class", [])
        current_student_info = sql_hp.get_one("select * from student where id=%s", [nid, ])
        return render(request, 'edit_student.html', {'class_list': class_list, 'current_student_info': current_student_info})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sql_hp.modify("update student set name=%s,class_id=%s where id=%s", [name, class_id, nid])
        return redirect('/students/')


# 对话框
def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        sql_hp.modify("insert into class(title) values(%s)", [title])
        return HttpResponse('ok')
    else:
        return HttpResponse("班级标题不能为空")
    #     return redirect('/classes/')
    # if len(title) > 0:
    #     sql_hp.modify("insert into class(title) values(%s)", [title])
    #     return redirect('/classes/')
    # else:
    #     pass


def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sql_hp.modify("update class set title=%s where id=%s", [content, nid])
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理异常"

    return HttpResponse(json.dumps(ret))


def modal_add_student(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sql_hp.modify("insert into student(name,class_id) values(%s,%s)", [name, class_id])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))


def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        sql_hp.modify("update student set `name`=%s,class_id=%s where id=%s  ", [name, class_id, nid])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return HttpResponse(json.dumps(ret))


def teachers(request):

    teacher_list = sql_hp.get_list("""
        SELECT teacher.id as tid,teacher.name, class.title from teacher
        left join teacher2class on teacher.id = teacher2class.teacher_id
        left join class on class.id = teacher2class.class_id""", [])
    result = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid] = {'tid': row['tid'], 'name': row['name'], 'titles': [row['title'], ]}

    return render(request, 'teachers.html', {'teacher_list': result.values()})


def add_teacher(request):
    if request.method == 'GET':
        class_list = sql_hp.get_list("select id,title from class", [])
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        name = request.POST.get('name')
        teacher_id = sql_hp.create("insert into teacher(name) value(%s)", [name, ])
        class_ids = request.POST.getlist('class_ids')
        print(name, class_ids)
        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id, cls_id)
            data_list.append(temp)
        obj = sql_hp.SqlHp()
        obj.multiple_modify("insert into teacher2class(teacher_id, class_id) values(%s, %s) ", data_list)
        obj.close()
        return redirect('/teachers/')


def edit_teacher(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        obj = sql_hp.SqlHp()
        teacher_info = obj.get_one("select id,name from teacher where id=%s", [nid, ])
        class_id_list = obj.get_list("select class_id from teacher2class where teacher_id=%s", [nid, ])
        class_list = obj.get_list("select id,title from class ", [])
        obj.close()

        temp = []
        for i in class_id_list:
            temp.append(i['class_id'])
        return render(request, 'edit_teacher.html', {
            'teacher_info': teacher_info, 'class_id_list': temp, 'class_list': class_list,
        })
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_ids = request.POST.getlist('class_ids')
        obj = sql_hp.SqlHp()
        obj.modify("update teacher set name=%s where id=%s", [name, nid])
        obj.modify("delete from teacher2class where teacher_id=%s", [nid])
        data_list = []
        for cls_id in class_ids:
            temp = (nid, cls_id)
            data_list.append(temp)
        obj = sql_hp.SqlHp()
        obj.multiple_modify("insert into teacher2class(teacher_id, class_id) values(%s, %s) ", data_list)
        obj.close()

        return redirect('/teachers/')


def get_all_class(request):
    time.sleep(0.5)
    obj = sql_hp.SqlHp()
    class_list = obj.get_list("select id,title from class", [])
    obj.close()
    return HttpResponse(json.dumps(class_list))


def modal_add_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id_list = request.POST.getlist('class_id_list')
        teachers_id = sql_hp.create("insert into teacher(name) values(%s)", [name])
        data_list = []
        for cls_id in class_id_list:
            temp = (teachers_id, cls_id)
            data_list.append(temp)
        obj = sql_hp.SqlHp()
        obj.multiple_modify("insert into teacher2class(teacher_id, class_id) values(%s, %s) ", data_list)
        obj.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理失败"
    return HttpResponse(json.dumps(ret))


def test(request):
    return render(request, 'test.html', )


def layout(request):
    return render(request, 'layout.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')

        if user == 'alex' and pwd == '123':
            obj = redirect('/classes/')
            obj.set_cookie('ticket', "ads")
            return obj
        else:
            return render(request, 'login.html')









