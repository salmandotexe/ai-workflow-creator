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
| Large Language Model  | OpenAI (GPT 3.5 turbo)                    |
| Logging and metrics   | Grafana + Prometheus                      |
| Flower                | Task Monitoring Dashboard                 |

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
        "instruction": "Go to en.wikipedia.org, type in FastAPI, click on <button class='cdx-button cdx-button--action-default cdx-button--weight-normal cdx-button--size-medium cdx-button--framed cdx-search-input__end-button'>Search</button> . wait 1 second, take a screenshot"
    }


# Output:


    {
    "task_id": "1e80eebf-da7d-408d-8c1a-b456ec98868d",
        "workflow": [
            {
                "action": "goto",
                "url": "https://en.wikipedia.org"
            },
            {
                "action": "type",
                "selector": "#searchInput",
                "value": "FastAPI"
            },
            {
                "action": "click",
                "selector": ".cdx-button.cdx-button--action-default.cdx-button--weight-normal.cdx-button--size-medium.cdx-button--framed.cdx-search-input__end-button"
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