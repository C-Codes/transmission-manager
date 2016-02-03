## transmission-manager

A management application for the BitTorrent Client [Transmission](http://www.transmissionbt.com/ "Transmission Homepage") written in Python.

## What do I need?

Developed to run under Python 2.7 (with Python 3.4 in mind). Requires the `transmission-remote` to be installed and present in your `$PATH`. It is distributed as part of the transmission project and can usually be installed through your package manager. (Note: installing `transmission` as part of homebrew under Mac OS X will install `transmission-remote`).

## Do I need this?

If you have a fast internet connection and/or never experience network latency or buffering issues while using Transmission, this is definitely **not** for you. In other words: If you are paying your ISP for a 100 Mbps connection and they can actually deliver such speeds, congratulations, this is probably not for you. If, however, you are in fact on a +/- 20 Mbps contract that actually only nets about 3 Mbps or less, which unfortunately is still quite common, this might be for you!

The motivation to develop and use this application is related to a desire to improve internet connectivity in any given household. It is mainly driven by slow access to the internet, which causes bottleneck situations when many people would like to use a single connection at the same time. Technically, your router could and will do this through QoS to prioritize activity on your network. Unfortunately, this doesn't always work too well when using Transmission at the same time, though - at least it doesn't for me. Therefore, I keep manually switching Transmission between "Speed Limit" and "Normal Speed" modes. Yes, you can also schedule these things in Transmission itself, which is great, but simply doesn't offer enough flexibility or any kind of dynamic adjustment.

## Usage

Make sure Transmission is running on your machine (or you know where it is running - see ##Remote Access for more info).

## Remote Access

If you are using the Transmission app under Mac OS X, you can go into the preferences and simply enable "Remote Access". All interesting settings can be configured there (authentication, port, IP access limitations).

In this example I assume you require no authentication and are using the default port 9091 with transmission running on a local machine with the IP: 10.0.1.10. If you open your browser and navigate to http://10.0.1.10:9091 you should be able to see the list of torrents managed by transmission.
