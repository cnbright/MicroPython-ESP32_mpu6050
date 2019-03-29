
ip_addr = '127.0.0.1'

def do_connect(host, password):
    global ip_addr
    import network
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)

    if not sta_if.isconnected():

        print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(host, password)
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())
    ip_addr = sta_if.ifconfig()[0]
    return ip_addr