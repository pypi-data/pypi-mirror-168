#!/bin/bash


# Download openshift OKD tarfile

wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz

tar xvf openshift-origin-client-tools*.tar.gz

cd openshift-origin-client*/
sudo mv  oc kubectl  /usr/local/bin/


cat << EOF | sudo tee /etc/docker/daemon.json
 {
     "insecure-registries" : [ "172.30.0.0/16" ]
 }
EOF

sudo systemctl restart docker

export $HOST_IP=$(hostname -I | cut -d' ' -f1)


oc cluster up --public-hostname=$HOST_IP

oc login -u system:admin
