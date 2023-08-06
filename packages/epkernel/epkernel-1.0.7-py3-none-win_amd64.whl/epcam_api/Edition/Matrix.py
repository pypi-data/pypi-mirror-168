import os, sys, json
from epcam_api import BASE
from epcam_api.Edition import Layers
from epcam_api.Action import Selection, Information

# 拷贝Layer
# jobname, org_layer_index, dst_layer, poi_layer_index
def copy_layer(jobname, old_layer_name):
    try:
        ret = BASE.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        src_layername=[]
        src_layername= Information.get_layers(jobname)
        if old_layer_name in src_layername:
            for i in range(0, len(layer_infos)):         
                if layer_infos[i]['name'] == old_layer_name:
                    old_layer_index = i + 1
        else:
            print('e')
            return 0
        dst_layer = ''
        # 新建空layer
        create_layer(jobname, 'jbz')
        ret2 = BASE.copy_layer(jobname, old_layer_index,
                               dst_layer, len(layer_infos) + 1)
        data2 = json.loads(ret2)
        new_layer = data2['paras']['newname']
        # 删除新层
        delete_layer(jobname, 'jbz')
        return new_layer
    except Exception as e:
        print(e)
        print('123456')
    return ''

# 创建layer
def create_layer(job, layer):
    try:
        index = -1  # 默认创建在末尾
        step = ''  # 在所有层创建
        BASE.create_new_layer(job, step, layer, index)
    except Exception as e:
        print(e)

# 删除layer
def delete_layer(job, layername):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layername:
                layer_index = i + 1
                BASE.delete_layer(job, layer_index)
                break
    except Exception as e:
        print(e)
    return 0

def insert_row(job, row_index,row_name):
    try:
        BASE.create_new_layer(job, '', row_name, row_index)
    except Exception as e:
        print(e)
    return 0

def insert_column(job, col_index,col_name):
    try:
        BASE.create_step(job, col_name, col_index)
    except Exception as e:
        print(e)
    return 0

# 创建step
def create_step(job, step):
    try:
        index = -1  # 默认创建在末尾
        BASE.create_step(job, step, index)
    except Exception as e:
        print(e)

def change_matrix_row(job, layer, context, type, layername):
    """
    #修改指定层别信息,若修改后信息与原层别一致，则此函数不执行
    :param     jobname:
    :param     layer:
    :param     context:
    :returns   :
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layer:
                layer_index = i + 1
                layer_infos[i]['context'] = context
                layer_infos[i]['type'] = type
                layer_infos[i]['name'] = layername
        BASE.change_matrix(job, -1, layer_index, '',
                           layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0


def change_matrix_column(job, src_name, dst_name):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        old_step_index = step_infos.index(src_name) + 1
        old_layer_index = -1
        new_layer_info = ''
        BASE.change_matrix(job, old_step_index,
                           old_layer_index, dst_name, new_layer_info)
    except Exception as e:
        print(e)


def delete_step(job, step):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        for i in range(0, len(step_infos)):
            if step_infos[i] == step:
                step_index = i + 1
        BASE.delete_step(job, step_index)
    except Exception as e:
        print(e)
    return 0


def copy_step(job, src_step_name):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']

        for i in range(0, len(step_infos)):
            if step_infos[i] == src_step_name:
                old_step_index = i + 1
        BASE.insert_step(job, old_step_index+1)
        dst_step = ''
        # 新建空
        create_step(job, 'jbz')
        ret2 = BASE.copy_step(job, old_step_index,
                              dst_step, len(step_infos) + 1)
        data2 = json.loads(ret2)
        new_step = data2['paras']['newname']
        # 删除新层
        delete_step(job, 'jbz')
        return new_step
    except Exception as e:
        print(e)
    return ''

#备份多层（覆盖）(需备份层无选中feature)
def backup_layer(job, step, layers, suffix):
    try:
        layer_list = Information.get_layers(job)
        for layer in layers:
            new_layer = layer + suffix
            if new_layer not in layer_list:
                create_layer(job, new_layer)
            else:
                BASE.clear_selected_features(job, step, new_layer)
                Selection.reverse_select(job, step, new_layer) 
                Layers.delete_feature(job, step, new_layer)  
                BASE.clear_selected_features(job, step, new_layer)
            Layers.copy_other(job, step, layer, new_layer, False, 0, 0, 0, 0, 0, 0, 0)
    except Exception as e:
        print(e)
        return None