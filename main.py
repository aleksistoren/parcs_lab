from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.workers = workers
        if workers is not None:
            self.workers_cnt = len(workers)
        else:
            self.workers_cnt = 0
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.arr = []


    def solve(self):
        # print("Job started")
        # print(f"Starting with {self.workers_cnt} workers")
        self.read_input()
        n = len(self.arr)

        chunks = [[] for _ in range(self.workers_cnt)]
        for i in range(n):
            chunks[i % self.workers_cnt].append(i)

        mapped = []
        for i in range(self.workers_cnt):
            mapped.append(self.workers[i].worker_solve(chunks[i], self.arr))
        reduced = self.reduce(mapped)

        self.write_output(reduced)


    def read_input(self):
        self.arr = [i for i in range(10000)]
        return
        f = open(self.input_file_name, "r")
        self.arr = list(map(int, f.readline().split()))
        f.close()


    def write_output(self, answer):
        f = open(self.output_file_name, "w")
        f.write(str(int(answer)))
        f.close()

    @staticmethod
    @expose
    def worker_solve(checkers, arr):
        result = 0
        for i in range(len(checkers)):
            for j in range(len(arr)):
                if arr[j] == checkers[i]:
                    result += 1
                    break
        return [result]

    @staticmethod
    @expose
    def reduce(mapped):
        res = []
        for item in mapped:
            res.extend(item.value)
        return sum(res)

if __name__ == '__main__':
    master = Solver(workers=[Solver(), Solver()], input_file_name="input1000000.txt", output_file_name="output.txt")
    master.solve()
