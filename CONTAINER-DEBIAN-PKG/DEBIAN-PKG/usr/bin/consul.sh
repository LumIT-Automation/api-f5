#!/bin/bash

set -e

function start() {
    # Start Consul agent.
    # Bind to *the* interface available within the container.
    # Connect to the server agent's ports, which are "attached" to the HOST IP => so, just find out the default route.
    serverAddress="$(ip route | grep default | grep -oP '(?<=via\ ).*(?=\ dev)')"
    /usr/bin/consul agent -enable-local-script-checks=true -config-dir=/etc/consul.d/ -data-dir=/var/lib/consul/ -retry-join $serverAddress

    # -retry-join allows retrying a join until it is successful.
    # Once it joins successfully to a member in a list of members it will never attempt to join again. Agents will then solely maintain their membership via gossip.
}

function stop() {
    /usr/bin/consul leave
}

function reload() {
    /usr/bin/consul reload
}

function restart() {
    stop
    sleep 1
    start
}

case $1 in
        start)
            start
            ;;

        stop)
            stop
            ;;

        reload)
            reload
            ;;

        restart)
            restart
            ;;

        *)
            echo $"Usage: $0 {start|stop|reload|restart}"
            exit 1
esac

exit 0
