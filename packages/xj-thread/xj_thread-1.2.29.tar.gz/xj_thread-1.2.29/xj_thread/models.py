import socket

from django.db import models
from django.utils import timezone
from DjangoUeditor.models import UEditorField

# from apps.user.models import User
# from apps.user.models import BaseInfo

hostname = socket.gethostname()
my_ip_addr = socket.gethostbyname(hostname)


class ThreadShow(models.Model):
    """
    2、Thread_ThreadShow 展示类型表
    展示类型。用于对前端界面的显示样式进行分类
    """

    class Meta:
        db_table = 'thread_show'
        verbose_name_plural = '13. 展示类型表 (样式)'

    id = models.AutoField(verbose_name='展示类型ID', primary_key=True, help_text='')
    value = models.CharField(verbose_name='值', max_length=50, help_text='')
    config = models.JSONField(verbose_name='前端配置', blank=True, null=True, default=list, help_text='')  # 用于存放前端自定义的界面或样式相关的配置数据
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.value}"


class ThreadCategory(models.Model):
    """
    3、Thread_ThreadCategory 主类别表
    类别。类似于版块大类的概念，用于圈定信息内容所属的主要类别
    """

    class Meta:
        db_table = 'thread_category'
        verbose_name_plural = '11. 类别表 (页面类别)'

    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    value = models.CharField(verbose_name='值', max_length=50, help_text='')
    need_auth = models.IntegerField(verbose_name="是否需要权限", default=True, choices=((1, "是"), (0, "否")))
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    parent_id = models.IntegerField(verbose_name='父类别ID', null=True, blank=True, help_text='')

    def __str__(self, help_text=''):
        return f"{self.value}"


class ThreadClassify(models.Model):
    """
    4、Thread_ThreadClassify 分类表
    @brief 分类。具体的分类，可以是按行业、兴趣、学科的分类，是主类别下的子分类。
    @note 考虑到多语言翻译的问题，不需要写接口，由运维在后台添加
    """

    class Meta:
        db_table = 'thread_classify'
        verbose_name_plural = '12. 分类表 (行业分类)'

    id = models.AutoField(verbose_name='分类ID', primary_key=True)
    # key = models.CharField(verbose_name='分类关键字', max_length=50, blank=True, null=True, help_text='')
    value = models.CharField(verbose_name='分类', max_length=50, unique=True, help_text='')
    show = models.ForeignKey(verbose_name='默认展示ID', to=ThreadShow, db_column='show_id', related_name='+',
                             on_delete=models.DO_NOTHING, null=True, blank=True, default=1, help_text='')
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    category = models.ForeignKey(verbose_name='父类别', to=ThreadCategory, db_column='category_id', related_name='+',
                                 on_delete=models.DO_NOTHING, blank=True, null=True, help_text='')
    icon = models.CharField(verbose_name='图标', max_length=255, blank=True, null=True, help_text='')

    def __str__(self, help_text=''):
        return f"{self.value}"


# 访问权限。作者指定允许哪里用户可以访问，例如私有、公开、好友、指定某些人可以访问等。
class ThreadAuth(models.Model):
    class Meta:
        db_table = 'thread_auth'
        verbose_name_plural = '权限类型表'

    id = models.AutoField(verbose_name='ID', primary_key=True)
    value = models.CharField(verbose_name='值', max_length=50)

    def __str__(self):
        return f"{self.value}"


# 扩展字段数据表。用于扩展一些自定义的版块功能的数据
class ThreadExtendData(models.Model):
    """ 6、Thread_ThreadExtendData 扩展字段数据表 """

    class Meta:
        db_table = 'thread_extend_data'
        verbose_name_plural = '扩展字段数据表'

    # id = models.AutoField(verbose_name='信息ID', primary_key=True, help_text='')
    thread_id = models.OneToOneField('Thread', related_name="thread_extend_data", db_column='thread_id',
                                     primary_key=True, on_delete=models.DO_NOTHING, help_text='')
    field_1 = models.CharField(verbose_name='field_1', max_length=255, blank=True, null=True, help_text='')
    field_2 = models.CharField(verbose_name='field_2', max_length=255, blank=True, null=True, help_text='')
    field_3 = models.CharField(verbose_name='field_3', max_length=255, blank=True, null=True, help_text='')
    field_4 = models.CharField(verbose_name='field_4', max_length=255, blank=True, null=True, help_text='')
    field_5 = models.CharField(verbose_name='field_5', max_length=255, blank=True, null=True, help_text='')
    field_6 = models.CharField(verbose_name='field_6', max_length=255, blank=True, null=True, help_text='')
    field_7 = models.CharField(verbose_name='field_7', max_length=255, blank=True, null=True, help_text='')
    field_8 = models.CharField(verbose_name='field_8', max_length=255, blank=True, null=True, help_text='')
    field_9 = models.CharField(verbose_name='field_9', max_length=255, blank=True, null=True, help_text='')
    field_10 = models.CharField(verbose_name='field_10', max_length=255, blank=True, null=True, help_text='')
    field_11 = models.CharField(verbose_name='field_11', max_length=255, blank=True, null=True, help_text='')
    field_12 = models.CharField(verbose_name='field_12', max_length=255, blank=True, null=True, help_text='')
    field_13 = models.CharField(verbose_name='field_13', max_length=255, blank=True, null=True, help_text='')
    field_14 = models.CharField(verbose_name='field_14', max_length=255, blank=True, null=True, help_text='')
    field_15 = models.CharField(verbose_name='field_15', max_length=255, blank=True, null=True, help_text='')
    field_16 = models.CharField(verbose_name='field_16', max_length=255, blank=True, null=True, help_text='')
    field_17 = models.CharField(verbose_name='field_17', max_length=255, blank=True, null=True, help_text='')
    field_18 = models.CharField(verbose_name='field_18', max_length=255, blank=True, null=True, help_text='')
    field_19 = models.CharField(verbose_name='field_19', max_length=255, blank=True, null=True, help_text='')
    field_20 = models.CharField(verbose_name='field_20', max_length=255, blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.thread_id}"

    def short_field_1(self):
        if self.field_1 and len(self.field_1) > 25:
            return "{}......".format(self.field_1[0:25])
        return self.field_1

    def short_field_2(self):
        if self.field_2 and len(self.field_2) > 25:
            return "{}......".format(str(self.field_2)[0:25])
        return self.field_2

    def short_field_3(self):
        if self.field_3 and len(self.field_3) > 25:
            return "{}......".format(str(self.field_3)[0:25])
        return self.field_3

    def short_field_4(self):
        if self.field_4 and len(self.field_4) > 25:
            return "{}......".format(str(self.field_4)[0:25])
        return self.field_4

    def short_field_5(self):
        if self.field_5 and len(self.field_5) > 25:
            return "{}......".format(str(self.field_5)[0:25])
        return self.field_5

    def short_field_6(self):
        if self.field_6 and len(self.field_6) > 25:
            return "{}......".format(str(self.field_6)[0:25])
        return self.field_6

    def short_field_7(self):
        if self.field_7 and len(self.field_7) > 25:
            return "{}......".format(str(self.field_7)[0:25])
        return self.field_7

    def short_field_8(self):
        if self.field_8 and len(self.field_8) > 25:
            return "{}......".format(str(self.field_8)[0:25])
        return self.field_8

    def short_field_9(self):
        if self.field_9 and len(self.field_9) > 25:
            return "{}......".format(str(self.field_9)[0:25])
        return self.field_9

    def short_field_10(self):
        if self.field_10 and len(self.field_10) > 25:
            return "{}......".format(str(self.field_10)[0:25])
        return self.field_10

    def short_field_11(self):
        if self.field_11 and len(self.field_11) > 25:
            return "{}......".format(str(self.field_11)[0:25])
        return self.field_11

    def short_field_12(self):
        if self.field_12 and len(self.field_12) > 25:
            return "{}......".format(str(self.field_12)[0:25])
        return self.field_12

    def short_field_13(self):
        if self.field_13 and len(self.field_13) > 25:
            return "{}......".format(str(self.field_13)[0:25])
        return self.field_13

    def short_field_14(self):
        if self.field_14 and len(self.field_14) > 25:
            return "{}......".format(str(self.field_14)[0:25])
        return self.field_14

    def short_field_15(self):
        if self.field_15 and len(self.field_15) > 25:
            return "{}......".format(str(self.field_15)[0:25])
        return self.field_15

    def short_field_16(self):
        if self.field_16 and len(self.field_16) > 25:
            return "{}......".format(str(self.field_16)[0:25])
        return self.field_16

    def short_field_17(self):
        if self.field_17 and len(self.field_17) > 25:
            return "{}......".format(str(self.field_17)[0:25])
        return self.field_17

    def short_field_18(self):
        if self.field_18 and len(self.field_18) > 25:
            return "{}......".format(str(self.field_18)[0:25])
        return self.field_18

    def short_field_19(self):
        if self.field_19 and len(self.field_19) > 25:
            return "{}......".format(str(self.field_19)[0:25])
        return self.field_19

    def short_field_20(self):
        if self.field_20 and len(self.field_20) > 25:
            return "{}......".format(self.field_20[0:25])
        return self.field_20


# 扩展字段表。用于声明扩展字段数据表中的(有序)字段具体对应的什么键名。注意：扩展字段是对分类的扩展，而不是主类别的扩展
class ThreadExtendField(models.Model):
    """  7、Thread_ThreadExtendField 扩展字段表 """

    class Meta:
        db_table = 'thread_extend_field'
        verbose_name_plural = '扩展字段表'
        unique_together = (("category_id", "field"),)  # 组合唯一，分类+字段
        ordering = ['-category_id']

    id = models.AutoField(verbose_name='信息ID', primary_key=True, help_text='')

    # 数据库生成classify_id字段
    category_id = models.ForeignKey(verbose_name='类别ID', null=True, blank=True, to=ThreadCategory,
                                    db_column='category_id', related_name='+', on_delete=models.DO_NOTHING, help_text='')
    # classify_id = models.ForeignKey(verbose_name='分类ID', null=True, blank=True, to=ThreadClassify,
    #                                 db_column='classify_id', related_name='+', on_delete=models.DO_NOTHING, help_text='')
    field = models.CharField(verbose_name='自定义字段', max_length=255, help_text='')  # 眏射ThreadExtendData表的键名
    field_index = models.CharField(
        verbose_name='冗余字段',
        max_length=255,
        help_text='',
        choices=(
            ("field_1", "field_1"),
            ("field_2", "field_2"),
            ("field_3", "field_3"),
            ("field_4", "field_4"),
            ("field_5", "field_5"),
            ("field_6", "field_6"),
            ("field_7", "field_7"),
            ("field_8", "field_8"),
            ("field_9", "field_9"),
            ("field_10", "field_10"),
            ("field_11", "field_11"),
            ("field_12", "field_12"),
            ("field_13", "field_13"),
            ("field_14", "field_14"),
            ("field_15", "field_15"),
            ("field_16", "field_16"),
            ("field_17", "field_17"),
            ("field_18", "field_18"),
            ("field_19", "field_19"),
            ("field_20", "field_20"),
        )
    )  # 眏射ThreadExtendData表的键名
    value = models.CharField(verbose_name='字段介绍', max_length=255, null=True, blank=True, help_text='')
    type = models.CharField(verbose_name='字段类型', max_length=255, blank=True, null=True, help_text='')
    unit = models.CharField(verbose_name='参数单位', max_length=255, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='字段配置', blank=True, null=True, default=dict, help_text='')

    def __str__(self):
        return f"{self.id}"


class Thread(models.Model):
    """  1、Thread_Thread 信息主表 """

    class Meta:
        ordering = ['-create_time']
        db_table = 'thread'  # 指定数据库的表名，否则默认会显示app名+class名。
        verbose_name_plural = '01. 信息表'  # 指定管理界面的别名，否则默认显示class名。末尾不加s。

    id = models.BigAutoField(verbose_name='ID', primary_key=True, help_text='')
    is_deleted = models.BooleanField(verbose_name='是否删除', default=False, help_text='')
    category_id = models.ForeignKey(verbose_name='类别ID', to=ThreadCategory, default=1, db_column='category_id', on_delete=models.DO_NOTHING, help_text='')
    classify_id = models.ForeignKey(verbose_name='分类ID', to=ThreadClassify, db_column='classify_id', on_delete=models.DO_NOTHING, null=True, blank=True, help_text='')
    show = models.ForeignKey(verbose_name='展示ID', to=ThreadShow, default=1, db_column='show_id', null=True, blank=True, on_delete=models.DO_NOTHING, related_name='+',
                             help_text='如果没有传入显示类型，则使用分类表中的默认显示类型')  # 如果没有传入显示类型，则使用分类表中的默认显示类型
    user_id = models.BigIntegerField(verbose_name='用户ID', db_index=True, help_text='')
    auth_id = models.ForeignKey(verbose_name='权限ID', to=ThreadAuth, db_column='auth_id', default=1, related_name='+', on_delete=models.DO_NOTHING, help_text='')
    title = models.CharField(verbose_name='标题', max_length=255, blank=True, null=True, db_index=True, help_text='')
    subtitle = models.CharField(verbose_name='子标题', max_length=255, blank=True, null=True, db_index=True, help_text='')
    content = UEditorField(verbose_name='内容', blank=True, null=True, help_text='信息列表页是不返回内容字段的，因为这会增加数据的体积')
    summary = models.CharField(verbose_name='摘要', max_length=1024, blank=True, null=True, default="", help_text='')
    author = models.CharField(verbose_name='作者', max_length=255, blank=True, null=True, help_text='')  # add-2022-05-20
    ip = models.GenericIPAddressField(verbose_name='IP地址', protocol='both', default=socket.gethostbyname(socket.gethostname()))  # 只记录创建时的IP
    has_enroll = models.BooleanField(verbose_name='开启报名', default=False, help_text='')
    has_fee = models.BooleanField(verbose_name='开启小费', default=False, help_text='')
    has_comment = models.BooleanField(verbose_name='开启评论', default=True, help_text='')
    cover = models.CharField(verbose_name='封面', max_length=1024, blank=True, null=True, help_text='')
    photos = models.JSONField(verbose_name='照片集', blank=True, null=True, help_text='')  # 对象数组，存放{id, url} 获取列表时使用，查看详细时再匹配资源表
    video = models.CharField(verbose_name='视频', max_length=1024, blank=True, null=True, help_text='')
    files = models.JSONField(verbose_name='文件集', blank=True, null=True, help_text='')  # 对象数组，存放{id, url}
    price = models.DecimalField(verbose_name='价格', max_digits=32, decimal_places=8, db_index=True, null=True, blank=True, help_text='')  # add-2022-05-20
    is_original = models.BooleanField(verbose_name='是否原创', default=True, help_text='')  # add-2022-05-20
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now, help_text='')
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, help_text='')  # 不显示，系统自动填。
    logs = models.JSONField(verbose_name='日志', blank=True, null=True, default=list, help_text='')  # 用户的修改记录等日志信息，数组对象类型 使用CRC32来比较哪些字段被修改过，并记录
    more = models.JSONField(verbose_name='更多信息', blank=True, null=True, help_text='')

    def __str__(self):
        return f"({self.id}{self.title})"

    # 判断指定字段长度,超出部分用省略号代替
    def short_content(self):
        if len(str(self.content)) > 50:
            return '{}...'.format(str(self.content)[0:50])
        else:
            return str(self.content)

    # 字段数据处理后,字段verbose_name参数失效
    # 需要重新指定,否则列表页字段名显示的是方法名(short_content)
    short_content.short_description = '内容'

    def short_cover(self):
        if len(str(self.cover)) > 15:
            return '{}...'.format(str(self.cover)[0:15])
        else:
            return str(self.cover)

    short_cover.short_description = '封面'

    def short_video(self):
        if len(str(self.video)) > 15:
            return '{}...'.format(str(self.video)[0:15])
        else:
            return str(self.video)

    short_video.short_description = '视频'

    def short_photos(self):
        if len(str(self.photos)) > 15:
            return '{}...'.format(str(self.photos)[0:15])
        else:
            return str(self.photos)

    short_photos.short_description = '照片集'

    def short_files(self):
        if len(str(self.files)) > 15:
            return '{}...'.format(str(self.files)[0:15])
        else:
            return str(self.files)

    short_files.short_description = '文件集'

    def short_logs(self):
        if len(str(self.logs)) > 15:
            return '{}...'.format(str(self.logs)[0:15])
        else:
            return str(self.logs)

    short_logs.short_description = '日志'

    def short_more(self):
        if len(str(self.more)) > 30:
            return '{}...'.format(str(self.more)[0:30])
        else:
            return str(self.logs)

    short_more.short_description = '更多信息'


class ThreadStatistic(models.Model):
    """ 10、Thread_ThreadStatistic 信息统计表 """
    thread_id = models.BigIntegerField(verbose_name='信息主表', primary_key=True, db_column="thread_id", help_text='')
    flag_classifies = models.CharField(verbose_name='分类**', max_length=255, null=True, blank=True, help_text='')
    flag_weights = models.CharField(verbose_name='权重**', max_length=255, null=True, blank=True, help_text='')
    weight = models.FloatField(verbose_name='权重', default=0, db_index=True, help_text='')
    views = models.IntegerField(verbose_name='浏览数', default=0, help_text='')
    plays = models.IntegerField(verbose_name='完阅数', default=0, help_text='')
    comments = models.IntegerField(verbose_name='评论数', default=0, help_text='')
    likes = models.IntegerField(verbose_name='点赞数', default=0, help_text='')
    favorite = models.IntegerField(verbose_name='收藏数', default=0, help_text='')
    shares = models.IntegerField(verbose_name='分享数', default=0, help_text='')

    class Meta:
        db_table = 'thread_statistic'
        verbose_name = '信息统计表'
        verbose_name_plural = verbose_name


class ThreadTag(models.Model):
    """
    8、Thread_ThreadTag 标签类型表
    标签类型，存放预置标签。用于智能化推送信息，以及关键字检索。未来应设计成根据信息内容自动生成标签。
    """

    class Meta:
        db_table = 'thread_tag'
        verbose_name_plural = '标签类型表'

    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    value = models.CharField(verbose_name='标签名', max_length=255, blank=True, null=True, help_text='')
    thread = models.ManyToManyField(to='Thread', through='ThreadTagMapping', through_fields=('tag_id', 'thread_id'), blank=True, help_text="")

    def __str__(self):
        return f"{self.value}"


class ThreadTagMapping(models.Model):
    """
    9、Thread_ThreadTagMapping 标签映射表
    标签映射，存放数据。即将标签和信息关联起来 """

    class Meta:
        db_table = 'thread_tag_mapping'
        verbose_name_plural = '标签映射表'

    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    thread_id = models.ForeignKey(verbose_name='信息ID', to=Thread, db_column='thread_id', related_name='+',
                                  on_delete=models.DO_NOTHING, help_text='')
    tag_id = models.ForeignKey(verbose_name='标签ID', to=ThreadTag, db_column='tag_id', related_name='+',
                               on_delete=models.DO_NOTHING, help_text='')

    def __str__(self):
        return f"{self.id}"


class ThreadImageAuth(models.Model):
    """
    9、Thread_ThreadTagMapping 图片权限表
    图片权限。作者可以指定上传的图片的访问权限。如公开照片、阅后即焚、已焚毁、红包、红包阅后即焚、红包阅后已焚毁
    """

    class Meta:
        db_table = 'thread_image_auth'
        verbose_name_plural = '图片权限表'

    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    value = models.CharField(verbose_name='值', max_length=255, blank=True, null=True, help_text='')


# 图片信息表。用于存放图片的各种信息，存放图片地址但不存放图。
class ThreadResource(models.Model):
    class Meta:
        db_table = 'thread_resource'
        verbose_name_plural = '图片表'

    id = models.BigIntegerField(verbose_name='ID', primary_key=True, help_text='')
    name = models.CharField(verbose_name='图片名称', max_length=255, null=True, blank=True, help_text='')
    url = models.CharField(verbose_name='图片链接', max_length=1024, null=True, blank=True, help_text='')
    filename = models.CharField(verbose_name='文件名', max_length=255, null=True, blank=True, help_text='')
    filetype = models.SmallIntegerField(verbose_name='文件类型', null=True, blank=True, help_text='')  # 文件类型0:图片，1:视频，2:文件
    format = models.CharField(verbose_name='文件格式', max_length=50, help_text='')
    image_auth_id = models.ForeignKey(verbose_name='图片权限ID', to=ThreadImageAuth, db_column='image_auth_id',
                                      related_name='+', on_delete=models.DO_NOTHING, null=True, blank=True, help_text='')
    price = models.DecimalField(verbose_name='价格', max_digits=32, decimal_places=8, db_index=True, null=True,
                                blank=True, help_text='')
    snapshot = models.JSONField(verbose_name='快照', blank=True, null=True, help_text='')  # 存放图片的快照数据，如缩略图等。json对象
    logs = models.JSONField(verbose_name='日志', blank=True, null=True, help_text='')  # 用于存放点击量，点赞量等,数组对象
    # user_id = models.ForeignKey(verbose_name='用户ID', to=User, db_column='user_id', related_name='+', on_delete=models.DO_NOTHING)
    user_id = models.BigIntegerField(verbose_name='用户ID', help_text='')
    thread = models.ManyToManyField(to='Thread', through='ThreadToResource',
                                    through_fields=('resource_id', 'thread_id'), blank=True, help_text='')


# 标签映射，存放数据。即将标签和信息关联起来
class ThreadToResource(models.Model):
    class Meta:
        db_table = 'thread_to_resource'
        verbose_name_plural = '图文关联表'

    id = models.AutoField(verbose_name='ID', primary_key=True, help_text='')
    thread_id = models.ForeignKey(verbose_name='信息ID', to=Thread, db_column='thread_id', related_name='+',
                                  on_delete=models.DO_NOTHING, help_text='')
    resource_id = models.ForeignKey(verbose_name='图片ID', to=ThreadResource, db_column='resource_id', related_name='+',
                                    on_delete=models.DO_NOTHING, help_text='')
