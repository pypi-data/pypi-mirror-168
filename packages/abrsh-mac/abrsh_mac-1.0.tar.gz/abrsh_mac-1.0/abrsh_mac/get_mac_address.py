import re
import subprocess


def get_mac(interfaces):
    """Return list of macs for the interfaces.
    Take a list of interfaces and return list of macs is exsits otherwise None.
    """
    macs = {}
    pattern = re.compile(r"(\w\w:){5}\w\w")

    def wrapper():
        for interface in interfaces():
            ifconfig = subprocess.check_output(["ifconfig", interface], text=True)
            macs[interface] = (
                pattern.search(ifconfig).group(0)
                if (pattern.search(ifconfig) != None)
                else None
            )
        macs2 = {}
        for key, value in macs.items():
            if value != None:
                macs2[key] = value
        return macs2

    return wrapper


@get_mac
def get_interfaces():
    ifconfig = subprocess.check_output(["ifconfig"], text=True)
    pattern = re.compile(r"(\w+):\sflags")
    return pattern.findall(ifconfig)


if __name__ == "__main__":
    for inter, mac in get_interfaces().items():
        print(inter, "=", mac)
