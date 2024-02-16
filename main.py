import DataProcessing
import DbUtils


def main():
    conn, cursor = DbUtils.open_db("Comp490Jobs.sqlite")
    DbUtils.setup_db(cursor)
    api_jobs_data = DataProcessing.get_multiple_pages_of_jobs(15)
    DbUtils.save_to_db(cursor, api_jobs_data)
    excel_jobs_data = DataProcessing.get_excel_data("Sprint3Data.xlsx")
    DbUtils.save_to_db(cursor, excel_jobs_data)
    DbUtils.close_db(conn)


def save_output(data_to_write: list[dict]):
    output_file = open("output.txt", "w")
    for job in data_to_write:
        print(job, file=output_file)
    output_file.close()


if __name__ == '__main__':
    main()
