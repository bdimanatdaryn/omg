import json

with open("sample-data.json", "r") as openfile:
    data = json.load(openfile)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':15} {'Speed':7} {'MTU'}")
print("-" * 80)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]

    dn = attr.get("dn", "")
    descr = attr.get("descr", "")
    speed = attr.get("speed", "")
    mtu = attr.get("mtu", "")

    print(f"{dn:50} {descr:15} {speed} {mtu}")