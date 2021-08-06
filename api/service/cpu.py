from api import models


def process_cpu_info(host_object, cpu_dict):
    if not cpu_dict['status']:
        return

    new_cpu_dict = {cpu_dict['data']['cpu_model']: cpu_dict['data']}
    new_cpu_set = set(new_cpu_dict)

    db_cpu_queryset = models.Server.objects.filter(hostname=host_object.hostname).all()
    db_cpu_dict = {row.cpu_model: row for row in db_cpu_queryset}
    db_cpu_set = set(db_cpu_dict)

    update_cpu_set = new_cpu_set - db_cpu_set

    record_str_list = []

    # 更新
    for i in update_cpu_set:
        models.Server.objects.filter(hostname=host_object.hostname).update(**new_cpu_dict[i])
        msg = '【更新cpu】cpu_count：{cpu_count}-cpu_physical_count：{cpu_physical_count}-cpu_model：{cpu_model}'.format(**new_cpu_dict[i])
        record_str_list.append(msg)

    if record_str_list:
        models.AssetsRecord.objects.create(content='\n'.join(record_str_list), server=host_object)


