import inspect
import os
import shutil
import sys
import urllib
from pathlib import Path
from typing import List, Callable
import subprocess

import pandas as pd

from johnsnowlabs import settings
from johnsnowlabs.py_models.url_dependency import UrlDependency


def get_py_snippet_from_modelhub(url):
    import requests
    from bs4 import BeautifulSoup
    # get_py_snippet_from_modelhub('https://nlp.johnsnowlabs.com/2022/09/06/finclf_augmented_esg_en.html')
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    python_code = soup.find_all("div", {"class": "language-python"})[0]
    return python_code.getText()


def str_to_file(str_, path):
    with open(path, "w") as text_file: text_file.write(str_)


def file_to_str(path):
    with open(path, 'r') as file:
        return file.read()


def run_cmd_and_check_succ(args: List[str], log=True, suc_print=settings.success_worker_print,
                           return_pipes=False) -> bool:
    r = subprocess.run(args, capture_output=True)
    if log:
        log_process(r)
    if return_pipes:
        return process_was_suc(r), r
    return process_was_suc(r)


def process_was_suc(result: subprocess.CompletedProcess, suc_print=settings.success_worker_print) -> bool:
    return suc_print in result.stdout.decode()


def log_process(result: subprocess.CompletedProcess):
    print("______________STDOUT:")
    print(result.stdout.decode())
    print("______________STDERR:")
    print(result.stderr.decode())


# def execute_slave_test(py_cmd):
#     prefix = 'from johnsnowlabs import * \n'
#     postfix = f"\neval_class('{py_cmd}') \n"
#     script_file_name = 'test_script.py'
#     script = inspect.getsource(eval_class)
#     script = f'{prefix}{script}{postfix}'
#     print(script)
#     str_to_file(script, script_file_name)
#     return run_cmd_and_check_succ(['python', script_file_name])
#

def execute_function_as_new_proc(function: Callable, suc_print=settings.success_worker_print):
    pass


def execute_py_script_string_as_new_proc(py_script,
                                         suc_print=settings.success_worker_print,
                                         py_exec_path=sys.executable,
                                         log=True,
                                         file_name=None,  # Optional metadata

                                         ):
    prefix = """
from johnsnowlabs import *
spark = jsl.start()
"""

    suffix = f"""
print('{suc_print}')    
    
"""

    str_to_file(prefix + py_script + suffix, 'tmp.py')
    suc, proc = execute_py_script_as_new_proc('tmp.py')
    return make_modelhub_snippet_log(file_name, suc, proc)


def execute_py_script_as_new_proc(py_script_path: str,
                                  suc_print=settings.success_worker_print,
                                  py_exec_path=sys.executable,
                                  log=True):
    # requires ipython installed
    cmd_args = [py_exec_path, py_script_path]  # '-m', 'IPython',
    return run_cmd_and_check_succ(cmd_args, log=log, suc_print=suc_print, return_pipes=True)


def clean_workshop_notebook(py_script_path, out_path, suc_print=settings.success_worker_print, work_dir=os.getcwd()):
    prefix = f"""
import os 
os.chdir('{work_dir}')
from johnsnowlabs import *
jsl.start()
"""

    suffix = f"""
print('{suc_print}')    
"""

    # Substring matches
    bad_sub_strings = [
        'files.upload()',
        # 'get_ipython',
        'pip install',
        'from google',
        'google.',
        'colab',
        'jsl.install',
        '#',
        'license_keys',

    ]

    # Hard matches
    bad_lines = [  # '\n',
        'jsl.install()',
    ]
    new_file = []
    with open(py_script_path, "r") as f:
        for l in f:
            if any(s in l for s in bad_sub_strings): continue
            if l in bad_lines: continue
            if 'get_ipython().system' in l:
                l = l.replace('get_ipython()', 'os')
            if 'get_ipython().run_line_magic' in l:
                continue

            new_file.append(l)
    new_file = prefix + ''.join(new_file) + suffix
    # print(new_file)
    str_to_file(new_file, out_path)


def modelhub_md_to_pyscript(path):
    start_s = '```python'
    end_s = '```'
    data = []
    started = False
    with open(path, 'r') as f:
        for l in f:
            if start_s in l:
                started = True
                continue
            if end_s in l:
                return data
            if started:
                data.append(l)
    return ['False']


import nbformat
from nbconvert import PythonExporter


def get_all_nb_in_local_folder(p):
    ## filter all files ending in .ipynb
    return [f'{p}/{f}' for f in os.listdir(p) if '.ipynb' in f]


def str_to_file(str_, path):
    with open(path, "w") as text_file: text_file.write(str_)


def convert_notebook(notebookPath, out_py_path):
    with open(notebookPath) as fh:
        nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
    exporter = PythonExporter()
    source, meta = exporter.from_notebook_node(nb)
    str_to_file(source, out_py_path)


def convert_all_notebooks(nb_folder):
    # Convert a folder which contains .ipynb into .py
    store_folder = f'{nb_folder}/nb_converted/'
    Path(store_folder).mkdir(parents=True, exist_ok=True)
    for nb_path in get_all_nb_in_local_folder(nb_folder):
        save_path = store_folder + nb_path.split('/')[-1] + '.py'
        convert_notebook(nb_path, save_path)


def test_ipynb(file_path_or_url, work_dir=os.getcwd()):
    if 'http' and '//' in file_path_or_url:
        file_name = file_path_or_url.split('/')[-1]

        print(f'Downloading {file_path_or_url} to  {file_name}')
        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(file_path_or_url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            file_path_or_url = file_name

    file_name = work_dir + '/' + file_path_or_url.split('/')[-1]
    convert_notebook(file_path_or_url, file_name)
    final_py_script = file_name + '___CLEANED.py'
    clean_workshop_notebook(py_script_path=file_name, out_path=final_py_script, work_dir=work_dir)

    succ, proc = execute_py_script_as_new_proc(py_script_path=final_py_script)
    return make_log(file_path_or_url, succ, proc, final_py_script)


def test_ipynb_folder(nb_folder, work_dir=os.getcwd(), log=True):
    return pd.DataFrame(test_list_of_ipynb(get_all_nb_in_local_folder(nb_folder), work_dir, log))


def test_list_of_ipynb(nb_paths_or_urls, work_dir=os.getcwd(), log=True):
    df = pd.DataFrame(test_ipynb(nb_path, work_dir) for nb_path in nb_paths_or_urls)
    if log:
        log_multi_run_status(df)
    return df


def log_multi_run_status(run_df):
    print(f'#' * 10 + "RUN RESULTS" + "#" * 10)
    for idx, row in run_df[run_df.success == False].iterrows():
        print(f'Result for Notebook  {row.notebook} {"#" * 25}')
        print(row.stdout)


def make_modelhub_snippet_log(md_file, suc, proc):
    return {
        'md_file': md_file,
        'success': suc,
        'stdout': proc.stdout.decode(),
        'stderr': proc.stderr.decode(), }


def make_log(nb_file, suc, proc, final_py_script):
    return {
        'notebook': nb_file,
        'success': suc,
        'stdout': proc.stdout.decode(),
        'stderr': proc.stderr.decode(),
        'test_script': final_py_script}


########### MODELHUB
def get_all_py_scripts_in_md_folder(markdown_folder):
    scripts = {}
    for p in os.listdir(markdown_folder):
        # print("TESTING", p)
        script = ''.join(modelhub_md_to_pyscript(f'{markdown_folder}/{p}'))
        if script == 'False':
            print("Badly Formatted Markdown File!", p)
            continue
        scripts[p] = script
    return scripts


def run_modelhub_md_script(md_path_or_url):
    if 'http' and '//' in md_path_or_url:
        md_path_or_url = get_py_snippet_from_modelhub(md_path_or_url)
    return execute_py_script_string_as_new_proc(modelhub_md_to_pyscript(md_path_or_url), file_name=md_path_or_url)


def test_folder_of_modelhub_md_files(markdown_folder):
    results = []
    scripts = get_all_py_scripts_in_md_folder(markdown_folder)
    for file, script in scripts.items():
        print('#' * 10 + f'Testing {file}' + '#' * 10)
        results.append(execute_py_script_string_as_new_proc(script, file_name=file))
    return pd.DataFrame(results)
