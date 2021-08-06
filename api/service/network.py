from api import models


def process_network_info(host_object, network_dict):
    if not network_dict['status']:
        return
    network_name_set = set(network_dict['data'])
    new_network_dict = {}
    for network_name in network_name_set:
        for inet in network_dict['data'][network_name]['inet']:
            new_network_dict[inet['address']] = {'name': network_name, 'address': inet['address'], 'netmask': inet['netmask'], 'broadcast': inet['broadcast'], 'hwaddr': network_dict['data'][network_name]['hwaddr'], 'up': network_dict['data'][network_name]['up']}
    new_network_set = set(new_network_dict)
    db_network_queryset = models.Nic.objects.filter(server=host_object)
    db_network_dict = {row.address: row for row in db_network_queryset}
    db_network_set = set(db_network_dict)

    create_network_set = new_network_set - db_network_set
    remove_network_set = db_network_set - new_network_set
    update_network_set = new_network_set & db_network_set

    record_str_list = []

    # 添加
    for i in create_network_set:
        models.Nic.objects.create(**new_network_dict[i], server=host_object)
        msg = '【新增网卡】address：{address}-hwaddr：{hwaddr}-netmask：{netmask}-broadcast：{broadcast}'.format(**new_network_dict[i])
        record_str_list.append(msg)

    # 删除
    models.Nic.objects.filter(server=host_object, address__in=remove_network_set).delete()
    if remove_network_set:
        msg = '【删除网卡】hwaddr：{}\n'.format(','.join(remove_network_set))
        record_str_list.append(msg)

    # 更新
    for i in update_network_set:
        temp = []
        for key, value in new_network_dict[i].items():
            old_value = getattr(db_network_dict[i], key)
            if value != old_value:
                msg = '网卡的{}，由{}变更成了{};'.format(key, old_value, value)
                setattr(db_network_dict[i], key, value)
                temp.append(msg)
        if temp:
            db_network_dict[i].save()
            row = '【更新网卡】hwaddr：{},更新的内容：{}'.format(i, ';'.join(temp))
            record_str_list.append(row)

    if record_str_list:
        models.AssetsRecord.objects.create(content='\n'.join(record_str_list), server=host_object)

