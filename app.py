import socket
import docker
import os
import a2s
import time

print('Target Container Name:', os.path.expandvars('${SRCDS_CONTAINER_NAME}'))
print('Target SRCDS Host:', os.path.expandvars('${SRCDS_HOST}'))
print('Target SRCDS Port:', os.path.expandvars('${SRCDS_PORT}'))
print('Initial Wating Time:', os.path.expandvars('${INITIAL_WATING_TIME}'))

client = docker.from_env()
container = client.containers.get(os.path.expandvars('${SRCDS_CONTAINER_NAME}'))

address = (os.path.expandvars('${SRCDS_HOST}'), int(os.path.expandvars('${SRCDS_PORT}')))

print(f'Wait for {os.path.expandvars('${INITIAL_WATING_TIME}')} seconds to ensure the server is available on start')
time.sleep(int(os.path.expandvars('${INITIAL_WATING_TIME}')))

errorCount = 0

while True:
    try:
        a2s.info(address)
    
    except socket.timeout:
        errorCount += 1
        print('Socket Timeout, Error Count:', errorCount)

    except socket.gaierror:
        errorCount += 1
        print('No Route to Host, Error Count:', errorCount)

    except ConnectionRefusedError:
        errorCount += 1
        print('Connection Refused, Error Count:', errorCount)
    
    else:
        errorCount = 0

    finally:
        if errorCount == 5:
            print('Server Restarting...')
            errorCount = 0;
            container = client.containers.get(os.path.expandvars('${SRCDS_CONTAINER_NAME}'))
            container.restart()
            time.sleep(60)

        time.sleep(12)
