import DataProcessing
import DbUtils


def main():
    complete_data = []
    conn, cursor = DbUtils.open_db("Comp490Jobs.sqlite")
    DbUtils.setup_db(cursor)
    for page in range(5):
        current_data = DataProcessing.get_data(page)
        clean_data = DataProcessing.clean_data_for_db(current_data)
        complete_data.extend(clean_data)
    DbUtils.save_to_db(cursor, complete_data)
    DbUtils.close_db(conn)





def save_output(data_to_write: list[dict]):
    output_file = open("output.txt", "w")
    for job in data_to_write:
        print(job, file=output_file)
    output_file.close()


if __name__ == '__main__':
    main()
