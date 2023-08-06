import textfsm

traceroute = """
Codes: S - State, L - Link, u - Up, D - Down, A - Admin Down
Interface    IP Address                        S/L  Description
---------    ----------                        ---  -----------
eth0         192.168.1.101/24                  u/u  WAN (DMZ of TP Link)
eth1         -                                 u/D  Local
eth2         -                                 u/u  Local
eth3         -                                 u/D  Local
eth4         -                                 u/u  CiscoSW
lo           127.0.0.1/8                       u/u  MGMT
             10.100.100.2/32
             ::1/128
switch0      10.33.2.1/24                      u/u  Local
             2a02:390:953e:2::1/64
wg1          10.33.120.1/24                    u/u  WG Remote Access
wg10         172.22.132.173/30                 u/u  p2p_usman
wg11         172.22.132.176/31                 u/u  p2p_dn42_edge
"""

# with open('vyosint.template') as template:
#     fsm = textfsm.TextFSM(template)
#     result = fsm.ParseText(traceroute)

# print(fsm.header)

# for i in result:
#     print (i)


bgp = """
IPv4 Unicast Summary:
BGP router identifier 172.22.132.166, local AS number 4242421869 vrf-id 0
BGP table version 666516
RIB entries 1459, using 262 KiB of memory
Peers 16, using 327 KiB of memory

Neighbor        V         AS MsgRcvd MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd
fe80::acab      4      64719       0       0        0    0    0    never         Idle
fe80::ade0      4 4242423914       0       0        0    0    0    never         Idle
172.20.16.141   4 4242421588       0       0        0    0    0    never       Active
172.20.43.96    4 4242422459   42569   33246        0    0    0 1d02h08m          504
172.20.53.104   4 4242423914  505069  102913        0    0    0 6d00h08m          506
172.20.222.224  4 4242423192 1036249  617585        0    0    0 1d08h47m          503
172.20.229.116  4 4242421080  912006  348484        0    0    0 02w1d23h          500
172.21.67.200   4 4242422092  484094  352653        0    0    0 1d19h59m          504
172.22.119.1    4      64719  219675  139170        0    0    0 3d01h05m          501
172.22.132.163  4 4242421869   94393  150809        0    0    0 4d00h18m      Connect
172.22.132.178  4 4242421869       0       0        0    0    0    never       Active
172.22.132.181  4 4242421869   36432  558917        0    0    0 4d00h18m       Active
172.23.91.119   4 4242422189       0       0        0    0    0    never      Connect
172.23.120.49   4 4242421720  609194  349753        0    0    0 02w1d23h          509

fe80::ade0      4 4242423914       0       0        0    0    0    never         Idle
Total number of neighbors 16
"""

with open('vyosbgp.template') as template:
    fsm = textfsm.TextFSM(template)
    result = fsm.ParseText(bgp)

for i in result:
    print (i)
    # print ("------------------------")
    # print ("Remote IP:",  i[2])
    # print ("Remote AS:",  i[3])
    # print ("MsgRcvd:",  i[4])
    # print ("MsgSent:",  i[5])
    # print ("Up/Down:",  i[7])
    # print ("State/PfxRcd:",  i[7])
    # print ("")