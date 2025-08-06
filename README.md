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

# Example

Endpoint `/api/v1/run-workflow/` payload:

    {
        "steps":[
            {
            "action": "goto",
            "url": "https://www.google.com"
            },
            {
            "action": "type",
            "selector": "textarea.gLFyf",
            "value": "youtube"
            },
            {
            "action": "click",
            "selector": "input.gNO89b"
            },
            {
            "action": "screenshot",
            "path": "screenshot.png"
            }
        ]
    }
