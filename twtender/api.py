#!/usr/bin/env python
import re
import requests
import pandas as pd
from typing import Optional
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
URL = "https://web.pcc.gov.tw/prkms/tender/common/advanced/readTenderAdvanced"


@app.get("/", response_class=HTMLResponse)
async def search_tender(
    tender_name: Optional[str] = Query(None, description="Name of the tender"),
    tender_id: Optional[str] = Query(None, description="ID of the tender"),
    org_id: Optional[str] = Query(None, description="ID of the organization"),
    start_date: Optional[str] = Query(None, description="format: 'yyyy/mm/dd'"),
    end_date: Optional[str] = Query(None, description="format: 'yyyy/mm/dd'"),
    p: Optional[int] = Query(1, description="Page number"),
    page_size: Optional[int] = Query(100, description="Number of results per page"),
    format: Optional[str] = Query(
        "html", description="Response format: 'json' or 'html'"
    ),
):
    if format not in ["json", "html"]:
        return JSONResponse(
            {"error": "Invalid format. Please use 'json' or 'html'."}, status_code=400
        )
    query = {}
    if tender_name:
        query["tenderName"] = tender_name
    if tender_id:
        query["tenderId"] = tender_id
    if org_id:
        query["orgId"] = org_id
    if start_date and end_date:
        query["dateType"] = "isDate"
        query["tenderStartDate"] = start_date
        query["tenderEndDate"] = end_date
    elif start_date or end_date:
        return JSONResponse(
            {"error": "Please provide both start_date and end_date."}, status_code=400
        )
    if len(query) == 0:
        query["dateType"] = "isNow"
    query["d-49738-p"] = p
    query["pageSize"] = page_size

    r = requests.get(URL, params=query)

    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", {"class": "tb_01"})
    headers = [th.text.strip() for th in table.find_all("th")]
    headers.pop(2)
    headers.insert(2, "標案名稱")
    headers.insert(2, "標案編號")

    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = tr.find_all("td")
        row = [cell.text.strip() for cell in cells]
        if len(row) + 1 != len(headers):
            continue

        case_number = cells[2].text.strip(" <\r\n\t")
        case_name_match = re.search(
            r'Geps3\.CNS\.pageCode2Img\("([^"]+)"\)', cells[2].u.script.text
        )
        case_name = case_name_match.group(1) if case_name_match else ""
        row.insert(3, case_name)
        row[2] = case_number
        rows.append(row)

    if len(rows) > 0:
        df = pd.DataFrame(rows, columns=headers)
    else:
        df = pd.DataFrame(columns=headers)
    df = df.drop(columns=[headers[-1]])
    if format == "json":
        return JSONResponse(df.to_dict(orient="list"))
    elif format == "html":
        return HTMLResponse(content=df.to_html(index=False), status_code=200)
    return JSONResponse(df.to_dict(orient="list"))
