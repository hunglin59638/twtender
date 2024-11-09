# Taiwan Tender API

This API allows you to search for Taiwan procurement tenders. The data is sourced from the [政府電子採購網](https://web.pcc.gov.tw/pis/).

## Usage

available at [https://tender.hlin.tw/](https://tender.hlin.tw/)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/hunglin59638/twtender.git
    cd twtender
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python -m twtender.main
    ```
4. Open the browser and go to [http://localhost:8000/](http://localhost:8000/)
5. You can also access the Swagger documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

### Docker Usage

#### Build and Run the Docker Container

1. Build the Docker image:
    ```bash
    docker build -t twtender .
    ```

2. Run the Docker container:
    ```bash
    docker run --rm -p 8000:8000 twtender
    ```

#### Use Pre-built Docker Image

1. Pull the Docker image from Docker Hub:
    ```bash
    docker pull hunglin59638/twtender:latest
    ```

2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 hunglin59638/twtender:latest
    ```

### Endpoints

#### Search Tenders

`GET /`

##### Query Parameters

[https://tender.hlin.tw/docs](https://tender.hlin.tw/docs)

- `tender_name` (Optional): Name of the tender.
- `tender_id` (Optional): ID of the tender.
- `org_id` (Optional): ID of the organization.
- `start_date` (Optional): Start date in the format 'yyyy/mm/dd'.
- `end_date` (Optional): End date in the format 'yyyy/mm/dd'.
- `p` (Optional): Page number (default: 1).
- `page_size` (Optional): Number of results per page (default: 100).
- `format` (Optional): Response format, either 'json' or 'html' (default: 'html').

##### Example Request

```bash
curl -X GET "http://localhost:8000?start_date=2023/01/01&end_date=2023/12/31&format=json"
{
  "標案編號": ["12345", "67890"],
  "標案名稱": ["Example Tender 1", "Example Tender 2"],
  // ...other fields...
}
```