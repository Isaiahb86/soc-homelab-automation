sudo ls /root

#fake cron job
echo  " * * * * *  echo 'health check complete'" | crontab -


#generate a syslog entry
logger "simulated cron job and sudo command on $(hostname)"


