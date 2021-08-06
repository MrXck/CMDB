from api import models


def process_basic_info(host_object, basic_dict):
    if not basic_dict['status']:
        return

    new_basic_dict = {basic_dict['data']['os_platform']: basic_dict['data']}
    new_basic_set = set(new_basic_dict)

    db_basic_queryset = models.Server.objects.filter(hostname=host_object.hostname).all()
    db_basic_dict = {row.os_platform: row for row in db_basic_queryset}
    db_basic_set = set(db_basic_dict)

    update_basic_set = new_basic_set - db_basic_set

    record_str_list = []

    # 更新
    for i in update_basic_set:
        models.Server.objects.filter(hostname=host_object.hostname).update(**new_basic_dict[i])
        msg = '【更新basic】os_platform：{os_platform}-os_version：{os_version}'.format(**new_basic_dict[i])
        record_str_list.append(msg)

    if record_str_list:
        models.AssetsRecord.objects.create(content='\n'.join(record_str_list), server=host_object)




