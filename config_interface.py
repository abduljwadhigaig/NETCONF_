This is the main script
from ncclient import manager
import xmltodict
CiscoC= { # this dictionary contains the Device details which needs to be change 
        "host": "192.168.148.75",
        "username": "cisco",
        "password": "cisco",
        "port": "830",
        "hostkey_verify" : False,
      
    }

def GigabitEthernet ():
    # please note here the interfaces GigabitEthernet needs the shutdown deleted ONLY once. Otherwise, an error would occur 
    # <shutdown xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"/>
    # This dictionary will configure the interface ip and subnet mask using the name of the interface GigabitEthernet
    netconf_template = open("config-temp-ietf-interfaces.xml").read()
    name = input("GigabitEthernet name : \n ")
    ip_address = input("ip_address : \n ")
    subnet_mask = input("subnet_mask : \n ")
    # Build the XML Configuration to be Sent
    netconf_payload = netconf_template.format(int_name= name,ip_address= ip_address,subnet_mask= subnet_mask  )
    print("Configuration Payload GigabitEthernet {name}:")
    print("----------------------")
    print(netconf_payload)
    # Send NETCONF <edit-config> using the option test-then-set which can be changed depending on your needs
    netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
    # Print the NETCONF Reply that would show if the configuration was succeeded or not
    print(netconf_reply)


def looback () :
    # This dictionary will configure the loopback interface ip and subnet mask using the name of the interface loopback
    netconf_template = open("config-temp-ietf-loopback.xml").read() # reading the XML template that contains the configurations
    name = input("LoopBack name : \n ")
    ip_address = input("ip_address : \n ")
    subnet_mask = input("subnet_mask : \n ")
    # Build the XML Configuration to Sent
    netconf_payload = netconf_template.format(int_name= name,
                                              ip_address= ip_address,
                                              subnet_mask= subnet_mask
                                              )
    print("Configuration Payload LoopBack {name}:")
    print("----------------------")
    print(netconf_payload)
    # Send NETCONF <edit-config>
    netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
    # Print the NETCONF Reply
    print(netconf_reply)

def passive_interface(OSPF_ID) :
        # Here we creat how many passive-interfaces do we have in our router, you can choose as mach as you need
        passive_interface_number = input("How many passive-interfaces do you have ?  : \n ")
        i=1 # i is the parameter for number of passive-interfaces
        while i <= int(passive_interface_number) :
            netconf_template = open("ospf_passive_interface.xml").read()# reading the XML template that contains the configurations
            passive_interface = input("passive-interface-number : \n ")
            # Build the XML Configuration to Sent
            netconf_payload = netconf_template.format( OSPF_ID= OSPF_ID,
                                                    passive_interface= passive_interface 
                                              ) 
            netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
            # Print the NETCONF Reply
            print(netconf_reply)
            i += 1

def network_ip(OSPF_ID) :
        # Here we creat how many advertised network do we have in our router, you can choose as mach as you need
        network_ip_number = input("How many advertised network do you have ? : \n ")
        i=1 
        while i <= int(network_ip_number) :
            netconf_template = open("ospf_network.xml").read()
            network_ip = input("network_ip : \n ")
            network_mask = input("network_mask: \n ")
            network_area = input("network_area : \n ")
            netconf_payload = netconf_template.format( OSPF_ID= OSPF_ID,
                                              network_ip= network_ip,
                                              network_mask= network_mask,
                                              network_area= network_area,
                                              )
            netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
            # Print the NETCONF Reply
            print(netconf_reply)
            i += 1

def ospf () :
        # Here we creat the OSPF protocol
        netconf_template = open("ospf.xml").read()
        OSPF_ID = input("OSPF-ID : \n ")
        router_id = input("router-id : \n ")
        redistribute_BGP_AS_Number = input("redistribute-BGP-AS-Number : \n ")
        #    Build the XML Configuration to Send
        netconf_payload = netconf_template.format(OSPF_ID= OSPF_ID,
                                              router_id= router_id,
                                              passive_interface= passive_interface,
                                              redistribute_BGP_AS_Number= redistribute_BGP_AS_Number,
    
                                              )
        print("Configuration Payload OSPF {OSPF_ID}:")
        print("----------------------")
        print(netconf_payload)
        # Send NETCONF <edit-config>
        netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
        # Print the NETCONF Reply
        print(netconf_reply)
        passive_interface(OSPF_ID)
        network_ip(OSPF_ID)

def bgp_neighbor (bgp_ID):
    # Here we creat how many bgp_neighbor do we have in our router, you can choose as mach as you need
    neighbor_number = input("How many neighbors do you have? : \n ")
    i=1 
    while i <= int(neighbor_number) :
        netconf_template = open("bgp.xml").read()
        neighbor_id= input("neighbor-ip: \n ")
        remote_as = input("remote_as : \n ")
        netconf_payload = netconf_template.format(bgp_ID= bgp_ID,
                                              neighbor_id= neighbor_id,
                                              remote_as= remote_as,
                                                 )
        netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
        # Print the NETCONF Reply
        print(netconf_reply)
        i += 1


def bgp_network (bgp_ID):
    # Here we creat how many bgp_network do we have in our router, you can choose as mach as you need
    network_number = input("How many BGP advertised network do you have ?: \n ")
    i=1 
    while i <= int(network_number) :
        netconf_template = open("bgp_network_advertised.xml").read()
        network_ip = input("network_ip : \n ")
        network_mask = input("network_mask : \n ")
        netconf_payload = netconf_template.format(bgp_ID= bgp_ID,
                                              network_ip= network_ip,
                                              network_mask= network_mask,
                                                 )
        netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
        # Print the NETCONF Reply
        print(netconf_reply)
        i += 1

        
def bgp () :
        # Here we creat the BGP protocol
        bgp_ID = input("BGP-AS : \n ")
        bgp_neighbor (bgp_ID)
        bgp_network (bgp_ID)
        netconf_template = open("bgp_redistribute.xml").read()
        redistribute_ospf_id = input("redistribute_ospf_id : \n ")
        #    Build the XML Configuration to Send
        netconf_payload = netconf_template.format(bgp_ID= bgp_ID,
                                              redistribute_ospf_id= redistribute_ospf_id,
                                              )
        print("Configuration Payload BGP {bgp_ID}:")
        print("----------------------")
        print(netconf_payload)
        # Send NETCONF <edit-config>
        netconf_reply= m.edit_config(netconf_payload, target="running",test_option='test-then-set')
        # Print the NETCONF Reply
        print(netconf_reply)

def lock () :
    # This dictionary is responsible for Locking the router configuration, which means no one else can edit while you are configuring
    netconf_reply= m.lock(target="running")
    # Print the NETCONF Reply
    print(netconf_reply)



def unlock () :
    # This dictionary is responsible for unLocking the router configuration
    netconf_reply= m.unlock(target="running")
    # Print the NETCONF Reply
    print(netconf_reply)

# this the main code
# PLEASE note that if you accidentally locked the router device twice, the router might crash
if __name__ == '__main__':
    print('DONT FORGET TO LOCK AND UNLOCK')
    interface = input("Enter the type of Operation : \n 1-GigabitEthernet Configration \n 2-loopback Configration 3-OSPF Configration \n 4-BGP Configration \n 5-Lock \n 6-Unlock\n 7-Exit \n")
    with manager.connect(**CiscoC) as m: # we use the imported ncclient library "manager" to connect to the Device. "**" used to unpack the dictionary
        while interface != '7' :
            match interface: 
                case "1":
                    GigabitEthernet () 
                case "2":
                    looback ()
                case "3":
                    ospf ()
                case "4":
                    bgp ()
                case "5":
                    lock ()
                case "6":
                    unlock ()
            interface = input("Enter the type of Operation : \n 1-GigabitEthernet Configration \n 2-loopback Configration 3-OSPF Configration \n 4-BGP Configration \n 5-Lock \n 6-Unlock\n 7-Exit \n")
    print('Session Closed')
