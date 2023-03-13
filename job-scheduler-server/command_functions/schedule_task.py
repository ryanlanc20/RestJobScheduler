import schedule

def scheduleTask(executionDelay,jobExecuterDelegate,type):
    schedule.every(executionDelay).seconds.do(jobExecuterDelegate).tag(type)