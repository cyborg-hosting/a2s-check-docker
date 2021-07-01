import socket
import docker
import os
import a2s
import time

print('Target Container Name:', os.path.expandvars('${SRCDS_CONTAINER_NAME}'))
print('Target SRCDS Host:', os.path.expandvars('${SRCDS_HOST}'))
print('Target SRCDS Port:', os.path.expandvars('${SRCDS_PORT}'))

client = docker.from_env()
container = client.containers.get(os.path.expandvars('${SRCDS_CONTAINER_NAME}'))

address = (os.path.expandvars('${SRCDS_HOST}'), int(os.path.expandvars('${SRCDS_PORT}')))

print('Wait for 60 seconds to ensure the server is available on start')
time.sleep(60)

errorCount = 0

while True:
    try:
        a2s.info(address)
    
    except socket.timeout:
        errorCount += 2
        print('Socket Timeout, Error Count:', errorCount - 1)

    except socket.gaierror:
        errorCount += 2
        print('No Route to Host, Error Count:', errorCount - 1)

    except ConnectionRefusedError:
        errorCount += 2
        print('Connection Refused, Error Count:', errorCount - 1)

    finally:
        if errorCount > 0:
            errorCount -= 1
        if errorCount == 5:
            print('Server Restarting...')
            errorCount = 0;
            container = client.containers.get(os.path.expandvars('${SRCDS_CONTAINER_NAME}'))
            container.restart()
            time.sleep(60)

        time.sleep(12)
