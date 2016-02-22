1) open a new terminal and type the following:
   'nc -u -l 8192 > ~/Documents/log_data_imu_gps.log'
   press enter (this starts up a server to listen for the data)
2) find your ip address by (in a new terminal) typing "ifconfig" and
   look for an "inet" address (should be something like 10.12.16.23)

3) use this inet address and 8192 as the port on the android app and
   start collecting/sending data

4) when you're done sending data to your laptop, press Control-C in
   the terminal where you issued the "nc -u -l 8192" to close the server

5) you should have a file called ~/Documents/log_data_imu_gps.log
   (you can check this by executing "less ~/Documents/log_data_imu_gps.log"
   in a new terminal and see if your data shows up)

6) now, to convert the data to csv that can be imported into
   excel/google docs, do the following in a terminal:

   "python ~/Downloads/jackson_data.py < ~/Documents/log_data_imu.gps.log > ~/Documents/log_data_formatted.csv"
