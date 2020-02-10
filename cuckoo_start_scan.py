import time
import sys
import cuckoo_worker
import ntpath
import myparser

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def CuckooSandbox(path , ip , port):
    filename = path_leaf(path)
    c_worker = cuckoo_worker.CuckooWorker(ip, port, 'eC7elTsNrvd2WmHSSAQTbQ')
    task_id = c_worker.analyze_file(path, filename)
    task_info = c_worker.view_task_result(task_id)
    while task_info['task']['status'] != 'reported':
        time.sleep(5)
        task_info = c_worker.view_task_result(task_id)
    result = c_worker.get_task_report(task_id)
    # Get API calls
    processes = result['behavior']['processes']
    score = result['info']['score']
    return processes , score

def main () :
    if len(sys.argv) < 4 :
        # print("[ - ] Error then start program: main.py <filename> <ip> <port>")
        # Send in pipe
        print('Error')
        sys.stdout.flush()
        return
    processes , score = CuckooSandbox(sys.argv[1], sys.argv[2], sys.argv[3])
    result = myparser.StartParsing(processes , score)
        
    

if __name__ == "__main__" :
    main()