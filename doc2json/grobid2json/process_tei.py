import os
import json
import argparse
import time
from typing import Optional

from doc2json.grobid2json.tei_to_json import convert_tei_xml_file_to_s2orc_json

BASE_TEMP_DIR = 'temp'
BASE_OUTPUT_DIR = 'output'
BASE_LOG_DIR = 'log'

def process_tei_file(
        tei_file: str,
        output_dir: str=BASE_OUTPUT_DIR,
        log_dir: str=BASE_LOG_DIR,
) -> Optional[str]:
    """
    Process files in a TEI XML file and get JSON representation
    :param tei_file:
    :param output_dir:
    :param log_dir:
    :return:
    """
    # create directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    # get paper id as the name of the file
    paper_id = os.path.splitext(tei_file)[0].split('/')[-1]
    output_file = os.path.join(output_dir, f'{paper_id}.json')

    # check if input file exists and output file doesn't
    if not os.path.exists(tei_file):
        raise FileNotFoundError(f"{tei_file} doesn't exist")
    if os.path.exists(output_file):
        print(f'{output_file} already exists!')

    # convert to S2ORC
    paper = convert_tei_xml_file_to_s2orc_json(tei_file)
    #with open(tei_file, 'r') as inf:
    #paper = convert_jats_xml_to_s2orc_json(jats_file, log_dir)

    # write to file
    with open(output_file, 'w') as outf:
        json.dump(paper.release_json("jats"), outf, indent=4, sort_keys=False)

    return output_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run S2ORC TEI2JSON")
    parser.add_argument("-i", "--input", default=None, help="path to the input TEI XML file")
    parser.add_argument("-o", "--output", default='output', help="path to the output dir for putting json files")
    parser.add_argument("-l", "--log", default='log', help="path to the log dir")

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    log_path = args.log

    start_time = time.time()

    os.makedirs(output_path, exist_ok=True)

    process_tei_file(input_path, output_path, log_path)

    runtime = round(time.time() - start_time, 3)
    print("runtime: %s seconds " % (runtime))
    print('done.')