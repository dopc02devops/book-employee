# Python-API-Framework

# Stop running process
    # brew services stop postgresql
    # lsof -i :5432
    # netstat -tuln | grep 5432
    # ps aux | grep postgres
    # sudo kill 54912


# Run application
    # cd to Employee-App
    # python3 -m venv venv
    # source venv/bin/activate
    # pip3 freeze > requirements.txt
    # set localdb = True
    # install db
        # docker pull amazon/dynamodb-local
        # docker run --name my-dynamo-db -p 8000:8000 amazon/dynamodb-local
    # python3 application.py
# Ducker build
    # docker login -u=dockerelvis -p=Simon197890
    # docker buildx build --platform linux/arm64 -t dockerelvis/k8employeehelm:latest --push .
# Multi-platform
    # docker buildx build --platform linux/amd64,linux/arm64 -t dockerelvis/k8employeehelm:latest --push .
------------------------------------------------------------------------------------------------------------
# Get index page
curl --location 'http://localhost:9001/Employee/index'

curl --location 'http://localhost:9001/Employee?id=1'

curl --location 'http://localhost:9001/Employee/allEmployees'
------------------------------------------------------------------------------------------------------------
# Put
curl --location --request PUT 'http://localhost:9001/Employee' \
--header 'Content-Type: application/json' \
--data '[{"name": "Elizabeth", "id": 0, "age": 54, "address": "40 Highwood Drive", "gender": "Male"}]'
------------------------------------------------------------------------------------------------------------
# Update Post
curl --location 'http://localhost:9001/Employee' \
--header 'Content-Type: application/json' \
--data '[{"name": "Elizabeth", "id": 1, "age": 5433, "address": "40 Highwood Drive", "gender": "Male"}]'
------------------------------------------------------------------------------------------------------------
# Delete
curl --location --request DELETE 'http://localhost:9001/Employee?id=2&name=Elizabeth' \
--header 'Content-Type: application/json' \
--data '[{"name": "Elizabeth", "id": 1, "age": 5433, "address": "40 Highwood Drive", "gender": "Male"}]'

curl --location --request DELETE 'http://localhost:9001/Employee/Employee_DB'
------------------------------------------------------------------------------------------------------------
