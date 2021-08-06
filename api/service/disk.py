from api import models


def process_disk_info1(host_obj, disk_dict):
    hostname = host_obj.id
    disk_obj_list = models.Disk.objects.filter(server__hostname=hostname)
    if disk_obj_list:
        disk_obj_dict = {}
        for disk_obj in disk_obj_list:
            if disk_obj.slot not in disk_dict:
                disk_obj.delete()
                continue
            disk_obj_dict[disk_obj.slot] = disk_obj
        for i in disk_dict:
            if i not in disk_obj_dict:
                models.Disk.objects.create(**disk_dict[i], server=host_obj)
            else:
                disk_obj = disk_obj_dict[i]
                disk_info = disk_dict[i]
                if disk_obj.pd_type != disk_info['pd_type']:
                    disk_obj.pd_type = disk_info['pd_type']
                if disk_obj.capacity != disk_info['capacity']:
                    disk_obj.capacity = disk_info['capacity']
                if disk_obj.model != disk_info['model']:
                    disk_obj.model = disk_info['model']
                disk_obj.save()
    else:
        for i in disk_dict:
            models.Disk.objects.create(**disk_dict[i], server=host_obj)


def process_disk_info(host_object, disk_dict):
    if not disk_dict['status']:
        return
    new_disk_dict = disk_dict['data']
    new_disk_slot_set = set(new_disk_dict)

    db_disk_queryset = models.Disk.objects.filter(server=host_object).all()
    db_disk_dict = {row.slot: row for row in db_disk_queryset}
    db_disk_slot_set = set(db_disk_dict)

    create_slot_set = new_disk_slot_set - db_disk_slot_set
    remove_slot_set = db_disk_slot_set - new_disk_slot_set
    update_slot_set = new_disk_slot_set & db_disk_slot_set

    record_str_list = []

    # 添加
    for slot in create_slot_set:
        models.Disk.objects.create(**new_disk_dict[slot], server=host_object)
        msg = '【新增硬盘】槽位：{slot}-类型：{pd_type}-容量：{capacity}-模式：{model}'.format(**new_disk_dict[slot])
        record_str_list.append(msg)

    # 删除
    models.Disk.objects.filter(server=host_object, slot__in=remove_slot_set).delete()
    if remove_slot_set:
        msg = '【删除硬盘】槽位：{}\n'.format(','.join(remove_slot_set))
        record_str_list.append(msg)

    # 更新
    for slot in update_slot_set:
        temp = []
        for key, value in new_disk_dict[slot].items():
            old_value = getattr(db_disk_dict[slot], key)
            if value != old_value:
                msg = '硬盘的{}，由{}变更成了{};'.format(key, old_value, value)
                setattr(db_disk_dict[slot], key, value)
                temp.append(msg)
        if temp:
            db_disk_dict[slot].save()
            row = '【更新硬盘】槽位：{},更新的内容：{}'.format(slot, ';'.join(temp))
            record_str_list.append(row)
    if record_str_list:
        models.AssetsRecord.objects.create(content='\n'.join(record_str_list), server=host_object)
