import shlex
import subprocess

cmd = "ffmpeg -headers 'X-Authorization: ATU-b86abb9efb5f0e29307d0d5c4e7fb61e86d37181'$'\r\nUse-Agent: pycopy'$'\r\nX-Api-Version: 1'$'\r\nX-Client-Type: api'$'\r\nConnection: keep-alive'$'\r\nAccept: */*'$'\r\nAccept-Encoding: gzip, deflate'$'\r\n' -loglevel debug -i 'https://copy.com/web/users/user-16139734/copy/test.mp3' -f s16le pipe:1"
args = shlex.split(cmd)
p = subprocess.Popen(args, stdin="https://copy.com/web/users/user-16139734/copy/test.mp3", stdout=subprocess.PIPE)
