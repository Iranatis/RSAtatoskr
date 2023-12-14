from parameter import get

from os import walk, path
from random import randint, seed


SEED = -1
XOR = -1
PUBLIC = -1

INPUT_PATH = "../INPUT/"
OUTPUT_PATH = "../OUTPUT/"

def get_files():
    result = []
    for root, dirs, files in walk(INPUT_PATH):
        for name in files:
            result.append(path.join(root, name))
    return result

def encrypt_file(file):
    global XOR
    XOR = SEED
    
    output_name = file.replace(INPUT_PATH, OUTPUT_PATH) + "." + get("global", "name")
    
    input_file = open(file, 'rb')
    output_file = open(output_name, 'wb')
    
    size = get("global", "size block in")
    step = get("global", "step")
    
    actual_step = 0
    while(chunk := input_file.read(size)):
        #print(chunk)
        if actual_step == 0:
            chunk = encrypt_bytes(chunk)
        else:
            chunk = b'\x00' * (get("global", "size block out") - get("global", "size block in")) + chunk
        output_file.write(chunk)
        #print(chunk)
        actual_step += 1
        actual_step %= step
        #input()
    
    input_file.close()
    output_file.close()
    
def encrypt_bytes(b):
    global XOR
    
    if len(b) < get("global", "size block in"):
        return b
    
    integer = int.from_bytes(b)
    integer ^= XOR
    XOR += 1
    XOR %= get("enc", "n")
    
    integer = pow(integer, PUBLIC, get("enc", "n"))
    
    return integer.to_bytes(get("global", "size block out"))

def set_seed():
    global SEED
    SEED = randint(0, (1 << 64) -1)
    seed(SEED)
    
def write_info():
    with open(OUTPUT_PATH + "info.txt", 'w') as f:
        f.write("seed : " + str(SEED) + "\n")
        f.write("public key : " + str(PUBLIC) + "\n")
        f.write("n : " + str(get("enc", "n")) + "\n")
        f.close()

#Rabin-Miller, pas sûr à 100%
def is_prime(n, k=100):
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
        
def set_public():
    global PUBLIC
    
    PUBLIC = generate_random_prime(3, get("enc", "n"))

def main():
    set_seed()
    set_public()
    print("set ready")
    
    for file in get_files():
        print("encrypt " + file)
        encrypt_file(file)
    
    write_info()
    print("finish")
    
if __name__ == "__main__":
    main()