Fenum - FTP file Enumerator python script with search (simple and regex) capability 

Usage: fenum.py [-h] [-U USERNAME] [-P PASSWORD] -r RHOST [-p PORT] -l LHOST
                [-t PATH] [-s SEARCH] [-e REGEX]

Arguments : 
  -h, --help            show this help message and exit
  -U USERNAME, --username USERNAME
                        FTP username - default is "anonymous"

  -P PASSWORD, --password PASSWORD
                        FTP password 

  -r RHOST, --remote-host RHOST
                        FTP server IP address

  -p PORT, --port PORT  FTP port - default is 21

  -l LHOST, --local-host LHOST
                        localhost interface IP address to create data
                        connection

  -t PATH, --path PATH  path to start enumeration - default is '/'

  -s SEARCH, --search SEARCH
                        STRING to search in FTP files

  -e REGEX, --regex REGEX
                        regex to search in FTP files


Example : 

	#python3 fenum.py -U anonymous -r 10.10.10.2 -l 192.168.1.1 -e ^pass.* 
