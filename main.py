import _csv
import csv
import os
import json
import shutil

dir_of_csvfile: str = './csvfile_from_eudic/'
dir_of_jsonfile: str = './jsonfile/'
dir_of_qwerty_dicts: str = '../public/dicts/'
qwerty_dicts_configuration_file: str = '../src/resources/dictionary.ts'
write_line_of_qwerty_dicts_configuration_file: int = 18  # 从 0 开始计行数
keep_countdown_line_of_qwerty_dicts_configuration_file: int = 6
configuration_template: str = ''
#     name: '',
#     description: '',
#     category: '',
#     url: '',
#     length: ,
#     language: '',
#   },
# "
newest_csv_filename: str = ''
csv_list: list[dict] = []
name_row_in_csv: int = 1  # 从第 0 列开始算
trans_row_in_csv: int = 3


def get_csv_filenames(dir: str):
    return os.listdir(dir)


def get_newest_csv_filename(filenames: list[str]):
    return filenames.pop()


def write_to_csv_list(filename: str):
    with open(dir_of_csvfile + filename) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            # csv_list.append({row[name_row_in_csv]: [row[trans_row_in_csv]]})
            csv_list.append({
                "name": row[name_row_in_csv],
                "trans": [row[trans_row_in_csv]],
            })

    csv_list.pop(0)


def save_csv_list_as_json(json_filename: str):
    json_str: str = json.dumps(csv_list, ensure_ascii=False)
    with open(dir_of_jsonfile + json_filename, 'w') as f:
        f.write(json_str)


def config_json_to_qwerty():
    shutil.copyfile(
        dir_of_jsonfile + newest_csv_filename.replace('csv', 'json'),
        dir_of_qwerty_dicts + newest_csv_filename.replace('csv', 'json')
    )
    lines: list[str] = []
    with open(qwerty_dicts_configuration_file, 'r') as f:
        for line in f:
            lines.append(line)
    for _ in range(write_line_of_qwerty_dicts_configuration_file,
                   len(lines) - keep_countdown_line_of_qwerty_dicts_configuration_file):
        lines.pop(write_line_of_qwerty_dicts_configuration_file)

    configuration_template = f"  {{\n    id: '{str('eudic')}',\n     name: '{str('Eudic')}',\n     description: '{newest_csv_filename.replace('.csv', '')}',\n     category: '',\n     url: './dicts/{newest_csv_filename.replace('csv', 'json')}',\n     length: {len(csv_list)},\n     language: 'en',\n   }},\n"

    lines.insert(write_line_of_qwerty_dicts_configuration_file, configuration_template)
    with open(qwerty_dicts_configuration_file, 'w') as f:
        f.write(''.join(lines))


filenames: list[str] = get_csv_filenames('./csvfile_from_eudic/')
newest_csv_filename = get_newest_csv_filename(filenames)
write_to_csv_list(newest_csv_filename)
save_csv_list_as_json(newest_csv_filename.replace('csv', 'json'))

config_json_to_qwerty()

os.system('cd ..')
os.system('yarn install')
os.system('yarn start --host 10086')

if __name__ == '__main__':
    filenames: list[str] = get_csv_filenames('./csvfile_from_eudic/')
    newest_csv_filename = get_newest_csv_filename(filenames)
    write_to_csv_list(newest_csv_filename)
    save_csv_list_as_json(newest_csv_filename.replace('csv', 'json'))
    # for line in csv_reader:
    #     print(line)
    config_json_to_qwerty()

    print(csv_list)
