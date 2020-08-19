# coding=utf8

import codecs

def delete_data(input_file, output_file):
    with codecs.open(output_file, 'w') as f:
        with codecs.open(input_file, 'r') as f:
            start_flag = False
            for line in f.readlines():
                line = line.strip()
                if not line.startswith('BEGIN') and not line.startswith('END') and not start_flag:
                    f.write(line+'\n')
                    continue
                if line.startswith('BEGIN') and not start_flag:
                    start_flag = True
                elif line.startswith('END') and start_flag:
                    start_flag = False
                else:
                    raise Exception('not match')
