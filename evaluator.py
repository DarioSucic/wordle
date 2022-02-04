from solver import solve, WORDS
from tqdm import tqdm

from time import perf_counter_ns as pc

def evaluate(words):
    avg = 0
    dts = []
    for w in tqdm(words):
        st = pc()
        steps = tuple(solve(w))
        et = pc()
        dts.append(et-st)
        if isinstance(steps[-1], str):
            n = len(steps) - 1
            avg += n
        else:
            pass
            #raise Exception("Failed word: " + w)
    avg /= len(words)
    return avg, dts

if __name__ == "__main__":
    avg, dts = evaluate(WORDS)
    print("avg:", avg)
    
    vmean, vmin, vmax = int(sum(dts)/len(dts)), min(dts), max(dts)
    vtotal = sum(dts)
    print("Runtime:")
    print(f"\t{vtotal = :>12,} ns")
    print(f"\t{vmin   = :>12,} ns")
    print(f"\t{vmax   = :>12,} ns")
    print(f"\t{vmean  = :>12,} ns")
