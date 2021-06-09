import os
import csv
import json
import zipfile
import tempfile
from time import time


def create_tmp_file(data):
    filename = tempfile.NamedTemporaryFile(delete=False).name
    with open(filename, "wb") as f:
        f.write(data)
    return filename


def write_csv_file(data, delimiter="\t"):
    """
        Method write array data to the file and return the file name
    :param data: (list)- Array of array data i.e is supposed to be written to the file.
    :param delimiter:
    :return:
    """
    filename = tempfile.NamedTemporaryFile(delete=False).name
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=delimiter)
        csvwriter.writerows(data)
    return filename


def read_csv_file(data_file, delimiter=","):
    with open(data_file, 'r') as text:
        csv_reader = csv.reader(text, delimiter=delimiter)
        for row in csv_reader:
            yield row


def read_csv_stream(stream, delimiter="\t"):
    csv_reader = csv.reader(iter(stream), delimiter=delimiter)
    for row in csv_reader:
        yield row


def compress_file_to_zip(zip_file_name, local_file_path, arcname):
    """
        Function to compress a file to a zip file.
    :param zip_file_name: (string) - Zipped file name
    :param local_file_path: (string) - File's path on the system.
    :param arcname: (string)  File name without the directory names
    :return: None
    """

    dir_name = os.path.dirname(zip_file_name)
    # check if the directory is not there
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    print("### In zipping file from {}  to {}",local_file_path, zip_file_name)
    with zipfile.ZipFile(
        zip_file_name, 'w', zipfile.ZIP_DEFLATED
    ) as zipped_items:
        zipped_items.write(local_file_path, arcname=arcname)


def write_to_file(data, file_path, mode="w", is_json=True):
    """
        Function to write json data fil
    :param data:
    :param file_path: (string) - absolute file path
    :return:
    """
    dir_name = os.path.dirname(file_path)
    # check if the directory is not there
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    print("File path in os == > ", file_path)
    try:
        with open(file_path, mode) as outfile:
            if is_json:
                json.dump(data, outfile)
            else:
                outfile.write(data)
    except Exception as e:
        raise Exception("Exception {}".format(str(e)))


def write_feed_file(self, file_dir, products):
    current_time = round(time())
    file_name = '{app_name}_to_PIM_feed_{timestamp}.json'.format(
        timestamp=current_time, app_name = self.app_name
    )
    zip_file_name = '{app_name}_to_PIM_feed_{timestamp}.zip'.format(
        timestamp=current_time, app_name = self.app_name
    )
    file_path = os.path.join(file_dir, file_name)
    with open(file_path, 'w') as f:
        f.write(json.dumps(products))
    zip_file_path = os.path.join(file_dir, zip_file_name)
    compress_file_to_zip(zip_file_path, file_path, file_name)
    return zip_file_name
