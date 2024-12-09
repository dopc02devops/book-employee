# Python-API-Framework

# Stop running process
    # brew services stop postgresql
    # lsof -i :5432
    # netstat -tuln | grep 5432
    # ps aux | grep postgres
    # sudo kill 54912


# Run application
    # cd to Book-App
    # python3 -m venv venv
    # source venv/bin/activate
    # pip3 freeze > requirements.txt
    # set db_Url to LOCAL_DB
    # install db
        # docker pull postgres
        # docker run --name my-postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=Simon1980 -e POSTGRES_DB=flaskdb -p 5432:5432 -d postgres
    # python3 backend/application.py
# Ducker build
    # docker login -u=dockerelvis -p=Simon197890
    # docker buildx build --platform linux/arm64 -t dockerelvis/k8bookhelm:latest --push .
    # docker buildx build --platform linux/arm64 -t dockerelvis/k8nginxhelm:latest --push .
# Multi-platform
    # docker buildx build --platform linux/amd64,linux/arm64 -t dockerelvis/k8bookhelm:latest --push .
    # docker buildx build --platform linux/amd64,linux/arm64 -t dockerelvis/k8nginxhelm:latest --push .
------------------------------------------------------------------------------------------------------------
# Get index page
curl --location 'http://127.0.0.1:8081/book/index'
------------------------------------------------------------------------------------------------------------
