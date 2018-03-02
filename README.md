Redis-test
==========

This is a simple key->value test for redis where I implemented threading and queues for throughput.


Usage
=====

```
usage: redis_test.py [-h] [-s HOST] [-p [PORT]] [-t [THREADS]] [-m [TIME]]
                     [-d] [-r]

Redis testing program

optional arguments:
  -h, --help            show this help message and exit
  -s HOST, --host HOST  Redis host to connect to
  -p [PORT], --port [PORT]
                        Redis port to connect to (default: 6379)
  -t [THREADS], --threads [THREADS]
                        Redis threads to test with (default: 1)
  -m [TIME], --time [TIME]
                        How long do you want the test to run for (seconds)
  -d, --debug           Enable Debug logging
  -r, --random          Randomly generate values
```


Example
=======

```
./redis_test.py -s 127.0.0.1 -p 80 -m 20 -t 100 -r

INFO: Starting 100 Threads for 20 Seconds
INFO: Testing done now caculating results
INFO: Total_Success: 472, Rate: 23/sec - Max_time: 7.74442696571s, Min_time: 0.00369715690613s, Avg_time: 4.63237895299s
INFO: Total_Errors: 0, Rate: 0/sec - Max_time: 0, Min_time: 0, Avg_time: 0
```
