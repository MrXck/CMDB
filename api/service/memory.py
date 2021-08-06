from api import models
memory = {
    'RAM slot #0':
        {
            'capacity': 2048,
            'slot': 'RAM slot #0',
            'model': 'DRAM',
            'speed': 'Unknown',
            'manufacturer': 'Not Specified',
            'sn': 'Not Specified'
        },
    'RAM slot #1':
        {
            'capacity': 0,
            'slot': 'RAM slot #1',
            'model': 'DRAM'
        },
        'RAM slot #2':
        {
            'capacity': 0,
            'slot': 'RAM slot #2',
            'model': 'DRAM'
        },
        'RAM slot #3':
        {
            'capacity': 0,
            'slot': 'RAM slot #3',
            'model': 'DRAM'
        }
}


def process_memory_info(host_object, memory_dict):
    if not memory_dict['status']:
        return
    new_memory_dict = memory_dict['data']
    new_memory_set = set(new_memory_dict)

    db_memory_queryset = models.Memory.objects.filter(server=host_object).all()
    db_memory_dict = {row.slot: row for row in db_memory_queryset}
    db_memory_set = set(db_memory_dict)

    create_slot_set = new_memory_set - db_memory_set
    remove_slot_set = db_memory_set - new_memory_set
    update_slot_set = new_memory_set & db_memory_set

    record_str_list = []

    # 添加
    for slot in create_slot_set:
        models.Memory.objects.create(**new_memory_dict[slot], server=host_object)
        msg = '【新增内存】capacity：{capacity}-slot：{slot}-model：{model}-speed：{speed}-manufacturer：{manufacturer}-sn：{sn}'.format(**new_memory_dict[slot])
        record_str_list.append(msg)

    # 删除
    models.Memory.objects.filter(server=host_object, slot__in=remove_slot_set).delete()
    if remove_slot_set:
        msg = '【删除内存】slot：{}\n'.format(','.join(remove_slot_set))
        record_str_list.append(msg)

    # 更新
    for slot in update_slot_set:
        temp = []
        for key, value in new_memory_dict[slot].items():
            old_value = getattr(db_memory_dict[slot], key)
            if str(value) != old_value:
                msg = '内存的{}，由{}变更成了{};'.format(key, old_value, value)
                setattr(db_memory_dict[slot], key, value)
                temp.append(msg)
        if temp:
            db_memory_dict[slot].save()
            row = '【更新内存】slot：{},更新的内容：{}'.format(slot, ';'.join(temp))
            record_str_list.append(row)
    if record_str_list:
        models.AssetsRecord.objects.create(content='\n'.join(record_str_list), server=host_object)



