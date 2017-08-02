sudo docker run -ti --name users -v $(pwd)/src:/src -p 6000:5000 -p 6001:5001 -p 6002:5002 --env-file /home/pablo/gitlab/fce/pablo/environment-usuarios-econo users
