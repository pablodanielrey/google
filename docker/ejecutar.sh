#!/bin/bash
sudo docker run -d --name google -p 5035:5000 -p 5036:5001 --rm --env-file $HOME/gitlab/fce/produccion/google google
