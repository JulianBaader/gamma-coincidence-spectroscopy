# Setup 
(RedPitaya 00:26:32:F0:C3:8F -> IP-Address may vary)
* Download the [red-pitaya-notes:image](http://pavel-demin.github.io/red-pitaya-notes/alpine/).
* Copy the contents of the downloaded zip-file onto an freshly formatted SD-Card.
* Copy the daq folder into the apps folder.
* To automatically start the daq application upon boot copy the `start.sh` script to the topmost directory on the SD card.
* Insert the SD-Card into the RedPitaya and connect it to Power.
* The green LED on the RedPitay indicates power, the blue LED means the server is running.
* The daq server is compatible with the `projects/mcpha/client/mcpha.py` client from the [red-pitaya-notes:source](https://github.com/pavel-demin/red-pitaya-notes/tree/master).
* Connect the RedPitaya via an Ethernet-USB dongle. Make sure the ?DHCP? is working -> PC: Settings: Network: USB Ethernet: IPv4 and IPv6: Shared to other computers
# Troubleshooting
* A connection the the RedPitaya can be acheived via `ssh root@rp-f0c38f.local` with password: `changeme` or using the [serial connection](https://redpitaya.readthedocs.io/en/latest/developerGuide/software/console/console/console.html).
