import functools
from kflow import authn
from smart_open import open
from datetime import datetime

def WarehouseDatetimeLastSuccessfulJob(job_id:str,base_env:str='WarehouseProd'):
    warehouse_engine = authn.getConnectionDB(base_env)
    sql = f"""
    select last_date_loaded, datetime_started
    from job_log
    where job_name = '{job_id}' and status = 'success'
    order by datetime_started
    desc limit 1
    """
    result_proxy = warehouse_engine.execute(sql)
    for row_proxy in result_proxy:
        ## last_date_loaded is not none if it was explicitly set as a parameter.
        ## if it is not none then use that, otherwise last_date_loaded is the date the
        ## job was started.
        if row_proxy.items()[0][1] == None:
            return row_proxy.items()[1][1]
        else:
            return row_proxy.items()[0][1]

def WarehouseJobLog(row:dict, table="job_log", schema="public",base_env:str='WarehouseProd'):
    """
    Esconder autenticación
    """
    warehouse_engine = authn.getConnectionDB(base_env)
    row = {k: v for k, v in row.items() if v}
    columns = "("+','.join(list(row.keys()))+")"
    values = "("+','.join(["'"+str(a)+"'" for a in list(row.values())])+")"
    sql = f"""
        insert into "{schema}"."{table}" {columns}
        values {values}
        """
    warehouse_engine.execute(sql)

def log_python_operator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):

        # Before
        run_date = datetime.today()
        context = kwargs["context"]
        if "dag" in context.keys():
            WarehouseJobLog(
                {"job_name":context["dag"].dag_id,
                "job_type":"snapshot",
                "table_name":"prisma_table",
                "datetime_started":run_date,
                "datetime_finished":None,
                "last_date_loaded":context["dag_run"].conf.get('last_date'),
                "status":"started",
                "status_message":""
                })
        
        # Func
        value = func(*args, **kwargs)
        
        # After
        if "dag" in context.keys():
            WarehouseJobLog(
                {"job_name":context["dag"].dag_id,
                "job_type":"snapshot",
                "table_name":"prisma_table",
                "datetime_started":run_date,
                "datetime_finished":datetime.now(),
                "last_date_loaded":None,
                "status":"success",
                "status_message":""
                })

        return value
        
    return wrapper_decorator
