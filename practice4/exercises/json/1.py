import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)

print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print(f"{'-'*50} {'-'*20} {'-'*8} {'-'*6}")

for i in data["imdata"]:
    dn = i["l1PhysIf"]["attributes"]["dn"]
    descr = i["l1PhysIf"]["attributes"]["descr"]
    speed = i["l1PhysIf"]["attributes"]["speed"]
    mtu = i["l1PhysIf"]["attributes"]["mtu"]

    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")