#!/bin/sh
SSH=`/sbin/service --status-all | grep ssh | grep + `
if [ -n "$SSH" ];then
	echo "ssh start"
else
	echo "ssh not start"
fi
WWW=`/sbin/service --status-all | grep www | grep + `
if [ -n "$WWW" ];then
		echo "www start"
	else
			echo "www not start"
fi
FTP=`/sbin/service --status-all | grep ftp | grep + `
if [ -n "$FTP" ];then
		echo "ftp start"
	else
			echo "ftp not start"
fi
POP3=`/sbin/service --status-all | grep pop3 | grep + `
if [ -n "$POP3" ];then
		echo "pop3 start"
	else
			echo "pop3 not start"
fi
SENDMAIL=`/sbin/service --status-all | grep sendmail | grep + `
if [ -n "$SENDMAIL" ];then
		echo "sendmail start"
	else
			echo "sendmail not start"
fi

