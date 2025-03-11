- Ensure you have Python install and setup if your ide of choice.

- Start mongodb container for Role Finder DB image.
    cd Docker
    docker compose up

To log into the container
- docker exec -it role_documentdb bash
- mongosh "mongodb://{username}:{password}@localhost:27017/?authSource={authsource}

Then run mongodb commands as needed.