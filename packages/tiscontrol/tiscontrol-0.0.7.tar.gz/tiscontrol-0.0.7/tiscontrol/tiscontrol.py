
import sys
import socket
import time
import logging

_LOGGER = logging.getLogger(__name__)


TRV = {}

sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
UDP_IP = socket.gethostbyname(socket.getfqdn())
# print("udp ip address ",UDP_IP)  
#UDP_IP = socket.gethostbyname(socket.gethostname())

UDP_IP = socket.getfqdn()
print("IP Address:",socket.gethostbyname_ex(UDP_IP)[2][1])

DEFAULT_PROXY_IP = UDP_IP
DEFAULT_PROXY_PORT = 6000


light=[]


class TrvCollector:
    """UDP proxy to collect Lightwave traffic."""

    def __init__(self, verbose):
        """Initialise Collector entity."""
        self.transport = None
        self.verbose = verbose

    def connection_made(self, transport):
        """Start the proxy."""
        self.transport = transport

    # pylint: disable=W0613, R0201
    def datagram_received(self, data, addr):
        """Manage receipt of a UDP packet from Lightwave."""

        #print(self.add_space(self.convert_hex(data)))
        self.store_data(self.convert_hex(data))


    def add_space(self,a):
        # split address to 6 character
        pac=' '.join([a[i:i+2] for i in range(0, len(a), 2)])
        # format to 00:00:00:00:00:00
        return pac

    def convert_hex(self, data):
        res = ""
        for b in data:
            res += "%02x" % b
        return res
    def enquiry(self,list1): 

        return not list1

    def store_data(self, data):

        if(str(data[42:46])=="0034"):
            print("your packet is right 0034",self.add_space(data))
        elif(str(data[42:46])=="0032"):
            print("your packet is right 0032 ",self.add_space(data))
            status_data=data[34:-1]
            print(status_data)
            subnet_id=status_data[0:2]
            device_id=status_data[2:4]
            channel_id=status_data[16:18]
            concat=status_data[0:2]+status_data[2:4]+status_data[16:18]
            level=status_data[20:22]

            if self.enquiry(light): 
                print("The list is Empty") 
                light.append({"level":level,"device_id":concat})
                print(light)
            else: 
                 print("The list isn't empty")
                 for value in light:
                    if(concat==value["device_id"]):
                        value["level"]=level
                        print(light)
                        return 


                


def proxy():
    """Run the LW Proxy."""
   
    print("proxy excuted ")
    message='C0A8018B53'
    sock.sendto(bytes.fromhex(message), (DEFAULT_PROXY_IP, DEFAULT_PROXY_PORT))


def main(argv=None):
    """Start the proxy."""
    if argv is None:
        argv = sys.argv[1:]

    proxy_ip = DEFAULT_PROXY_IP
    proxy_port = DEFAULT_PROXY_PORT
    verbose = False

    print("success ",DEFAULT_PROXY_IP)
    sock.bind(("", DEFAULT_PROXY_PORT))
    
    while True:
        data, addr = sock.recvfrom(65565) # buffer size is 65565 bytes
        #print("received message: %s" % data)
        _LOGGER.warning("received message from TIS server: %s"  % data)
        time.sleep(0.25)


if __name__ == "__main__":
    main()