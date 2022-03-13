import requests
from requests.auth import HTTPProxyAuth
from digestAuth import HTTPProxyDigestAuth
import time

numberOfTimes = 1

with open('proxies.txt', 'r') as f:
    proxy = [line.strip() for line in f]

ipPort = []
username = []
password = []
for p in proxy:
    ip = p.split(':')
    ipPort.append(ip[0] + ':' + ip[1])
    username.append(ip[2])
    password.append(ip[3])


viewCount = input("How many views would you like to send?\n")
sleepTime = input("Enter the amount of time between each view (in seconds): ")
url = input("Please input the url of the listing: ")
if len(ipPort) < int(viewCount):
    numberOfTimes = input("Please enter the amount of times you would like to reuse proxies: ")

numberOfTimes = int(numberOfTimes)
proxyIndex = 0
successCount = 0
startTime = time.time()
for i in range(int(viewCount)):
    if i % numberOfTimes == 0:
        proxyIndex += 1
    s = requests.Session()
    s.proxies = {
        'https', 'http://' + ipPort[proxyIndex]
    }
    s.auth = HTTPProxyDigestAuth(username[proxyIndex], password[proxyIndex])

    res = s.get(url)
    if res.ok:
        print("Success")
        successCount += 1
    else:
        break
    time.sleep(float(sleepTime))

endTime = time.time() - startTime
formattedTime = "{:.2f}".format(endTime)
print(f"{successCount} out of {viewCount} succeeded in {formattedTime}s")