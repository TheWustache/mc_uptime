import pexpect
import os
import time

path = '/Users/leo/Projects/minecraft_server/'

mc = pexpect.spawn('java -Xmx1024M -Xms1024M -jar minecraft_server.1.12.2.jar nogui', cwd=path)
mc.expect('.*Done.*')
print('Server started.')
index = mc.expect('.*stop.*')
print('Stopping server.')
mc.sendline('say §d§lServer §d§lclosing §d§lin §c§l3 §c§lseconds.')
time.sleep(3)
mc.sendline('stop')
mc.expect('.*Saving chunks.*')
print('Server stopped.')
# for i in range(10):
#     mc.sendline('say ' + str(i))
#     time.sleep(3)
mc.terminate(force=True)
