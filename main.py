from serpapi import GoogleSearch
import secrets


def main():
    complete_data = []
    for page in range(5):
        current_data = get_data(page)
        complete_data.extend(current_data)
    save_output(complete_data)


def get_data(page: int) -> dict:
    params = {
        "api_key": secrets.api_key,
        "engine": "google_jobs",
        "q": "Software Developer",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "us",
        "location": "Boston, Massachusetts, United States",
        "start": page,
        "lrad": "100"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results["jobs_results"]


def save_output(data_to_write: list[dict]):
    output_file = open("output.txt", "w")
    for job in data_to_write:
        print(job, file=output_file)
    output_file.close()


if __name__ == '__main__':
    main()
