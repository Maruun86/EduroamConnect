Modifed Files
=============

/etc/network/interfaces
-----------------------
.. code-block:: console
    
    allow-hotplug wlan0
    iface wlan0 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

/etc/wpa_supplicant/wpa_supplicant.conf 
---------------------------------------
.. code-block:: console

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=DE

    network={
        ssid="eduroam"
        proto=RSN
        key_mgmt=WPA-EAP
        eap=PEAP
        identity="USER@HOST"
        password="PASSWORD"
        phase1="peaplabel=0"
        phase2="auth=MSCHAPV2"
    }

/etc/systemd/timesyncd.conf
---------------------------
.. code-block:: console

    [TIME]
    NTP=time.jade-hs.de
    RootDistanceMaxSec=5
