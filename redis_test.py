#!/usr/bin/python

import redis
import argparse
import string, random
import datetime,time
from threading import Thread
from Queue import Queue

def getArgs():
    parser = argparse.ArgumentParser(description="Redis testing program")
    parser.add_argument('-s', '--host', help='Redis host to connect to')
    parser.add_argument('-p', '--port', type=int, nargs='?', default=6379, help='Redis port to connect to (default: 6379)')
    parser.add_argument('-t', '--threads', type=int, nargs='?', default=1, help='Redis threads to test with (default: 1)')
    parser.add_argument('-m', '--time', type=int, nargs='?', default=60, help="How long do you want the test to run for (seconds)")
    parser.add_argument('-d', '--debug', action="store_true", help='Enable Debug logging')
    parser.add_argument('-r', '--random', action="store_true", help='Randomly generate values')
    return parser.parse_args()

def randomgen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def redis_connect(host,port,debug):
    try:
        conn = redis.StrictRedis(
            host = host,
            port = port)
        result=conn
        if debug:
            print "DEBUG: Connecting to Redis at %s:%s" % (host, port) 
    except Exception as e:
        if debug:
            print "ERROR: Connecting to Redis - %s" % (e)
        result = None
 
    return result

def put_value(conn,debug, key, value):

    try:  
        result=conn.set(key,value)
        if debug:
            print "DEBUG: Inserting %s - %s" % (key, value)
    except Exception as e:
        if debug:
            print "DEBUG: Failed to insert %s:%s - %s" % (key,value,e)
        result=None

    if debug:
        print "DEBUG: Successfully put %s - %s into Redis" % (key,value)
    
    return result

def get_key(conn,debug, key,value):

    try:  
        if debug:
            print "DEBUG: Getting %s" % (key)
        result=conn.get(key)
    except Exception as e:
        if debug:
            print "DEBUG: Failed to get value from %s" % (key, e)
        result=None

    if debug and result is not None:
        print "DEBUG: Successfully got %s:%s from Redis" % (key,result)

    if debug:
        print "DEBUG: Matching value %s from Key: %s" % (value, key)
    if [ value == result ]:
        if debug:
            print "DEBUG: %s matches %s from Key: %s" % (result, value, key)
    elif value is not result:
        if debug:  
            print "DEBUG: %s doesn't match %s from key %s" % (result, value, key)
        result = None

    return result

def del_key(conn,debug, key):

    try:  
        if debug:
            print "DEBUG: Deleting Key %s" % (key)
        result=conn.delete(key)
    except Exception as e:
        if debug:
            print "DEBUG: Failed to delete key  %s - %s" % (key,e)
        result=None

    if debug and result is not None:
        print "DEBUG: Successfully remove key %s from Redis" % (key)

    return result

def do_work(q):
    conn = redis_connect(args.host,args.port,args.debug)
    stime = time.time()

    print q.get()

    if conn:
        if args.random:
            key=randomgen()
            value=randomgen()
        if args.debug:
            print "DEBUG: Randomly generating Key: %s, Value: %s" % (key,value)

        result = put_value(conn, args.debug, key, value)
        result = get_key(conn, args.debug, key, value)
        result = del_key(conn, args.debug, key)
       
        if result:
            retcode = "Success"
        else:
            retcode = "Error"
    else:
        retcode = "Error Connecting"

    etime = (time.time() - stime)
    if args.debug: 
        print "DEBUG: Thread finished at %s" % (etime)

    q.task_done()

    save_timings(retcode, etime)

def save_timings(retcode,etime):
    if [[ retcode == 'Success' ]]:
        success.append(etime)
    elif [[ retcode == 'Error' ]]:
        error.append(etime)
    else:
        unknown.append(etime)
    
if __name__ == "__main__":
    success=[]
    error=[]
    unkown=[]

    args = getArgs()
    q = Queue(args.threads)
    etime = datetime.datetime.now() + datetime.timedelta(0,int(args.time))

    print "INFO: Starting %s Threads for %s Seconds" % (args.threads, args.time)   
 
    while datetime.datetime.now() < etime:
        t = Thread(target=do_work, args=(q,))
        t.start()
        q.put(t)
        q.join() 

    print "INFO: Testing done now caculating results"
    
    if len(success) != 0:
        print "INFO: Total_Success: %s, Rate: %s/sec - Max_time: %ss, Min_time: %ss, Avg_time: %ss" % (len(success),(len(success)/int(args.time)),max(success),min(success) , reduce(lambda x, y: x + y, success) / len(success)) 
    else:
        print "INFO: Total_Success: 0, Rate: 0/sec - Max_time: 0, Min_time: 0, Avg_time: 0"
   
    if len(error) != 0:
        print "INFO: Total_Errors: %s, Rate: %s/sec - Max_time: %ss, Min_time: %ss, Avg_time: %ss" % (len(error),(len(success)/int(args.time)),max(error),min(error) , reduce(lambda x, y: x + y, error) / len(error)) 
    else:
        print "INFO: Total_Errors: 0, Rate: 0/sec - Max_time: 0, Min_time: 0, Avg_time: 0" 
