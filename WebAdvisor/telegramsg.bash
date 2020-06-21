#!/bin/bash
 
TOKEN="882587231:AAE5Cxj4gUepjJGT1voD6u12mSyS1tW0T1Q"
 
USER=$1
SUBJECT=$2
 
curl --silent --output /dev/null "https://api.telegram.org/bot$TOKEN/sendMessage?chat_id=$USER&text=$SUBJECT"
 
exit 0
----------------