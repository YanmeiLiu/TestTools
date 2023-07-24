# 排序
from config.db import Mysql


def getSort(kind_value, sort='user_score'):
    sql = "select project_id from  project_kind_related " \
          "where kind_value = %d and project_id in (select id from project where state =1);" % kind_value
    sql_result = Mysql('yellowPageDB').select(sql)
    print('此次排序的长度是:{}'.format(len(sql_result)))
    project_lists = []
    if sql_result:
        for i in sql_result:
            project_id = i[0]
            project_lists.append(project_id)
        # print(project_lists)
        projects = ','.join('%s' % id for id in project_lists)
        print(projects)
        sql_sort = "select project_id,project_name,{}  from project_score where project_id in ({})  order by {} desc;".format(
            sort, projects, sort)
        sql_sort_result = Mysql('yellowPageDB').select(sql_sort)
        print('project_id, project_name,{} \n'.format(sort))
        for j in sql_sort_result:
            # sql_name = "select id,name from project where id =%d;" % j[0]
            # sql_name_result = Mysql('yellowPageDB').select(sql_name)
            print(j[0], ',', j[1], ',', j[2], '\n')

    else:
        print('无产品，无需排序')