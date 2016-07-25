#!/bin/bash
# Script that uploads all files in current directory to EC2 Onboarding API folder (~/scripts/onboarding)
files=("config" "docs" "v1" "README.md" "API-REFERENCE.md")

if [ $# -eq 0 ]
  then
    echo "No private key file supplied."
    echo "Call this script as follows: ./update_server.sh \"/path/to/key.pem\""
    exit
fi

for i in "${files[@]}"
do
	 scp -i $1 -r ./$i  ubuntu@nlp.engazeapp.com:/home/ubuntu/api/$i
done

if [ "$2" = "reload" ]
  then
  	echo "Reloading gunicorn... "
    ssh -i $1 ubuntu@nlp.engazeapp.com "sudo initctl reload engazeapi"
    if [ $? -eq 0 ]
      then
        echo "Success."
    else
    	echo "Failed."
    fi	
    exit
fi