import time
from csv import writer

class BenchmarkInfo:
    def __init__(self):
        self.instance = ""
        self.input_translation = ""
        self.horizon = ""
        self.node_expansions = ""
        self.solving_successfull = ""
        self.total_processing = ""
        self.total_real_world = ""

    def row(self):
        return [self.instance, self.input_translation, self.node_expansions, self.horizon, self.solving_successfull, self.total_processing, self.total_real_world]

    def end_benchmark(self, p_start, start, file):
        performance_end_time = time.perf_counter_ns()
        end_time = time.process_time_ns()

        self.total_real_world = performance_end_time - p_start
        self.total_processing = end_time - start

        if(file != ""):
            with open(file, 'a') as f:
                writer_object = writer(f)
            
                writer_object.writerow(self.row())
            
                f.close()