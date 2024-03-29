import re
import openpyxl
import secrets
from serpapi import GoogleSearch
from typing import Tuple, List


def get_data(page: int) -> List[dict]:
    params = {
        "api_key": secrets.api_key,
        "engine": "google_jobs",
        "q": "Software Developer",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "location": "Boston, Massachusetts, United States",
        "start": page,
        "lrad": "100",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results["jobs_results"]


def get_multiple_pages_of_jobs(num_pages: int) -> List[tuple]:
    complete_data = []
    for page in range(num_pages):
        current_data = get_data(page)
        clean_data = clean_data_for_db(current_data)
        complete_data.extend(clean_data)
    return complete_data


def clean_data_for_db(raw_job_data: list[dict]) -> list[Tuple]:
    """this is a DRY violation, but I want it to be easy to follow, so I'll put it in here for now
    There should really be one canonical location to the database structure"""
    db_ready_data = []
    for job in raw_job_data:
        job_id = job["job_id"]
        job_title = job["title"]
        company_name = job["company_name"]
        job_description = job["description"]
        location = job["location"]
        posted_date = ""
        remote = False
        optional_job_data = job["detected_extensions"]
        if optional_job_data.get("posted_at"):
            posted_date = optional_job_data["posted_at"]
        if optional_job_data.get("work_from_home"):
            remote = True  # A little optimistic, but all of my data only has work_from_home when TRUE
        url = job["related_links"][0]["link"]  # related_lists is a list of dictionaries
        job_highlights = job["job_highlights"]
        benefits_section = {}
        # the benefits section can be in and position in the job_highlights list, so we look for it
        for section in job_highlights:
            if section.get("title") == "Benefits":
                benefits_section = section
        min_salary, max_salary = get_salary(benefits_section, job_description.lower())
        salary_time_period = "N/A"
        if 0 < min_salary < 900:
            salary_time_period = "Hourly"
        elif min_salary > 0:
            salary_time_period = "Yearly"
        prepared_data = (
            job_id,
            job_title,
            company_name,
            job_description,
            location,
            min_salary,
            max_salary,
            salary_time_period,
            posted_date,
            url,
            remote,
        )
        db_ready_data.append(prepared_data)
    return db_ready_data


def get_salary(benefits_section: dict, job_description: str):
    """this is more complicated than you were required to do, I'm looking in several places for salary info"""
    min_salary = 0
    max_salary = 0
    if benefits_section:  # if we got a dictionary with stuff in it
        for benefit_item in benefits_section["items"]:
            if "range" in benefit_item.lower():
                # from https://stackoverflow.com/questions/63714217/how-can-i-extract-numbers-containing-commas-from
                # -strings-in-python
                numbers = re.findall(
                    r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)", benefit_item
                )
                if numbers:  # if we found salary data, return it
                    return int(numbers[0].replace(",", "")), int(
                        numbers[1].replace(",", "")
                    )
            numbers = re.findall(r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)", benefit_item)
            if (
                    len(numbers) == 2 and int(numbers[0].replace(",", "")) > 30
            ):  # some jobs just put the numbers in one item
                # and the the description in another
                return int(numbers[0].replace(",", "")), int(
                    numbers[1].replace(",", "")
                )
            else:
                return min_salary, max_salary
    location = job_description.find("salary range")
    if location < 0:
        location = job_description.find("pay range")
    if location < 0:
        return min_salary, max_salary
    numbers = re.findall(
        r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)",
        job_description[location: location + 50],
    )
    if numbers:
        return int(numbers[0].replace(",", "")), int(numbers[1].replace(",", ""))
    return min_salary, max_salary


def get_excel_data(file_name: str) -> List[Tuple]:
    jobs_data = []
    excel_file = openpyxl.load_workbook(file_name)
    jobs_sheet = excel_file.active
    for row in jobs_sheet.iter_rows(
            min_row=2
    ):  # skip the first row which has the column names in it
        db_ordered_job = order_row_for_db(row)
        jobs_data.append(db_ordered_job)
    return jobs_data


def order_row_for_db(row: tuple) -> tuple:
    remote = False
    if "remote" in row[9].value.lower():
        remote = True
    return (
        row[2].value,  # the job id is in column C
        row[9].value,  # the job title is in column J
        row[0].value,  # the company name is in column A
        "No Description given for job",
        row[4].value,  # the job location is in column E
        row[7].value,  # the max salary is in column G
        row[6].value,  # the min salary is in column H
        row[8].value,  # the time period for the salary is in column I
        row[
            1
        ].value,  # the posted at is either in text in column B - which I have used, or in unix time on column F
        "URL Not Available for job",
        remote,
    )
