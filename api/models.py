from django.db import models


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)


class BusinessUnit(models.Model):
    name = models.CharField(verbose_name='业务线', max_length=64, unique=True)


class IDC(models.Model):
    name = models.CharField(verbose_name='机房', max_length=32)
    floor = models.IntegerField(verbose_name='楼层', default=1)


class Server(models.Model):
    hostname = models.CharField(verbose_name='主机名', max_length=32)
    last_date = models.DateField(verbose_name='最近汇报时间', null=True, blank=True)

    status_choice = (
        (1, '上线'),
        (2, '下线'),
    )
    status = models.IntegerField(verbose_name='状态', choices=status_choice, default=1)

    business_unit = models.ForeignKey(verbose_name='业务线', to='BusinessUnit', on_delete=models.CASCADE)

    idc = models.ForeignKey(verbose_name='机房', to='IDC', on_delete=models.CASCADE)
    cabinet_num = models.CharField(verbose_name='机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name='机柜中序号', max_length=30, null=True, blank=True)

    os_platform = models.CharField(verbose_name='系统', max_length=32, null=True, blank=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=32, null=True, blank=True)

    manufacturer = models.CharField(verbose_name='SN号', max_length=64, null=True, blank=True)
    model = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    sn = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)

    cpu_count = models.CharField(verbose_name='cpu个数', max_length=32, null=True, blank=True)
    cpu_physical_count = models.CharField(verbose_name='', max_length=32, null=True, blank=True)
    cpu_model = models.CharField(verbose_name='', max_length=32, null=True, blank=True)


class Disk(models.Model):
    slot = models.CharField(verbose_name='槽位', max_length=16)
    pd_type = models.CharField(verbose_name='类型', max_length=16)
    capacity = models.CharField(verbose_name='容量', max_length=64)
    model = models.CharField(verbose_name='型号', max_length=64)
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)


class AssetsRecord(models.Model):
    content = models.TextField(verbose_name='内容')
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='时间', auto_now_add=True)


class Nic(models.Model):
    name = models.CharField(verbose_name='网卡名称', max_length=128, default='null')
    address = models.CharField(verbose_name='ip地址', max_length=32)
    netmask = models.CharField(verbose_name='子网掩码', max_length=32)
    broadcast = models.CharField(verbose_name='', max_length=32)
    hwaddr = models.CharField(verbose_name='网卡mac地址', max_length=32)
    up = models.BooleanField(default=False)
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)


class Memory(models.Model):
    capacity = models.CharField(verbose_name='容量', max_length=32)
    slot = models.CharField(verbose_name='插槽位', max_length=32)
    model = models.CharField(verbose_name='型号', max_length=32)
    speed = models.CharField(verbose_name='速度', max_length=32)
    manufacturer = models.CharField(verbose_name='制造商', max_length=32)
    sn = models.CharField(verbose_name='内存SN号', max_length=32)
    server = models.ForeignKey(verbose_name='服务器', to='Server', on_delete=models.CASCADE)
