#!/bin/bash
sudo docker run -d --name google -v $(pwd)/src:/src -p 5035:5000 -p 5036:5001 --name google --rm --env-file $HOME/gitlab/fce/produccion/google google
sudo docker exec -t google bash instalar.sh
sudo docker restart google

