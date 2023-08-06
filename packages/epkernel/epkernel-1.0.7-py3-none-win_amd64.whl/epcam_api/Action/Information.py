import os, sys, json, math
from epcam_api import epcam, BASE

def check_matrix_info(job:str, step='', layers=[])->bool:
    try:
        if isinstance(job, str) and isinstance(step, str) and isinstance(layers, list):
            open_jobs = get_opened_jobs()
            if job in open_jobs: 
                if step == '' and layers == []:
                    return False
                step_lst= get_steps(job)
                layer_lst = get_layers(job)
                if step!='':
                    if step not in step_lst:
                        print('step不存在')
                        return False
                if layers!=[]:
                    for layer in layers:
                        if layer not in layer_lst:
                            print(layer + ' 不存在')
                            return False
            else:
                print(f'{job}:未打开,请查找原因!')
                return False
        else:
            print("请检查填写的参数类型!")
            return False
    except Exception as e:
        return False
        print(e)
    return True

def is_selected(job,step,layer):
    ret = BASE.is_selected(job,step,layer)
    ret = json.loads(ret)
    if 'result' in ret:
        return ret['result']
    return False

def get_drill_layer_name(job):
    """
    #获取孔层layer名
    :param     job:
    :param     step:
    :return    drill_list:孔层名列表
    :raises    error:
    """
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        drill_list = []
        layer_info = data['paras']['info']
        for i in range(0, len(layer_info)):
            if layer_info[i]['type'] == 'drill' and layer_info[i]['context'] == 'board':
                drill_list.append(layer_info[i]['name'])
        return drill_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return []

def get_inner_layers(job):
    """
    #获取内层layer_list
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                board_layer_list.append(layer_info[i]['name'])      
        if len(board_layer_list) <= 2:
            print('no inner layer!')
            return []
        else:
            board_layer_list.pop(-1)
            board_layer_list.pop(0)
            inner_layer_list = board_layer_list
        return inner_layer_list
    except Exception as e:
        print(e)
    return []

def get_board_layers(job):
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        layer_list = []
        layer_info = data['paras']['info']
        if len(layer_info):
            for i in range(0, len(layer_info)):
                if layer_info[i]['context'] == 'board':
                    layer_list.append(layer_info[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''

def get_soldermask_layers(job):
    """
    #获取防焊层list
    :param     job:
    :param     step:
    :returns   solder_mask_list:
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        solder_mask_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'solder_mask':
                solder_mask_list.append(layer_info[i]['name'])      
        return solder_mask_list
    except Exception as e:
        print(e)
    return ''

def get_signal_layers(job):
    """
    #获取内外层layer 名
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and (layer_info[i]['type'] == 'signal'or layer_info[i]['type'] == 'power_ground'):
                board_layer_list.append(layer_info[i]['name'])
        return board_layer_list
    except Exception as e:
        print(e)
    return []

def get_outer_layers(job):
    """
    #获取外层list
    :param     job:
    :returns   outter_layer_list:外层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        if index_list == []:
            print("no signal layer")
            return []
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])
        outter_layer_list = []
        outter_layer_list.append(board_layer_list[0])
        if len(board_layer_list) == 1:
            return outter_layer_list
        else: 
            outter_layer_list.append(board_layer_list[-1])
        return outter_layer_list
    except Exception as e:
        print(e)
    return ''

def get_silkscreen_layers(job):
    """
    #获取丝印层layer_list        
    :param     job:     
    :returns   layer_list:丝印层layername列表     
    :raises    error:    
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'silk_screen':
                layer_list.append(layer_info[i]['name'])
        
        if len(layer_list) < 1:
            print("can't find silk_screen-layer!")

        return layer_list
    except Exception as e:
        print(e)
    return ''

def get_soldermask_layers(job):
    """
    #获取防焊层list
    :param     job:
    :param     step:
    :returns   solder_mask_list:
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        solder_mask_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'solder_mask':
                solder_mask_list.append(layer_info[i]['name'])      
        return solder_mask_list
    except Exception as e:
        print(e)
    return ''

#获取layer profile polygon
def get_profile(job, step):
    try:
        return BASE.get_profile(job, step)
    except Exception as e:
        print(e)
    return 0

def get_layer_feature_count(job, step, layer):
    ret = BASE.get_layer_feature_count(job, step, layer)
    ret = json.loads(ret)
    if 'featureNum' in ret:
        return int(ret['featureNum'])
    return -1

def get_steps(job):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        steps = data['paras']['steps']
        return steps
    except Exception as e:
        print(e)
    return []

def get_layers(job):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_infos)):
            layer_list.append(layer_infos[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_usersymbol_list(job):
    try:
        ret = BASE.get_special_symbol_names(job)
        data = json.loads(ret)
        user_list = data['paras']
        return user_list
    except Exception as e:
        print(e)
    return []

def get_profile_box(job:str, step:str)->dict:   
    try:
        info= check_matrix_info(job, step)
        if info:
            ret_= BASE.has_profile(job,step)
            data_= json.loads(ret_)['result']
            if data_:
                ret = BASE.get_profile_box(job, step)
                data = json.loads(ret)
                profile_box = data['paras']
                return profile_box
            else:
                print('没有profile!')
                return None
        else:
            return info
    except Exception as e:
        print(e)
    return 0

#获取拼版中最小和最大坐标
def get_inner_profile_box(job:str,step:str)->dict:
    try:
        repeat_infos=BASE.get_step_repeat(job,step)    #获取拼板信息
        repeat_infos=json.loads(repeat_infos)
        repeat_infos=repeat_infos['result']
        xminlist=[]
        yminlist=[]
        xmaxlist=[]
        ymaxlist=[]
        for repeat_info in repeat_infos:
            repeat_infox=repeat_info['X']
            repeat_infoy=repeat_info['Y']
            set_box=BASE.get_profile_box(job, repeat_info['NAME'])
            set_box=json.loads(set_box)['paras']
            datum_x=json.loads(BASE.get_step_header_infos(job, repeat_info['NAME']))['x_datum']
            datum_y=json.loads(BASE.get_step_header_infos(job, repeat_info['NAME']))['y_datum']
            x_offset = repeat_infox - datum_x
            y_offset = repeat_infoy - datum_y
            pts=[]
            pts.append([set_box['Xmin']+x_offset,set_box['Ymin']+y_offset])
            pts.append([set_box['Xmin']+x_offset,set_box['Ymax']+y_offset])
            pts.append([set_box['Xmax']+x_offset,set_box['Ymax']+y_offset])
            pts.append([set_box['Xmax']+x_offset,set_box['Ymin']+y_offset])
            width=set_box['Xmax']-set_box['Xmin']
            height=set_box['Ymax']-set_box['Ymin']
            if repeat_info['MIRROR']:
                pts.clear()
                pts.append([set_box['Xmin']+x_offset-width,set_box['Ymin']+y_offset])
                pts.append([set_box['Xmin']+x_offset-width,set_box['Ymax']+y_offset])
                pts.append([set_box['Xmin']+x_offset,set_box['Ymax']+y_offset])
                pts.append([set_box['Xmin']+x_offset,set_box['Ymin']+y_offset])

            if repeat_info['ANGLE']!=0:
                value = math.acos(-1) / 180
                ratio = -1 * repeat_info['ANGLE'] * value
                if repeat_info['MIRROR']:
                    ratio = -1 * (360-repeat_info['ANGLE']) * value
                for pt in pts:
                    a = pt[0]
                    b = pt[1]
                    pt[0]=(a - repeat_infox)*math.cos(ratio) - (b - repeat_infoy)*math.sin(ratio) + repeat_infox
                    pt[1]=(a - repeat_infox)*math.sin(ratio) + (b - repeat_infoy)*math.cos(ratio) + repeat_infoy
            allx=[]
            ally=[]
            for pt in pts:
                allx.append(pt[0])
                ally.append(pt[1])
            allx.sort()
            ally.sort()
            xmin=allx[0]
            ymin=ally[0]
            set_length=allx[-1]-allx[0]
            set_width=ally[-1]-ally[0]    
            length= (repeat_info['NX']-1)*repeat_info['DX']+set_length
            width = (repeat_info['NY']-1)*repeat_info['DY']+set_width
            xmax=xmin+length
            ymax=ymin+width
            xminlist.append(xmin)
            yminlist.append(ymin)
            xmaxlist.append(xmax)
            ymaxlist.append(ymax)
        xminlist.sort()
        yminlist.sort()
        xmaxlist.sort(reverse=True)
        ymaxlist.sort(reverse=True)
        gSRxmin=xminlist[0]
        gSRymin=yminlist[0]
        gSRxmax=xmaxlist[0]
        gSRymax=ymaxlist[0]
        infos={}
        infos['gSRxmin']=gSRxmin
        infos['gSRymin']=gSRymin
        infos['gSRxmax']=gSRxmax
        infos['gSRymax']=gSRymax
        return infos
    except Exception as e:
        print(e)
    return {}

def get_selected_features_box(job:str, step:str, layers:list)->dict:
    try:
        ret = BASE.get_selected_features_box(job, step, layers)
        data = json.loads(ret)
        features_box=[]
        for value in data.values():
            features_box.append(value)
        if len(set(features_box))==1:
            return {}
        else:
            return data
    except Exception as e:
        print(e)
    return None

def get_rest_cu_rate(job:str,step:str,layer:str,thickness:int)->float:
    try:
        resolution_define = 0
        ret = BASE.get_rest_cu_rate(job,step,layer,resolution_define,thickness)
        cu_t = json.loads(ret)['result']
        data_1= float(cu_t.split('/')[0])
        data_2= float(cu_t.split('/')[1])
        data= round((data_1/data_2),4)
        return data
    except Exception as e:
        print(e)
        return -1
        
def get_opened_jobs()->list:
    try:
        ret= BASE.get_opened_jobs()
        data= json.loads(ret)['paras']
        return data
    except Exception as e:
        print(repr(e)+'不存在已经打开的料!')
        return []

#获取选中feature的坐标,symbolname,极性, 角度, 是否镜像
def get_selected_features_infos(job:str, step:str, layer:str)->list:
    try:
        ret = BASE.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        featureinfos = []
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_selected_features_count(job:str, step:str, layer:str)->int:
    try:
        if isinstance(job, str) and isinstance(step, str) and isinstance(layer, str):
            count_sum=0
            features_count = get_selected_features_infos(job,step,layer)
            if features_count!=None:
                count_sum = len(features_count)
            else:
                print('无物件选中!')
            return count_sum
        else:
            print("参数类型错误!")
            return None
    except Exception as e:
        print(e)
    return None

#获取当前状态下筛选器的筛选状态
def get_select_param()->dict:
    try:
        featuretype_list= ['positive','negative','text','surface','arc','line','pad']
        ret= BASE.get_select_param()
        data = json.loads(ret)
        if data['paras']!=False:
            infos= data['paras']['param']
            featuretypes= infos['featuretypes']
            result= BASE.Dec2Bin(featuretypes)
            if len(result)!=7 and featuretypes>32:
                result.reverse()
                result_new= result
                result_new.append(0)
                result_new.reverse()
            else:
                result_new=result
            bool_lst=[]
            for value in result_new:
                if value==1:
                    bool_lst.append(True)
                else:
                    bool_lst.append(False)
            new_lst = dict(zip(featuretype_list, bool_lst))
            infos['featuretypes']=new_lst
            return infos
    except Exception as e:
        print(repr(e))
    return None

def get_system_attr_defines()->list:
    try:
        ret = BASE.get_system_attr_defines()
        data = json.loads(ret)
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_user_attr_defines()->list:
    try:
        ret = BASE.get_user_attr_defines()
        data = json.loads(ret)
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None
