from celery import shared_task


@shared_task(ignore_result=True)
def run_script_on_device(group, device, script):
    print(group, device, script)
