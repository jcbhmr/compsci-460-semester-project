# SpeedCompare

💻 Basic network speed testing client & server scripts in Python

## Installation

```sh
pip install git+https://github.com/jcbhmr/speedcompare.git
```

## Usage

<table><td>

```sh
speedcompare-server tcp
```

<td>

```sh
speedcompare tcp
```

</table>

There are three modes for the client and the server: tcp, udp, and http11. The options are _mostly_ the same for each mode.

For the server there's `--bind` and `--size`. The server determines how much data to send to the client. The client just counts the data and ends the timer when the connection closes. For UDP since there isn't a connection close event that you can detect from the receiver we use a timeout instead.

On the client there's `--host` and `--sockets` to set the remote server address and the number of simultaneous connections to make. Each connection will be run in a new Python thread.

## How it works

You choose the amount of data to send from the server to the client. When a new client connects to the server it immediately sends that many bytes. The client then can check how long it took to receive the data and calculate the speed.

## Results

All of these tests were run on a GitHub Codespaces VM with 2 cores and 4 GB of RAM. There was no network travesal involved; all of these connections are strictly local.

### TCP

<table align=center><td>

```sh
python -m speedcompare tcp
```

<td>

```sh
python -m speedcompare-server tcp
```

</table>

| Size per socket | Sockets | Size total | Time | Speed total | Speed per socket |
| --- | --- | --- | --- | --- | --- |
| 10 MB | 1 | 10 MB | 0.44 s | 179 Mbps | 179 Mbps |
| 10 MB | 2 | 20 MB | 0.64 s | 249 Mbps | 124 Mbps |
| 10 MB | 4 | 40 MB | 1.0 s | 319 Mbps | 79 Mbps |
| 10 MB | 8 | 80 MB | 2.2 s | 288 Mbps | 36 Mbps |
| 10 MB | 16 | 160 MB | 2.2 s | 567 Mbps | 35 Mbps |
| 10 MB | 32 | 320 MB | 3.1 s | 807 Mbps | 25 Mbps |
| 10 MB | 64 | 640 MB | 5.5 s | 930 Mbps | 14 Mbps |
| 10 MB | 128 | 1.2 GB | 9.9 s | 1.0 Gbps | 7 Mbps |
| 10 MB | 256 | 2.5 GB | 20 s | 1.0 Gbps | 3 Mbps |

Takeaways:

- As more sockets are added the speed per socket decreases. This means that if you have a lot of browser tabs open all fetching data that your overall per-tab speed will decrease. Makes sense.
- You can get close to 1 Gbps under the testing conditions before things top out.

### UDP

| Size per socket | Sockets | Size total | Loop delay | Size received | Time | Speed total | Speed per socket | Percentage through |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 MB | 1 | 10 MB | 0 ms | 385 kB | 1.0 s | 3 Mbps | 3 Mbps | 3.8% |
| 10 MB | 1 | 10 MB | 1 ms | 9.2 MB | 3.0 s | 24 Mbps | 24 Mbps | 92% |
| 10 MB | 2 | 20 MB | 0 ms | 1.0 MB | 1.0 s | 7 Mbps | 3 Mbps | 5.2% |
| 10 MB | 2 | 20 MB | 1 ms | 15 MB | 3.8 s | 31 Mbps | 15 Mbps | 76% |
| 10 MB | 4 | 40 MB | 0 ms | 2.9 MB | 1.1 s | 21 Mbps | 5 Mbps | 7.3% |
| 10 MB | 4 | 40 MB | 1 ms | 21 MB | 3.8 s | 45 Mbps | 11 Mbps | 53% |
| 10 MB | 8 | 80 MB | 0 ms | 6.8 MB | 1.1 s | 45 Mbps | 5 Mbps | 8.5% |
| 10 MB | 8 | 80 MB | 1 ms | 32 MB | 3.9 s | 64 Mbps | 8 Mbps | 40% |
| 10 MB | 16 | 160 MB | 0 ms | 15 MB | 1.4 s | 87 Mbps | 5 Mbps | 9.5% |
| 10 MB | 16 | 160 MB | 1 ms | 50 MB | 4.0 s | 98 Mbps | 6 Mbps | 31% |
| 10 MB | 32 | 320 MB | 0 ms | 37 MB | 1.8 s | 163 Mbps | 5 Mbps | 11% |
| 10 MB | 32 | 320 MB | 1 ms | 72 MB | 4.1 s | 139 Mbps | 4 Mbps | 22% |
| 10 MB | 64 | 640 MB | 0 ms | 86 MB | 3.0 s | 227 Mbps | 3 Mbps | 13% |
| 10 MB | 64 | 640 MB | 1 ms | 151 MB | 6.2 s | 192 Mbps | 3 Mbps | 23% |
| 10 MB | 128 | 1.2 GB | 0 ms | 193 MB | 4.7 s | 324 Mbps | 2 Mbps | 15% |
| 10 MB | 128 | 1.2 GB | 1 ms | 270 MB | 10 s | 201 Mbps | 1 Mbps | 21% |
| 10 MB | 256 | 2.5 GB | 0 ms | 321 MB | 7.2 s | 355 Mbps | 1 Mbps | 12% |
| 10 MB | 256 | 2.5 GB | 1 ms | 546 MB | 19 s | 220 Mbps | 0.8 Mbps | 21% |

Takeaways:

- The highest per-socket bandwidth was 24 Mbps where the server loop had a 1ms delay. I think this is because slowing down the server sending the data allows the client to keep up and not just discard excessive incoming data.
- Bandwidth was never as high as TCP. Given that the received percentage never crossed 80% I think the speed never caught up because so much data was just discarded due to the client not being able to keep up.

### HTTP/1.1

| Size per socket | Sockets | Size total | Time | Speed total | Speed per socket |
| --- | --- | --- | --- | --- | --- |
| 10 MB | 1 | 10 MB | 0.05 s | 1.3 Gbps | 1.3 Gbps |
| 10 MB | 2 | 20 MB | 0.1 s | 1.4 Gbps | 700 Mbps |
| 10 MB | 4 | 40 MB | 0.1 s | 1.8 Gbps | 450 Mbps |
| 10 MB | 8 | 80 MB | 0.3 s | 1.6 Gbps | 200 Mbps |
| 10 MB | 16 | 160 MB | 0.7 s | 1.7 Gbps | 106 Mbps |
| 10 MB | 32 | 320 MB | 1.2 s | 2.0 Gbps | 62 Mbps |
| 10 MB | 64 | 640 MB | 1.6 s | 3.0 Gbps | 46 Mbps |
| 10 MB | 128 | 1.2 GB | 2.8 s | 3.5 Gbps | 27 Mbps |
| 10 MB | 256 | 2.5 GB | 4.9 s | 4.1 Gbps | 16 Mbps |

Takeaways:

- Exceedingly fast. I think this has to do with the fact that these Python urllib requests or even the Python HTTP server are being all made from some highly optimized Python code or maybe even directly calling a C++ HTTP library instead of implementing the HTTP protocol in Python.
- Use HTTP whenever you can. It's much much easier to make a concrete HTTP request or even a WebSocket connection instead of trying to implement your own UDP protocol.

As a sidenote, using `curl` I get a 1.3 Gbps download speed so I think that yeah the Python code is just delegating to some really fast C++ code since the client isn't the bottleneck. It's the Python HTTP server that can't serve fast enough.

```
$ curl http://localhost:8002 > /dev/null
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 9765k    0 9765k    0     0  1362M      0 --:--:-- --:--:-- --:--:-- 1362M
```

## Development

Here's the quick commands to get started:

<table><thead><tr><th>Linux & macOS<th>Windows
<tbody><tr><td>

```sh
ptyhon3.12 -m venv .venv
. .venv/bin/activate
```

<td>

```ps1
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

</table>

```sh
pip install -r requirements.txt
```

Now you can edit the Python code and run `python -m speedcompare` or `python -m speedcompare-server` to run the app locally!
