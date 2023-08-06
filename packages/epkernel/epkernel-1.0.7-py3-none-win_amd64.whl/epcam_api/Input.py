import os, sys, json
from epcam_api import BASE
from epcam_api.Action import Information
from epcam_api.Edition import Job

#打开料号
def open_job(job, path):
    try:
       ret= json.loads(BASE.open_job(path, job))['paras']['status']
       return ret   
    except Exception as e:
        print(e)
        return False

def open_eps(job, path):
    try:
        open_jobs = Information.get_opened_jobs()
        if job in open_jobs: #存在
            return False
        else:
            ret = BASE.open_eps(job, path)
            ret_= json.loads(ret)
            if 'result' in ret_:
                if ret_['result']: #True
                    return ret_['result']
                else:
                    data= Information.get_opened_jobs()
                    if job in data:
                        Job.delete_job(job)
                        return False
                    else:
                        return False
    except Exception as e:
        print(e)
    return False