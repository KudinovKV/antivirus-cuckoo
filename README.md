# antivirus-cuckoo

*cuckoo_start_scan* - main file to start scanning
*cuckoo_worker* - all requests to Cuckoo Sandbox Server
*myparser* - Random forest classifier (malware/clear)

# Start working

1. Run Cuckoo Server on another VM.

> virtualbox
> cuckoo api -H 0.0.0.0
> cuckoo -d

2. Installing python3.
3. Change your *auth_token* on *cuckoo_start_scan*.
4. Run *cuckoo_start_scan* like:

> python cuckoo_start_scan.py /path/to/file <ip> <port>