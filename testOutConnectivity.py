import socket
import time
import sys, getopt

def TestConnectivity(ip, port, num_tries=100):
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error as err: 
    print("socket creation failed with error %s" %(err))
  for i in range(num_tries):
    try:
      sock.connect((ip, port))
      sock.close()
    except socket.error as e:
      msg = 'Connect failed with "%s" on attempt %i' % (e, i)
      raised_errno = e.errno or -1
      return (raised_errno, msg)
    return (0, 'Success')

def WaitForNetwork(ip, port, total_wait=20, totalTries=100, outFileName="logs.txt"):
  logFile = open(outFileName, "x")
  logFile.write('Beggining time='+str(time.time()))
  end = time.time() + total_wait
  err, msg = TestConnectivity(ip, port, totalTries)
  while err and time.time() <= end:
    logFile.write('TestConnectivity failed with error.\t'+msg+'\tCURRENT TIME:'+str(time.time())+'\t- trying again...\n')
    time.sleep(0.5)
    err, msg = TestConnectivity(ip, port, totalTries)
  if err:
    logFile.write("\n\nAll failed")
  else:
    logFile.write('\n\n\nVerified full external network connectivity for VM\n\n')
  logFile.close()

def main(argv):
  ip = "127.0.0.1"
  port = 80
  waitTime = 20
  totalTries = 100
  outFileName = ''
  try:
      opts, args = getopt.getopt(sys.argv[1:],"hpwti:o:")
  except getopt.GetoptError:
    print('testOutConnectivity.py\n-i IP\n-o Outfile\n')
    sys.exit(2)
  for opt, arg in opts:
      if opt == '-h':
         print('testOutConnectivity.py\n-i IP\n-p Port\n-w Wait\n-t Total attempts\n-o Outfile\n')
         sys.exit()
      elif opt in ("-i"):
         ip = arg
      elif opt in ("-p"):
         port = arg
      elif opt in ("-w"):
         waitTime = arg
      elif opt in ("-t"):
         totalTries = arg
      elif opt in ("-o"):
         outFileName = arg
  WaitForNetwork(ip, port, waitTime, totalTries, outFileName)

if __name__ == "__main__":
  main(sys.argv[1:])