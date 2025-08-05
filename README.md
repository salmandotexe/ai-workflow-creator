# AI-workflow-creator
Supports creation of AI workflows seamlessly

# Technology
| Component          | Technology              |
| ------------------ | ----------------------- |
| Web Framework      | FastAPI                 |
| Task queue         | Celery                  |
| Broker             | RabbitMQ                |
| Result Backend     | MongoDB                 |
| Browser Automation | Playwright              |
| Containerization   | Docker & Docker Compose |
| Flower             | Celery Task Monitoring Dashboard|

# High-Level Architecture

                                      +------------------+
                                      |   Client (User)  |
                                      +--------+---------+
                                               |
                                               v
                                      +--------+---------+
                                      |    FastAPI API   |
                                      +--------+---------+
                                               |
                                               v
                                      +--------+---------+
                                      |    RabbitMQ      |
                                      +--------+---------+
                                               |
                           +-------------------+-------------------------+
                           |                                             |
                           v                                             v
                  +--------+---------+                          +--------+---------+
                  |  Celery Worker    |  <-----> MongoDB        |  Celery Results  |
                  | (Executes Workflow|       (Results,         |  Backend + Logs  |
                  |  & Automation)    |      Workflow Logs)     |                  |
                  +-------------------+                         +------------------+
                           |
                           v
               +-----------+-------------+
               | Browser Automation Task  |
               |   (Playwright Headless)  |
               +-------------------------+

                                      +-------------------+
                                      |     Flower UI     |
                                      | (Task Monitoring) |
                                      +-------------------+

# Installation

`docker-compose up --build`