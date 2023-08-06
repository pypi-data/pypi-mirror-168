#!/bin/bash


# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


#installing POT
# Creating a symbolic link 
source /opt/intel/openvino_2021/bin/setupvars.sh

ln -s /opt/intel/openvino_2021/deployment_tools/tools/ .

echo -e "\e[1;31mSymbolic link created\e[0m"

echo -e "\e[1;32m\nFollow the README.md for usage\e[0m"




