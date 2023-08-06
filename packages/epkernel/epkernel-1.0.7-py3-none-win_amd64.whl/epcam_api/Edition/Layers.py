import os, sys, json
from epcam_api import BASE

from epcam_api.Action import Selection, Information

def delete_feature(job, step, layers):
    try:
        BASE.sel_delete(job, step, layers)
    except Exception as e:
        print(e)
    return 0

def break_features(job, step, layers, type):
    try:
        BASE.sel_break(job, step, layers, type)
    except Exception as e:
            print(e)
    return 0

def add_line(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, polarity:bool, attributes:list)->None:
    try:
        layer = ''
        if len(layers) > 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        BASE.add_line(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, polarity, 0, attributes)
    except Exception as e:
        print(e)
    return 0

def hierarchy_edit(job, step, layers, mode):
    try:
        BASE.sel_index(job, step, layers, mode)
    except Exception as e:
        print(e)
    return 0

def add_surface(job:str, step:str, layers:list, polarity:bool, attributes:list, points_location:list)->None:
    try:
        layer = ''
        if len(layers)> 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        BASE.add_surface(job, step, layers, layer, polarity, 0, False, attributes, points_location)
    except Exception as e:
        print(e)
    return ''

def add_round_surface(job:str, step:str, layers:list, polarity:bool, attributes:list,center_x:int,center_y:int,radius:int)->None:
    try:
        layer = ''
        if len(layers)> 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        point2_x = center_x + radius
        point2_y = center_y
        points_location = [[center_x, center_y], [point2_x, point2_y]]
        BASE.add_surface(job, step, layers, layer, polarity, 0, True, attributes, points_location)
    except Exception as e:
        print(e)
    return '' 

def contour2pad(job, step, layers, tol, minsize, maxsize, suffix):
    try:
        BASE.contour2pad(job, step, layers, tol, minsize, maxsize, suffix)
    except Exception as e:
        print(e)
    return ''

def resize_polyline(job, step, layers, size, sel_type):
    try:
        BASE.resize_polyline(job, step, layers, size, sel_type)
    except Exception as e:
        print(e)
    return ''

def contourize(job, step, layers, accuracy, separate_to_islands, size, mode):
    try:
        BASE.contourize(job, step, layers, accuracy, separate_to_islands, size, mode)
    except Exception as e:
        print(e)
    return ''

def add_pad(job, step, layers, symbol, location_x, location_y, polarity, orient, attributes):
    try:
        layer=''
        if len(layers)>0:
            layer=layers[0]
        BASE.add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, 0, orient, attributes)
    except Exception as e:
        print(e)
    return ''

def change_feature_symbols(job, step, layers, symbol):
    try:
        BASE.change_feature_symbols(job, step, layers, symbol, False)
    except Exception as e:
        print(e)
    return 0

def create_profile(job, step, layer):
    try:
        BASE.create_profile(job, step, layer)
    except Exception as e:
        print(e)
    return 0
    
def step_repeat(job, parent_step, child_steps):
    """
    #拼板
    :param     parentstep: panel
    :param     childsteps: 拼入panel的step
    :returns    :
    :raise error:
    """
    try:
        BASE.step_repeat(job, parent_step, child_steps)
    except Exception as e:
        print(e)
    return 0

def surface_repair(job, step, layers, scope, radius, remove_type, is_round):
    try:
        ret= Information.check_matrix_info(job,step,layers)
        if ret==True:
            BASE.remove_sharp_angle(job, step, layers, scope, radius, remove_type, is_round)
    except Exception as e:
        print(e)
    return 


def line2pad(job, step, layers):
    try:
        ret= Information.check_matrix_info(job,step,layers)
        if ret==True:
            BASE.line2pad_new(job, step, layers)
    except Exception as e:
        print(e)
    return 

def surface2outline(job, step, layers, width):
    try:
        ret= Information.check_matrix_info(job,step,layers)
        if ret==True:
            BASE.surface2outline(job, step, layers, width)
    except Exception as e:
        print(e)
    return 

def modify_attributes(job, step, layers, mode, attributes):
    try:
        BASE.modify_attributes(job, step, layers, mode, attributes)
    except Exception as e:
        print(e)
    return 

def add_arc(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, center_x:int, center_y:int,cw:bool,polarity:int, attributes:list)->None:
    try:
        layer=''
        if len(layers)>0:
            layer=layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        dcode = 0
        BASE.add_arc(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, center_x, center_y,cw,polarity, dcode, attributes)
    except Exception as e:
        print(e)
    return None

def layer_compare(job1:str, step1:str, layer1:str, job2:str, step2:str, layer2:str, tol:int, isGlobal:bool, consider_SR:bool, comparison_map_layername:str, map_layer_resolution:int)->None:
    try:
        BASE.layer_compare(job1, step1, layer1, job2, step2, layer2, tol, isGlobal, consider_SR, comparison_map_layername, map_layer_resolution)
    except Exception as e:
        print(e)
    return None

#将指定层中选中的feature拷贝至目标层，若无选中feature则将指定层资料整层拷贝
def copy_other(src_job:str, src_step:str, src_layer:str, dst_layer:str, invert:bool, offset_x:int, offset_y:int, mirror:int, resize:float, rotation:float, x_anchor:float, y_anchor:float):
    try:
        BASE.sel_copy_other(src_job, src_step, [src_layer], [dst_layer], invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return None

#将指定料号的step下的指定层的所有feature信息拷贝至目标料号的step下的对应层中
def copy_features2dstjob(src_job:str, src_step:str, src_layer:str, dst_job:str, dst_step:str, dst_layer:str, mode:bool, invert:bool)->None:
    try:
        BASE.copy_layer_features(src_job, src_step, [src_layer], dst_job, dst_step, [dst_layer], mode, invert)
    except Exception as e:
        print(e)
    return ''

#将指定料号指定层中选中的feature移动至目标料号下的目标层中，
def move2other_layer(src_job:str, src_step:str, src_layers:list, dst_job:str, dst_step:str, dst_layer:str, invert:bool, offset_x:int, offset_y:int, mirror:int, resize:float, rotation:float, x_anchor:float, y_anchor:float)->None:
    try:
        BASE.sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return ''
