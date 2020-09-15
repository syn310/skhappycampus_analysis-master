# skhappycampus_analysis

The most appropriate company recommendation logic

cd C:\workspace\skhappycampus_analysis
docker build --tag analysis:0.1 .
docker images
docker run -it -p 80:80 -p 8082:8082 analysis:0.1
docker ps

# mysql access
use mysql;
grant all privileges on *.* to root@'%' identified by 'skcc';

# example API Test
http://localhost/analysis/1/0620ksy@naver.com


# Docker Study
https://www.katacoda.com/
