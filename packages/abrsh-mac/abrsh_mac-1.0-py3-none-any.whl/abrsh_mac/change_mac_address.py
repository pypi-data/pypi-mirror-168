import subprocess
from mac_address.get_mac_address import get_interfaces


old_mac = get_interfaces()
print(f"old mac: {old_mac}")

for i in get_interfaces().keys():
    subprocess.run(f"sudo ifconfig {i} down", shell=True)
    subprocess.run(f'sudo ifconfig {i} hw ether {input("enter new mac: ")}', shell=True)
    subprocess.run(f"sudo ifconfig {i} up", shell=True)

print(f"new mac: {get_interfaces()}")
