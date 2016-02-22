1) open up a terminal wherever you saved the data_collector.py file
   and execute the command "./data_collector.py"
   (or "python data_collector.py")

2) find your ip address by (in a new terminal) typing "ifconfig" and
   look for an "inet" address (should be something like 10.12.16.23).
   should be under the "wlan0" (wifi) interface section.

3) use this inet address and 8190 as the port on the android app and
   start collecting/sending data

4) when you're done sending data to your laptop, press Control-C in
   the terminal where you issued the "data_collector.py" to close the server

5) you should have a file called ./output.csv
   (you can check this by executing "less ./output.csv"
   in a new terminal and see if your data shows up)

6) Import this file in excel/google sheets, hope it works
