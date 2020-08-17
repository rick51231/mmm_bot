import subprocess

from core.settings import WEBHOOK_HOST, BASE_DIR

command_str = ['/code/certificate/acme.sh',
               '--issue',
               '--dns',
               'dns_cf',
               f'-d',
               f'{WEBHOOK_HOST}',
               f'-d',
               f'www.{WEBHOOK_HOST}',
               f"--key-file",
               f"{BASE_DIR}/certificate/{WEBHOOK_HOST}-key.pem",
               f"--fullchain-file",
               f"{BASE_DIR}/certificate/{WEBHOOK_HOST}-cert.pem"]
print(' '.join(command_str))
command = subprocess.Popen(command_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True)
output, errors = command.communicate()

command.wait()
if command.returncode != 0:
    print(output)
    print('____')
    print(errors)
    # messages.error(request, f"Ошибка при получении сертификата"
    #                         f"{errors}")
