# AI-workflow-creator
Automates Playwright headless browser workflows in parallel, through human language

# Technology
| Component             | Technology                                |
| --------------------- | ----------------------------------------- |
| Web Framework         | FastAPI                                   |
| Task queue            | Celery                                    |
| Broker                | RabbitMQ                                  |
| Result Backend        | MongoDB                                   |
| Browser Automation    | Playwright                                |
| Containerization      | Docker & Docker Compose                   |
| Large Language Model  | OpenAI (GPT 3.5) turbo                    |
| Flower                | Celery Task Monitoring Dashboard (TODO)   |
| Logging and metrics   | Grafana (TODO)                            |

# High-Level Architecture

                                                +------------------+
                                                |   Client (User)  |
                                                +--------+---------+
                                                         |
                                                         v
                                                +--------+---------+
                                                |                  |                +--------------+
                                                |    FastAPI API   +<-------------->|    OpenAI    |
                                                |                  |                +--------------+
                                                +--------+---------+
                                                         |
                                                         v
                                                +--------+---------+
                                                |    RabbitMQ      |
                                                +--------+---------+
                                                         |
                             +---------------------------+----------------------------+
                             |                                                        |
                             v                                                        v
                  +----------+----------+                                    +--------+---------+
                  |  Celery Worker      |  <--------->  MongoDB              |  Celery Results  |
                  | (Executes Workflow  |        ( Results, Workflow Logs    |  Backend + Logs  |
                  |    & Automation)    |               & State )            |                  |
                  +---------------------+                                    +------------------+
                             |
                             v
                 +-----------+-------------+
                 | Browser Automation Task |
                 |   (Playwright Headless) |
                 +-------------------------+

                                                +-------------------+
                                                |     Flower UI     |
                                                | (Task Monitoring) |
                                                +-------------------+

# Installation

`docker-compose up --build`

# Example

Endpoint `/api/v1/generate-workflow/` payload:

    {
        "instruction": "Go to google.com, type youtube in the <textarea class = 'gLFyf'>, click button <input class = 'gNO89b'> then take a screenshot"
    }


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
