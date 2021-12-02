# zerotier-corosync-pacemaker
Implement Floating IP using Zerotier private controller network to be used in a High Availability Setup with Corosync, Pacemaker

>Make sure that python is in your PATH which python should output the path to python binary

Create Floating IP Reassignment Resource Agent:

1- Download assign-ip Script:
```sh
sudo curl -L -o /usr/local/bin/assign-ip https://raw.githubusercontent.com/heshamyosry/zerotier-corosync-pacemaker/main/assign-ip.py
```
2- Make it executable:
```sh
sudo chmod +x /usr/local/bin/assign-ip
```
Use of the assign-ip script requires the following details:

> Your Zerotier API token must be in the "zt_token" environmental variable
Your Zerotier API URL must be in the "zt_controllerURL" environmental variable
Your Zerotier Network ID must be in the "network_id" environmental variable
Floating IP: The first argument to the script, the Floating IP that is being assigned
Node ID: The second argument to the script, the Node ID that the Floating IP should be assigned to

3- Download FloatIP OCF Resource Agent:
```sh
sudo mkdir /usr/lib/ocf/resource.d/zerotier
sudo curl -o /usr/lib/ocf/resource.d/zerotier/floatip https://raw.githubusercontent.com/heshamyosry/zerotier-corosync-pacemaker/main/floatip
sudo chmod +x /usr/lib/ocf/resource.d/zerotier/floatip
```
4- Add FloatIP Resource:
```sh
sudo crm configure primitive FloatIP ocf:zerotier:floatip \
  params zt_token=your_personal_access_token \
  floating_ip=your_floating_ip \
  zt_controllerURL=http://controller-url \
  zt_networkID=faf3b5e040a6aab9	
```

If you check the status of your cluster (sudo crm status or sudo crm_mon), you should see that the FloatIP resource is defined and started on one of your nodes
