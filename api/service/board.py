from api import models


def process_board_info(host_object, board_dict):
    if not board_dict['status']:
        return

    new_board_dict = {board_dict['data']['manufacturer']: board_dict['data']}
    new_board_set = set(new_board_dict)

    db_board_queryset = models.Server.objects.filter(hostname=host_object.hostname).all()
    db_board_dict = {row.manufacturer: row for row in db_board_queryset}
    db_board_set = set(db_board_dict)

    update_board_set = new_board_set - db_board_set

    record_str_list = []

    # 更新
    for i in update_board_set:
        models.Server.objects.filter(hostname=host_object.hostname).update(**new_board_dict[i])
        msg = '【更新board】manufacturer：{manufacturer}-model：{model}-sn：{sn}'.format(**new_board_dict[i])
        record_str_list.append(msg)

    if record_str_list:
        models.AssetsRecord.objects.create(content='\n'.join(record_str_list), server=host_object)
