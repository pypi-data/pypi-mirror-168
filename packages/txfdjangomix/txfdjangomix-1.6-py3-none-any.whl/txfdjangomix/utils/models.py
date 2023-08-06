import re
from django.db import models
from django.apps import apps


class BaseModel(models.Model):
    """基础的模型类,为其他表补存字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        abstract = True


def model_field_relation(app_name, model_name):
    """返回模型类对象信息
    app_name : 模型类models所在的文件夹的名称 str
    model_nam : 模型类的名称 str
    return (<django.db.models.fields.BigAutoField: id>, <django.db.models.fields.DateTimeField: create_time>)
    """
    model_obj = apps.get_model(app_name, model_name)
    filed = model_obj._meta.fields
    return filed


def name_attribute_relation(app_name, model_name, attribute_name='verbose_name', reverse=False):
    """
    :param attribute_name:  创建表字段的属性 如 verbose_name help_text max_length 等
    :param reverse: k v 互换
    :return:
        reverse=False
        {'id': 'ID', 'create_time': '创建时间', 'update_time': '更新时间', 'is_delete': 'is delete', 'tb_key': '字段名称', 'tb_value': '结果', 'tb_date': '时间', 'year_q': '年度季度标识', 'company_code': '公司编号'}
    """
    ret = {i.name: getattr(i, attribute_name) for i in model_field_relation(app_name, model_name)}
    if reverse:
        ret = {v: k for k, v in ret.items()}
    return ret


class AllModelDesc(object):
    """
    全部的表的解释说明
        all_desc
    单个字段的解释说明
    model_default
    model_choice
    model_type
    name_attribute_relation(参数attribute_name控制)
    """

    tables = ['default', 'verbose_name', 'help_text', 'null', 'choice', 'type']

    def model_default(self, app_name, model_name, attribute_name='default'):
        """
        默认值 没有就传空
        """
        ret_dcit = {}
        for i in model_field_relation(app_name, model_name):
            v = getattr(i, attribute_name)
            if isinstance(v, type):
                v = None
            ret_dcit[i.name] = v
        return ret_dcit

    def model_choice(self, app_name, model_name):
        """
        verbose_name： choices
        :return: {'gender': ['男', '女'], }
        """
        choice_dict = {}
        params = model_field_relation(app_name, model_name)
        for i in params:

            choices = i.choices
            if choices:
                choices = [i[0] for i in choices]
            else:
                choices = []
            choice_dict[i.name] = choices  # 'name': i.name,
        return choice_dict

    def model_type(self, app_name, model_name):
        """
        'name'： type
        :return: {'id': 'Integer', 'name': 'string'}
        """
        type_dict = {}
        params = model_field_relation(app_name, model_name)
        for i in params:
            tp = i.description
            tp = tp._proxy____args
            v = tp[0].split(' ')[0]
            if v == 'Big':
                v = 'Integer'
            elif v == 'Text':
                v = 'String'
            type_dict[i.name] = v

        return type_dict

    def all_desc(self, app_name, model_name):
        """
        key      默认值            中文             类型                下拉选项       不传          备注
        {'id': {'default': None, 'chinese': 'ID', 'type': 'Integer', 'choice': [], 'no': False, 'desc': ''}, 'KNO': {'default': None, 'chinese': '代码', 'type': 'String', 'choice': [], 'no': True, 'desc': ''}, 'NA': {'default': None, 'chinese': '科目名称', 'type': 'String', 'choice': [], 'no': False, 'desc': ''}, 'LB': {'default': None, 'chinese': '类别', 'type': 'String', 'choice': [], 'no': True, 'desc': ''}, 'F': {'default': '借', 'chinese': '方向', 'type': 'String', 'choice': ['借', '贷'], 'no': False, 'desc': ''}, 'LB10': {'default': '金额式', 'chinese': '帐页', 'type': 'String', 'choice': ['金额式', '数量式', '数量金额式', '外币式', '复币式', '数量复币式', '多栏式'], 'no': False, 'desc': ''}, 'CK': {'default': None, 'chinese': '辅助核算项', 'type': 'String', 'choice': [], 'no': True, 'desc': ''}, 'FNO': {'default': None, 'chinese': '上级code', 'type': 'String', 'choice': [], 'no': True, 'desc': ''}, 'unit': {'default': None, 'chinese': '需要数量核算，数量单位', 'type': 'String', 'choice': [], 'no': True, 'desc': ''}, 'currency': {'default': None, 'chinese': '需要外币核算，币种', 'type': 'String', 'choice': [], 'no': True, 'desc': ''}, 'retain': {'default': False, 'chinese': '保留以前年度账簿记录', 'type': 'Boolean', 'choice': [], 'no': False, 'desc': ''}, 'remarks': {'default': None, 'chinese': '备注', 'type': 'String', 'choice': [], 'no': True, 'desc': ''}, 'OUTNA': {'default': None, 'chinese': '报出科目', 'type': 'String', 'choice': [], 'no': True, 'desc': '注: 报出数据时如果不改变科目代码，不需要录入'}}

        """
        default_ = self.model_default(app_name, model_name)
        chinese_ = name_attribute_relation(app_name, model_name, attribute_name='verbose_name')
        type_ = self.model_type(app_name, model_name)
        choice_ = self.model_choice(app_name, model_name)
        desc_ = name_attribute_relation(app_name, model_name, attribute_name='help_text')
        no_ = name_attribute_relation(app_name, model_name, attribute_name='null')

        return {i: {'default': default_[i],
                    'chinese': chinese_[i],
                    'type': type_[i],
                    'choice': choice_[i],
                    'no': no_[i],
                    'desc': desc_[i]} for i in default_}


def show_model_class_name(fp):
    """显示.py 文件下面所有的 class名称"""
    # fp = os.path.abspath('..' + '/backstage/apps/admins/models.py')
    data = []
    with open(fp, 'r', encoding='utf-8') as f:
        while True:
            ret = f.readline()
            if not ret:
                break
            if re.search(r'class .*\):$', ret):
                data.append(ret.split(' ')[1].split('(')[0])
    return data
