from subprocess import check_output
import requests

def service_alive_check_tcp(ip, port, output_info):
    try:
        check_output(['nc', '-z', ip, str(port)])
        print("TCP {} is alive".format(output_info))
    except:
        print("TCP {} is not alive".format(output_info))
        exit(1)
        
def service_alive_check_udp(ip, port, output_info):
    try:
        check_output(['nc', '-u', '-z', ip, str(port)])
        print("UDP {} is alive".format(output_info))
    except:
        print("UDP {} is not alive".format(output_info))
        exit(1)

def dns_check(url, record_type, test_data, output_info):
    try:
        output = check_output(['dig', '+noall', '+answer', url, record_type, '@8.8.8.8']).decode()
        if test_data in output:
            print("{} Success".format(output_info))
        else:
            raise
    except:
        print("{} Failed".format(output_info))
        exit(1)

def web_check(url):
    try:
        r = requests.get(url)
        if r.status_code == 200 and "<!flag: NAP_2016_Web_Challenge_Part_1>" in r.text:
            print("Web Test Success")
        else:
            raise
    except:
        print("Web Test Failed")
        exit(1)

domain_url= input("Please input your domain name: ")
ip = input("Please input your ip: ")

service_alive_check_tcp(ip, 53, "DNS")

service_alive_check_udp(ip, 53, "DNS")

service_alive_check_tcp(ip, 80, "Web")

dns_check("NAP2016-DNS1.nasa.{}".format(domain_url),
          "cname",
          "IN CNAME nasa.cs.nctu.edu.tw.",
          "DNS1 CNAME")

dns_check("NAP2016-DNS2.nasa.{}".format(domain_url),
          "a",
          ip,
          "DNS2 A Record")

dns_check("NAP2016-WEB1.nasa.{}".format(domain_url),
          "txt",
          "NAP_2016_Web_Challenge_Part_1",
          "WEB1 TXT Record")

web_check("http://NAP2016-WEB1.nasa.{}".format(domain_url))

print("All Tests Success!")
