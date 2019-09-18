import csv


def get_data_header(data_file_path):
    with open(data_file_path, newline='') as csv_file:
        return csv_file.readline().rstrip('\r\n').split(',')


def get_all_user_story(data_file_path):
    file_content = {}
    table_head = get_data_header(data_file_path)
    with open(data_file_path, newline='') as csv_file:
        for item in csv.DictReader(csv_file):
            file_content[item[table_head[0]]] = item
    return file_content


def write_new_story(story_dict, data_file_path, write_method='a'):
    with open(data_file_path, write_method) as csv_file:
        csv.DictWriter(csv_file, fieldnames=get_data_header(data_file_path)).writerow(story_dict)


def write_all_story(story_dict, table_head, data_file_path, write_method='w'):
    with open(data_file_path, write_method) as csv_file:
        csv.writer(csv_file).writerow(table_head)
        for story in story_dict.values():
            csv.DictWriter(csv_file, fieldnames=table_head).writerow(story)


