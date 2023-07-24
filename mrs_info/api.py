from flask import Flask, request, render_template

from mrs_info.DiffUsers import DiffUsers
from mrs_info.ProjectInfo import ProjectInfo
from mrs_info.UserInfo import UserInfo, RoleInMrs, CreateMobile

app = Flask(__name__)


# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def userinfo():
    user_info = ""
    if request.method == 'POST':
        if 'submit_button' in request.form:
            print(request.form)
            user_id = request.form['user_id']
            mobile = request.form['mobile']
            nick = request.form['nick']
            db = request.form['env_db']

            user_info, user_id = UserInfo(nick=nick, user_id=user_id, mobile=mobile,
                                          db='mus_' + db).reUserid()  # 查询一个用户
            print(user_info)
            # user_info, user_id = u.reUserid()
            if user_id:
                user = RoleInMrs(user_id=user_id, db='pms_' + db)
                # u = UserInfo(user_id=i[0], db='mus_' + db)

                investor = user.isInvestor()
                user_info.update(investor)
                entrepreneur = user.isEntrepreneur()
                user_info.update(entrepreneur)
                investor_manager = user.isInvestorManager()
                user_info.update(investor_manager)
            # user_info = json.dumps(user_info, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        # print(user_info)
    return render_template("user.html", user_info=user_info)


# http://172.16.11.98/project?project_id=2003684587122695&db=pms_pre
# http://172.16.11.98/project?name=15624971711&db=pms_test
@app.route('/project')
def projectinfo():
    project_id = request.args.get('project_id')
    project_name = request.args.get('name')
    db = request.args.get('db')

    i = ProjectInfo(project_id=project_id, name=project_name)
    project = i.getProject()
    if project.get('code') == 0:
        project.update(i.hasDraftEntrepreneur())
        project.update(i.hasDraft())
        project.update(i.hasEntrepreneur())
        project.update(i.hasContact())
        project.update(i.hasFinancing())
        project.update(i.hasRoadShow())
        project.update(i.hasOnlineFinancing())
    # project = json.dumps(project, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
    print(project)
    return render_template("project.html", project=project)


@app.route('/diffusers', methods=['GET', 'POST'])
def getUsers():
    users = ""
    if request.method == 'POST':
        if 'submit_button' in request.form:
            print(request.form)
            user_type = request.form['user_type']
            user_nums = request.form['user_nums']
            db = request.form['env_db']
            print(db)
            if int(user_type) in range(0, 6):
                sql_result = DiffUsers(user_type=int(user_type), nums=user_nums, db='pms_' + db).getInfo()

                if sql_result:  # 根据这些user_id获取用户的信息
                    users = []
                    for i in sql_result:
                        u = UserInfo(user_id=i[0], db='mus_' + db)
                        user_info, user_id = u.reUserid()
                        if user_id:  # 注册的用户
                            user = RoleInMrs(user_id, 'pms_' + db)
                            investor = user.isInvestor()
                            user_info.update(investor)
                            entrepreneur = user.isEntrepreneur()
                            user_info.update(entrepreneur)
                            investor_manager = user.isInvestorManager()
                            user_info.update(investor_manager)
                        # if user_info['code'] == 0:  # 能根据user_id查询到结果的才显示出来
                        users.append(user_info)
                else:
                    users = [{"code": 9, "msg": "暂无该类型用户"}]

            elif int(user_type) == 999:
                users = []
                for i in range(0, int(user_nums)):
                    mobile, code = CreateMobile()  # 随机获取一个用户
                    u = UserInfo(mobile=mobile)
                    user_info, user_id = u.reUserid()
                    users.append(user_info)
    print(users)
    return render_template("getDiffUsers.html", user_info=users)


if __name__ == '__main__':
    app.run(host='172.17.13.67', port=80, debug=True)  # host 配置为本机地址，debug=True是调试模式
