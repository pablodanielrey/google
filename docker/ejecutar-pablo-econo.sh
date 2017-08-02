sudo docker run -ti --name google -v $(pwd)/src:/src -p 7000:5000 -p 7001:5001 -p 7002:5002 --env-file /home/pablo/gitlab/fce/pablo/environment-google-econo google
