import os

from movieAnalysis.settings import BASE_DIR

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务
# djcelery.setup_loader()
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_BROKER_URL = 'redis://:1690036618@127.0.0.1:6379/1'
# CELERY_RESULT_BACKEND = 'redis://:1690036618@127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

# 有些情况可以防止死锁
CELERYD_FORCE_EXECV = True

#可以有效防止死锁。即使不是这个原因造成的，也尽量加上
CELERYD_FORCE = True

# 单个任务的最大运行时间
# CELERYD_TASK_TIME_LIMIT = 12 * 30

# 每个worker最多执行100个任务被销毁，可以防止内存泄漏
# CELERYD_MAX_TASKS_PER_CHILD = 100


# CELERY_IMPORTS = (
#     'proxyManager.tasks.testWriteFile',
# )


# from datetime import timedelta

# 定时任务
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'proxyManager.tasks.testWriteFile',  # 任务名
#         'schedule': timedelta(seconds=6),  # 每2s执行一次该任务
#         'args': ()
#     }
# }
