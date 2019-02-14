# ogp-agent-monitoring-script
Python script to monitor Open Game Panel (OGP) agents to make sure they are up and running properly.

# Prereqs
You'll need to download and install a few python packages before this will work.  Use the below commands on a Debian / Ubuntu based system.

```
sudo pip install xxtea-py
sudo pip install cffi
```
# Usage
Change the variables section of ogp_monitor.py to use your OGP agent IP address, port, and encryption key.  Multiple entries are supported.  Takes the format of:

`OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY;OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY;OGP_AGENT_IP,OGP_AGENT_PORT,OGP_AGENT_KEY`

This allows the script to monitor multiple different agents.

Change `youremailaddress@yourdomain.com` to your notification email address if you'd like to receive an email alert when any of your OGP agents is down.  
