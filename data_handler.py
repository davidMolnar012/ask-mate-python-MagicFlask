import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data.csv'
DATA_HEADER = ['id', 'title', 'user_story', 'acceptance_criteria', 'business_value', 'estimation', 'status']
STATUSES = ['planning', 'todo', 'in progress', 'review', 'done']


def get_all_user_story():
    file_content = {}
    with open(DATA_FILE_PATH, newline='') as csv_file:
        for item in csv.DictReader(csv_file):
            file_content[item[DATA_HEADER[0]]] = item
        csv_file.close()
    return file_content, DATA_HEADER


def write_new_story(story_dict, write_method='a'):
    with open(DATA_FILE_PATH, write_method) as csv_file:
        csv.DictWriter(csv_file, fieldnames=DATA_HEADER).writerow(story_dict)
        csv_file.close()


def write_whole_story(story_dict, write_method='w'):
    with open(DATA_FILE_PATH, write_method) as csv_file:
        print(story_dict)
        csv.writer(csv_file).writerow(DATA_HEADER)
        for story in story_dict.values():
            csv.DictWriter(csv_file, fieldnames=DATA_HEADER).writerow(story)
        csv_file.close()