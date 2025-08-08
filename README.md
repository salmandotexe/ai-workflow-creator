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
| Logging and metrics   | Grafana + Prometheus                      |
| Flower                | Task Monitoring Dashboard (disabled)      |

# High-Level Architecture

                                                +------------------+
                                                |   Client (User)  |
                                                +--------+---------+
                                                         |
                                                         v
                                                +--------+---------+
                                                |                  |                +--------------+
                                                |                  +<-------------->|    OpenAI    |
                                                |  FastAPI Server  |                +--------------+
                                                |                  +-------------------------------------+
                                                |                  |                                     |
                                                +--------+---------+                                     |
                                                         |                                               |
                                                         v                                               |
                                                +--------+---------+                                     |
                                                |    RabbitMQ      |                                     |
                                                +--------+---------+                                     |
                                                         |                                               |
                             +---------------------------+----------------------------+                  |
                             |                                                        |                  |
                             v                                                        v                  |
                  +----------+----------+                                    +--------+---------+        |
                  |  Celery Worker      |  <--------->  MongoDB              |  Celery Results  |        |
                  | (Executes Workflow  |        ( Results, Workflow Logs    |  Backend + Logs  |        |
                  |    & Automation)    |               & State )            +------------------+        |
                  |                     |                                                                |
                  |                     |-------------------+                                            |
                  +---------------------+                   |                                            |
                             |                              |                                            v
                             v                              |                               +------------+------------+
                 +-----------+-------------+                +------------------------------>+  Shared Storage Volume  |
                 | Browser Automation Task |                                                +-------------------------+
                 |  (Playwright Headless)  |
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
        "instruction":"go to https://en.wikipedia.org/wiki/FastAPI, wait 1 second, take a screenshot"
    }


# Output:


    {
        "task_id": "b89903a3-c50c-44ab-aa40-b49794c68745",
        "workflow": [
            {
                "action": "goto",
                "url": "https://en.wikipedia.org/wiki/FastAPI"
            },
            {
                "action": "wait",
                "value": 1
            },
            {
                "action": "screenshot"
            }
        ]
    }
<img src="examples/aec934918cc845bfb40a43a42d11b53f.png" alt="alt text" width="800">

Endpoint `/api/v1/run-workflow/` payload:

    {
        "steps":[
            {
                "action": "goto",
                "url": "https://en.wikipedia.org/wiki/FastAPI"
            },
            {
                "action": "wait",
                "value": 1
            },
            {
                "action": "screenshot"
            }
        ]
    }