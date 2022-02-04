with open("wordlist.txt") as file:
    WORDS = file.read().splitlines()

class State:
    __slots__ = ("word", "yellow", "gray", "possible")
    def __init__(self, words):
        self.word = [None] * 5
        self.yellow = set()
        self.gray = set()
        self.possible = words.copy()

    def update(self, response):
        for i, (c, v) in enumerate(response):
            match v:
                case 0: self.gray.add(c)
                case 1: self.yellow.add(c)
                case 2: self.word[i] = c
    
    def is_done(self):
        return all(self.word)

    def check_word(self, word: str):
        for c in self.yellow:
            if c not in word:
                return False

        for c in word:
            if c in self.gray:
                return False

        for i in range(len(word)):
            if self.word[i] is not None and self.word[i] != word[i]:
                return False

        return True

    def best_guess(self):
        self.possible = [w for w in self.possible if self.check_word(w)]
        return max(self.possible, key=num_unique_letters, default=None)
        

def num_unique_letters(word: str):
    return len(set(word))

def submit_guess(guess: str):
    return list(zip(guess, map(int, input(f"Write response to guess [{guess}]:").strip())))

def eval_guess(guess: str, known: str):
    out = []
    for g, k in zip(guess, known):
        out.append((g, 2 if (g == k) else (1 if g in known else 0)))
    return out

def solve(known_answer=None, words=WORDS):
    state = State(words)
    for _round in range(6):
        if (guess := state.best_guess()) is None:
            return
        response = eval_guess(guess, known_answer) if known_answer else submit_guess(guess)
        state.update(response)

        if known_answer:
            # print(f" {guess=:} {list(zip(*response))[1]}")
            yield (guess, list(zip(*response))[1])
        
        if state.is_done():
            break
    else:
        return

    yield "".join(state.word)

if __name__ == "__main__":
    if ans := solve("shard"):
        print("Answer:", ans)
    else:
        print("Failed to guess word :/")
