#!/bin/bash
sudo docker run -ti --name google -p 5035:5000 -p 5036:5001 --rm --env-file environment $HOME/gitlab/fce/produccion/google google
