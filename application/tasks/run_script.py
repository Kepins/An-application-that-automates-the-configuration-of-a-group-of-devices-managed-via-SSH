from celery import shared_task
from invoke import UnexpectedExit
from paramiko import AuthenticationException

from application.models import Script
from application.utils.task_utils import create_connection, check_connection


@shared_task(ignore_result=True)
def run_script_on_device(group_pk, device_pk, script_pk):
    status, warns, password, key = check_connection(device_pk, group_pk)

    script = Script.objects.get(pk=script_pk)
    try:
        result = connection.run(script.script, hide=True)
        print(result.stdout)
        return
    except AuthenticationException as e:
        print("Authentification failed")
        return
    except UnexpectedExit as e:
        print(e.args[0].stderr)
        return
