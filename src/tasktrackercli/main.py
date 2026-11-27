import os
import json
import io
import argparse
from operator import itemgetter


def json_file_exists(json_file_path: str):
    if os.path.exists(json_file_path):
        return True

    return False


def create_json_file():
    json_filename = 'tasks.json'
    path_to_project_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(path_to_project_dir, json_filename)

    if json_file_exists(json_file_path=json_file_path):
        print('File already exists')
    else:
        print('Creating file')
        json_file_path = os.path.join(path_to_project_dir, json_filename)
        with io.open(json_file_path, 'w') as f:
            f.write(json.dumps([]))


def verify_id_task_exists(id_task: int):
    with io.open('tasks.json', 'r') as json_file:
        json_data = json.load(json_file)
        if json_data:
            for data in json_data:
                if data['id'] == id_task:
                    print('Task already exists')
                    return True

            print('Task does not exist')
        else:
            print('No tasks found')

    return False


def get_next_id_task():
    next_id_task = 1
    with io.open('tasks.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        if json_data:
            max_id = max(json_data, key=itemgetter('id'))['id']
            next_id_task = max_id + 1

        return next_id_task


def add_task(description_task: str):
    from datetime import datetime

    # verify_id_task_exists(1)
    task_id = get_next_id_task()

    with io.open('tasks.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)


    with io.open('tasks.json', 'w', encoding='utf-8') as json_file:
        date_now = str(datetime.now())
        new_task = [
            {
                'id': task_id,
                'description': description_task,
                'status': 'todo',
                'createdAt': date_now,
                'modifiedAt': date_now
            }
        ]

        json_data.extend(new_task)

        json.dump(json_data, json_file, indent=4, ensure_ascii=False)


def update_task(id_task: int, description_task: str):
    if verify_id_task_exists(id_task=id_task):
        from datetime import datetime

        with io.open('tasks.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                if data['id'] == id_task:
                    data['description'] = description_task
                    data['modifiedAt'] = str(datetime.now())
                    break

        with io.open('tasks.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
            return True

    return False


def delete_task(id_task: int):
    if verify_id_task_exists(id_task=id_task):
        with io.open('tasks.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        with io.open('tasks.json', 'w', encoding='utf-8') as json_file:
            for i in range(0, len(json_data)):
                if json_data[i]['id'] == id_task:
                    json_data.pop(i)
                    print('Task deleted')
                    break

            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
            return True

    return False


def mark_done_task(id_task: int):
    if verify_id_task_exists(id_task=id_task):
        from datetime import datetime

        with io.open('tasks.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                if data['id'] == id_task:
                    data['status'] = 'done'
                    data['modifiedAt'] = str(datetime.now())
                    break

        with io.open('tasks.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
            return True

    return False


def mark_in_progress_task(id_task: int):
    if verify_id_task_exists(id_task=id_task):
        from datetime import datetime

        with io.open('tasks.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                if data['id'] == id_task:
                    data['status'] = 'in-progress'
                    data['modifiedAt'] = str(datetime.now())
                    break

        with io.open('tasks.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
            return True

    return False


def list_tasks(list_task: str):
    with io.open('tasks.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        tasks_by_type = list_tasks_by_type(json_data, list_task)
        print(tasks_by_type)


def list_tasks_by_type(json_data, list_task: str):
    list_task_items = []

    for data in json_data:
        if data['status'] == list_task:
            list_task_items.append(data)
        elif list_task == 'all':
            list_task_items.append(data)

    json_data_formatted_str = json.dumps(list_task_items, indent=4, ensure_ascii=False)

    return json_data_formatted_str


TYPE_TASKS = {
    "add": add_task,
    "update": update_task,
    "delete": delete_task,
    "mark-in-progress": mark_in_progress_task,
    "mark-done": mark_done_task,
    "list": list_tasks
}


def main():
    parser = argparse.ArgumentParser(prog='TaskTrackerCLI', description='Task Tracker')
    parser.add_argument(
        'task-cli',
        default='task-cli',
        choices=['task-cli'],
        help='type "task-cli" to start script'
    )
    subparsers = parser.add_subparsers(dest='subcommand-type')

    parser_add_task = subparsers.add_parser('add', help='')
    parser_add_task.add_argument('description-task', type=str, help='')

    parser_update_task = subparsers.add_parser('update', help='')
    parser_update_task.add_argument('id-task', type=int, help='')
    parser_update_task.add_argument('update-description-task', type=str, help='')

    parser_delete_task = subparsers.add_parser('delete', help='')
    parser_delete_task.add_argument('id-task', type=int, help='')

    parser_mark_in_progress_tasks = subparsers.add_parser('mark-in-progress', help='')
    parser_mark_in_progress_tasks.add_argument('id-task', type=int, help='')

    parser_mark_done_tasks = subparsers.add_parser('mark-done', help='')
    parser_mark_done_tasks.add_argument('id-task', type=int, help='')

    parser_list_tasks = subparsers.add_parser('list', help='')
    parser_list_tasks.add_argument('list-task', default='all', nargs='?', type=str, choices=['all', 'todo', 'in-progress', 'done'],
                                   help='')

    args = parser.parse_args().__dict__
    print(args)

    return args


def args_handler(args):
    if args['subcommand-type'] in TYPE_TASKS:
        if args['subcommand-type'] == 'add':
            TYPE_TASKS[args['subcommand-type']](args['description-task'])
        elif args['subcommand-type'] == 'update':
            TYPE_TASKS[args['subcommand-type']](args['id-task'], args['update-description-task'])
        elif args['subcommand-type'] == 'delete':
            TYPE_TASKS[args['subcommand-type']](args['id-task'])
        elif args['subcommand-type'] == 'mark-in-progress':
            TYPE_TASKS[args['subcommand-type']](args['id-task'])
        elif args['subcommand-type'] == 'mark-done':
            TYPE_TASKS[args['subcommand-type']](args['id-task'])
        elif args['subcommand-type'] == 'list':
            TYPE_TASKS[args['subcommand-type']](args['list-task'])


if __name__ == '__main__':
    create_json_file()
    args = main()
    args_handler(args)
