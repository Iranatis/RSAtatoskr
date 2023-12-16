from random import randint

#Le delta semble donner un temps d'exécution trop long
DELTA = 0

# Va écrire les informations généré dans un fichier
def write_info(borne_inf, borne_sup, a, b, n, file = "abn.txt"):
    with open(file, 'w') as f:
        f.write("borne inférieur : " + str(borne_inf) + "\n")
        f.write("borne supérieur : " + str(borne_sup) + "\n")
        f.write("a : " + str(a) + "\n")
        f.write("b : " + str(b) + "\n")
        f.write("n : " + str(n) + "\n")
        f.close()

# Détermine de manière probabiliste si un nombre n est premier avec k tests
# selon le test de primalité de Rabin-Miller, pas sûr à 100%
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

# Va générer un nombre premier aléatoire en les bornes données
def generate_random_prime(minimum, maximum):
    while True:
        n = randint(minimum, maximum)
        if n % 2 == 0:
            n += 1
        if is_prime(n):
            return n

# Va générer le triplet (a, b, n) utilisé dans les fichiers de config de dec/ et enc/
def generate_a_b_n(inf, sup):
    borne_inf = pow(256, inf)
    borne_sup = pow(256, sup)
    
    limit_inf = pow(256, inf//2 - DELTA)
    limit_sup = pow(256, sup//2 + DELTA)
    
    a, b, n = 0, 0, 0
    
    while borne_inf > n or borne_sup < n:
        a = generate_random_prime(limit_inf, limit_sup)
        b = generate_random_prime(limit_inf, limit_sup)
        n = a*b
        
    return a, b, n
    
def main():
    inf = int(input("Donnez la taille minimal en octects : "))
    sup = int(input("Donnez la taille maximal en octects : "))
    
    if inf == sup:
        exit("Les bornes doivent être de taille différentes")
        return
        
    if inf > sup:
        inf, sup = sup, inf
        
    a, b, n = generate_a_b_n(inf, sup)
    
    print("a :", a)
    print("b :", b)
    print("n :", n)
    
    write_info(inf, sup, a, b, n)


if __name__ == "__main__":
    main()