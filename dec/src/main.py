from parameter import get

from os import walk, path
from random import randint, seed


SEED = -1
XOR = -1
PUBLIC = -1
PRIVATE = -1

INPUT_PATH = "../INPUT/"
OUTPUT_PATH = "../OUTPUT/"

def get_files():
    result = []
    for root, dirs, files in walk(INPUT_PATH):
        for name in files:
            result.append(path.join(root, name))
    return result

def decrypt_file(file):
    global XOR
    XOR = SEED
    
    output_name = file.replace(INPUT_PATH, OUTPUT_PATH)
    output_name = output_name.replace("." + get("global", "name"), "")
    
    input_file = open(file, 'rb')
    output_file = open(output_name, 'wb')
    
    size = get("global", "size block in")
    step = get("global", "step")
    
    actual_step = 0
    while(chunk := input_file.read(size)):
        #print(chunk)
        if actual_step == 0:
            chunk = decrypt_bytes(chunk)
        else:
            chunk = chunk[get("global", "size block in") - get("global", "size block out"):]
        output_file.write(chunk)
        #print(chunk)
        actual_step += 1
        actual_step %= step
        #input()
    
    input_file.close()
    output_file.close()
    
def decrypt_bytes(b):
    global XOR
    
    if len(b) < get("global", "size block in"):
        return b
    
    integer = int.from_bytes(b)
    
    integer = pow(integer, PRIVATE, get("dec", "a") * get("dec", "b"))
    
    integer ^= XOR
    XOR += 1
    XOR %= get("dec", "a") * get("dec", "b")
    
    return integer.to_bytes(get("global", "size block out"))

def set_seed():
    global SEED
    SEED = int(input("Donner seed (et 5k€ en BTC :)) : "))
    seed(SEED)
    
def write_info():
    with open(OUTPUT_PATH + "info.txt", 'w') as f:
        f.write("seed : " + str(SEED) + "\n")
        f.write("public key : " + str(PUBLIC) + "\n")
        f.write("private key : " + str(PRIVATE) + "\n")
        f.write("a : " + str(get("dec", "a")) + "\n")
        f.write("b : " + str(get("dec", "b")) + "\n")
        f.close()
    
def inverse_mod(a, n):
    #Je suppose a et n premier entre eux

    r1, r2 = n, a
    x1, x2 = 0, 1

    while r2:
        q = r1 // r2
        r1, r2 = r2, r1 - q * r2
        x1, x2 = x2, x1 - q * x2

    # Pour avoir x1 >= 0
    x1 = x1 % n

    return x1


# Rabin-Miller, pas sûr à 100%
# k = 25, recommendation GMP
# https://fr.wikipedia.org/wiki/Test_de_primalit%C3%A9_de_Miller-Rabin
def is_prime(n, k=25):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Écriture de n comme 2^r * d + 1 avec d impair
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Test de primalité Rabin-Miller
    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_random_prime(minimum, maximum):
    while True:
        n = randint(minimum, maximum)
        if n % 2 == 0:
            n += 1
        if is_prime(n):
            return n
        
def set_private():
    global PRIVATE, PUBLIC
    
    PUBLIC = generate_random_prime(3, get("dec", "a") * get("dec", "b"))
    
    PRIVATE = inverse_mod(PUBLIC, (get("dec", "a") - 1) * (get("dec", "b") - 1))

def main():
    set_seed()
    set_private()
    print("set ready")
    
    for file in get_files():
        print("decrypt " + file)
        decrypt_file(file)
    
    #write_info()
    print("finish")
    
if __name__ == "__main__":
    main()