import net_automation

edge_dn42_lan = net_automation.Vyos(
    device_type = "vyos",
    host = "edge.dn42.lan",
    username = "test",
    password = "test",
)

edge_dn42_lan.init_ssh()

result =  (edge_dn42_lan.get_bgp_summary())

for i in result:
    print (i)