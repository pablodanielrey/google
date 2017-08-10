sudo docker run -ti --name google -v $(pwd)/src:/src -p 8000:5000 -p 8001:5001 -p 8002:5002 --env-file /home/emanuel/econo/gitlab/fce/pablo/environment-google-econo google
