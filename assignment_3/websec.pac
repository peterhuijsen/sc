function FindProxyForURL(url, host){
    if ( dnsDomainIs(host,"websec2026.liacs.nl") ) {
        return "SOCKS5 127.0.0.1:12345" ;
    }
}

