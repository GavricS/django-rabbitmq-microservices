# Microservice architecture proof-of-concept implemented in Python
## Introduction
This project is a proof-of-concept of microservice architecture built using Django 4. It implements the same business logic as [TDD Microservice in PHP](https://github.com/madeindra/codeigniter-microservice/tree/master), with some tecnhical improvements.

The system consists of three separate microservices: order service, financial service and warehouse service. Each service handles one part of the business logic of the system:
- Order service handles order logic - it has access to the order database and provides a REST REST API for the order entity. It also provides an endpoint for "checking out" the order, which notifies the rest of the system (through the RabbitMQ infrastructure) that the checkout flow should begin.
- Financial service handles invoice logic - it has access to the invoice database and provides a REST API for the invoice entity. It also hosts a worker that handles RabbitMQ communication.
- Warehouse service handles product logic - it has access to the product database and provides a REST API for the product entity. It also hosts a worker that handles RabbitMQ communication.

The control flow is identical as described [here](https://github.com/madeindra/codeigniter-microservice/tree/master#architecture)

## Prerequisites
- Docker

## Usage
Just compose up:
```bash
docker compose up
```

If running for the first time, connect to order, financial and warehouse containers and execute migrations:
```bash
python manage.py migrate
```