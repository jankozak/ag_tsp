# -*- coding: utf-8 -*-
"""noc_innowacji_AG_TSP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11G34W8uy9GPOBNQP633OatEGV5DB_XVO

# 🌃 **Noc Innowacji UE Katowice 2022** 
# Algorytm genetyczny do problemu TSP
🌜 22.10.2022

📭 ➡ [*jkozak.pl*](http://www.jkozak.pl/)
---

Problem:
*   Problem TSP:
*   http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html
*   Na wejściu: macierz odległości pomiędzy punktami.

Reprezentacja:
*   Kolejność miast (jedno miasto, to jeden gen), liczone o 0.

Funkcja oceny:
*   Suma odległości pomiędzy miastami

Inicjalizacja:
*   Losowanie n-osobników (populacja wielkości n)

Selekcja:
*   Turniej.

Przeszukiwanie:
*   Krzyżowanie: PMX
*   Mutacja: Inwersja

**Sposób rozwiązania:**
1. Wczytać dane z pliki i przygotować macierz odległości
2. Napisać funkcję losującą osobnika.
3. Napisać funkcję losującą n-osobników, czyli całą populację.
4. Napisać funkcję sumującą odległości pomiedzy miamstami i zastosować ją do całej populacji.
5. Napisać selekcję z parametrem k, gdzie z k losowych osobników przejdzie jeden najlepszy (o najmniejszej sumie)
6. Napisać krzyżowanie.
7. Napisać mutację.

# Dodatkowe funkcje 🛠
"""

import random

def print_individual(ind, fitness):
    print("-".join(map(str,ind)),fitness)

def print_population(pop, fitness): # pop -- populacja
    print("="*10)
    for ind, f in zip(pop,fitness): # zip iteruje po 2 listach na raz z pop zapisuje do ind a z fitness do f
        print_individual(ind,f)
    print("="*10)

"""## Inicjalizacja populacji"""

def new_individual(m): # m, to liczba miast, czyli num_of_cities
    ind = [i for i in range(m)] # osobnik ma wszystkie numety miast
    random.shuffle(ind) # mieszamy kolejność tych numerów
    return ind # zwracamy nowego osobnika

def new_population(n,m): # n, to liczba osobników w populacji (num_of_ind); a m, to liczba miast, czyli num_of_cities
    population = [] # populacja popczątkowa jest pusta
    for _ in range(n): # n razy:
        population.append(new_individual(m)) # dodajemy nowego osobnika
    return population # zwracamy całą zainicjowaną populację

"""# Ocena osobników 🔢"""

def calculate_fitness(ind, distance_matrix): # ind, to osobnik, a distance_matrix, to macierz odległości wczytana z pliku
    sum_distance = 0 # Tutaj sumujemy odległości pomiędzy wszystkimi miastami
    for i in range(len(ind)-1): # przejdziemy po wszystkich indeksach osobnika, poza ostanim
        city_1 = ind[i] # wczytujemy numer pierwszego miasta
        city_2 = ind[i+1] # i drugiego miasta 
        sum_distance += distance_matrix[city_1][city_2] # odległość pomiędzy miastem "i" i "i+1", a następnie dodajemy do sumy
    sum_distance += distance_matrix[ind[0]][ind[-1]]
    return sum_distance

def evaluate_population(pop, distance_matrix): # pop, to cała populacja
    fitness=[] # lista z ocenami
    for ind in pop: # dla każdego osobnika
        fitness.append(calculate_fitness(ind,distance_matrix)) # policz ocenę i dodaj do listy ocen
    return fitness

"""# Operacje genetyczne 🌍

## Selekcja
"""

def selection(pop, fitness, k=None):
    new_population = [] # Tworzymy nową populację -- T, osobników wyselekcjonowanych
    for _ in range(len(pop)): # W nowej populacji będzie tyle samo osobników, co w P, czyli len(pop)
        selected = tournament(pop, fitness, k)
        new_population.append(selected) # dodanie wybranego osobnika
    return new_population # zwracamy populację T

"""### Selekcja tuniejowa"""

def tournament(pop, fitness, k):
    num_of_ind = len(pop) # zapisujemy liczbę osobników (dla wygody)
    min_index = random.randint(0,num_of_ind-1) # Piewszy losowy osobnik jest najlepszy
    for _ in range(k-1): # Losujemy kolejnych osobników (w sumie będzie i k)
        random_index = random.randint(0,num_of_ind-1) # Kolejny losowy osobnik
        if fitness[min_index]>fitness[random_index]: # Jeśli kolejny losowy osobnik jest lepszy, to
            min_index=random_index # zapmiętujemy go, jako najlepszego
    return pop[min_index][:] # zwracamy kopię najlepszego z turnieju

"""## Krzyżowanie"""

def crossover(pop, pc): # pop, to populacja po selekcji, pc, to parametr krzyżowanie (czy w ogóle krzyżować)
    new_population = [] # nowa populacja już po krzyżowaniu osobników
    for i in range(0,len(pop),2): # krok co dwa, bo krzyżujemy parami
        # i -- "pierwszy" rodzic.
        # i+1 -- "drugi" rodzic.
        p1 = pop[i]
        p2 = pop[i+1]

        # Losujemy, czy krzyżować
        if random.random()<pc: # Jeśli wylosowana z zakresu [0,1) jest mniejsza od pc, to krzyżować
            c1,c2 = crossover_PMX(p1,p2) # wywołujemy odpowiednią metodę krzyżowania
            new_population.append(c1) # do nowej poulacji przechodzi potomek "pierwszy"
            new_population.append(c2) # do nowej poulacji przechodzi potomek "pierwszy"
        else: # jeśli większe, to bez krzyżowania przechodzą dalej
            new_population.append(p1[:]) # do nowej poulacji przechodzi kopia rodzica "pierwszego"
            new_population.append(p2[:]) # do nowej poulacji przechodzi kopia rodzica "drugiego"

    return new_population

"""### PMX"""

def pmx_fix(parent, self_mid, mid):
    fix = [] # To będzie zwracana część osobnika
    for gene in parent: # Przechodzimy przez geny rodzica, które mają zostać przpisane
        while gene in self_mid: # Jeśli taki gen istnieje już w środku potomka, to szukamy nowego
            gene = mid[self_mid.index(gene)] # Znajduejmy indeks genu (self_mid.index(gene)) i nowy gen, to odpowiednik w mid drugiego potomka
        fix.append(gene) # Dodajemy gen do nowej części osobnika
    return fix

def crossover_PMX(p1,p2):
    cut1 = random.randint(1,len(p1)-2) # Pierwszy punkt przecięcia, zapewniamy, aby nie był skrajnie po lewej i zostało miejsce na drugi punkt przecięcia
    cut2 = random.randint(cut1+1,len(p1)-1) # aby był odsunięty od cut1 i nie był skrajnie po prawej

    c1 = p1[cut1:cut2] # środek pierwszego rodzica przepisujemy do pierwszego potomka (boki będa dodane później)
    c2 = p2[cut1:cut2] # i to samo dla 2

    prefix1 = pmx_fix(p2[:cut1], c1, c2) # Wywołujemy funkcję, która przepisze początek z p2 i zwróci go w odpowiedniej kolejności do wpisania w c1 (wpiszemy go późnie)
    prefix2 = pmx_fix(p1[:cut1], c2, c1) # analogicznie dla c2

    postfix1 = pmx_fix(p2[cut2:], c1, c2) # To samo, ale dla końca p2 i później wpisania w odpowiedniej kolejności w c1
    postfix2 = pmx_fix(p1[cut2:], c2, c1) # analogicznie dla c2

    c1 = prefix1 + c1 + postfix1 # Łączymy początek, środek i koniec c1
    c2 = prefix2 + c2 + postfix2 # analogicznie dla c2

    return c1, c2

"""## Mutacja"""

def mutation(pop, pm): # pop, to mutowana populacja, pm, to prarametr (prawdopodobieństwo) mutacji
    # Zwróćmy uwagę, że w przypadku mutacji zmieniamy osobniki w populacji, a więc nie tworzymy nowej populacji ani nowych osobników
    for i in range(len(pop)): # Przechodzimy przez całą populację
        if random.random()<pm: # Losujemy, czy wykonać mutację
            mutation_inv(pop[i]) # jeśli tak, to aktualnego osobnika (pop[i], czyli i-tego osobnika) przekazujemy do odpowiedniej mutacji
        # Jeśli random.random()>=pm, czyli nie ma mutacji, to nic nie musimy robić

"""### Inwersja"""

def mutation_inv(ind):
    cut1 = random.randint(1,len(ind)) # Losujemy pierwszy punkt inwersji
    cut2 = random.randint(1,len(ind)) # Losujemy drugi punkt inwersji
    while cut2==cut1: # Dopóki punkty są takie same, to
        cut2 = random.randint(1,len(ind)) # losuj inny
    if cut1>cut2: # jeśli pierwszy punkt jest większy od drugiego, to
        cut1, cut2 = cut2, cut1 # je zamień miejscami

    ind[cut1:cut2] = ind[cut2-1:cut1-1:-1]

"""# Sukcesja 🆕"""

def succession(pop_P, fitness_P, pop_O, fitness_O):
    pop_P += pop_O
    fitness_P += fitness_O
    fit = [[f, i] for f,i in zip(fitness_P,range(len(fitness_P)))]
    fit.sort()
    return [pop_P[el[1]] for el in fit[:len(fit)//2]]

"""# Rozwiązanie 🔥

Wczytujemy liczbę miast oraz macierz odległości pomiędzy miastami
"""

# Parametry algorytmu
num_of_ind = 100
num_of_gen = 4000 # Liczba generacji (wykonań, kolejnych populacji) algorytmu
k = int(round(0.3*num_of_ind,0))
pc = 0.95 # Prawdopodobieństwo krzyżowania
pm = 0.05 # Prawdopodobieństwo mutacji

lines = open("berlin52.txt").readlines() # Otwarcie pliku i odczytanie do listy

num_of_cities = int(lines[0]) # Pierwsza linia, to liczba miast, zmieniamy na int i zapamiętujemy
distance_matrix = [[0 for _ in range(num_of_cities)] for _ in range(num_of_cities)] # Tworzymy macierz odległości, dla wielkości odpowiadającej liczbie miast i wszystko wypełniamy zerami

row = 1 # Zaczynamy od miasta o id 1, czyli od drugiego, bo w pierwszym jest tylko 0
for line in lines[2:]: # jak wyżej
    columns = list(map(int,line.strip().split())) # line.strip().split() -- czyścimy białe znaki i dzielimy na listę; map(int,...) zamieniamy elementy listy na int-y
    for col in range(len(columns)): # Przechodzimy przez komulny, ale po ich indeksach, aby móc zmieniać wartość w distance_matrix
        #columns[col] # odległość pomiędzy miastem row i col
        distance_matrix[row][col] = columns[col] # do macierzy odległości w miejscu row i col wpisujemy odległość pomiędzy row i col
        distance_matrix[col][row] = columns[col] # i odbicie, bo problem jest symetryczny
    row += 1 # zwiększamy indeks wiersza o 1

def genetic_algorithm(is_succession=True, print_info=False):
    ##########
    #
    # Tworzymy populację (inicjalizujemy) P (początkową i bazową)
    #
    ##########
    pop_P = new_population(num_of_ind,num_of_cities)

    ##########
    #
    # Oceniamy populację P
    #
    ##########
    fitness = evaluate_population(pop_P,distance_matrix)

    ##########
    #
    # Szukamy najlepszego w populacji początkowej
    #
    ##########

    # Tworzymy nowego soobnika, który początkowo jest najlepszy
    # jest to pierwszy osobnik z populacji.
    # Nasz najlepszy osobnik, to krotka, gdzie pierwszy element, to miasta, a
    # drugi element, to odległość -- dle efektywnego porównania potem).
    min_ind = (pop_P[0][:],fitness[0]) 
    # Następnie idziemy przez resztę populacji, szukając, czy nie ma lepszego.
    for i in range(1,len(pop_P)):
        if fitness[i]<min_ind[1]: # jeśli ocena aktualnego (i-tego) osobnika jest lepsza (mniejsza) od oceny nalepszego, czyli min_ind[1]
            # To aktualny jest nowym najlepszym:
            min_ind = (pop_P[i][:],fitness[i])    

    print("Najlepszy po losowym:", min_ind[1])

    all_min = [min_ind[1]]
    pop_max = [max(fitness)]
    pop_avg = [sum(fitness)/num_of_ind]

    ##########
    #
    # Pętla algorytmu genetycznego
    #
    ##########
    for gen in range(num_of_gen): # do warunku stopu, u nas liczba generacji
        # Selekcja
        pop_T = selection(pop_P, fitness, k) # dla czytelności przypisujemy do pop_T, jednak lepiej byłoby do pop, aby system operacyjny wiedział, że może zwolnić starą pamięć pop_P
        # Krzyżowanie
        pop_O = crossover(pop_T, pc)
        # Mutacja
        mutation(pop_O, pm)
        # Ocena nowej populacji
        fitness_O = evaluate_population(pop_O,distance_matrix)

        if is_succession:
            pop_P = succession(pop_P, fitness, pop_O, fitness_O)
        else:
            pop_P = pop_O
        fitness = evaluate_population(pop_P,distance_matrix)
        
        # Sprawdzamy, czy po wszystkich operacjach pojawił się jakiś nowy, najlepszy
        for i in range(num_of_ind): # Przechodzimy przez wszystkich osobników
            if fitness[i]<min_ind[1]: # mid_ind, to krotka, gdzie w [0] jest osobnik, a w [1] jego ocena; jeśli więc znajdziemy coś o mniejszej (lepsze) ocenia, to:
                min_ind = (pop_P[i][:],fitness[i]) # to tworzymy krotkę, z (kopią osobnika, jego funkcją oceny)
        
        if print_info and gen %100==0: # co 100 generacji wyświetlamy najlepszego
            print(min_ind[1])

        all_min.append(min_ind[1])
        pop_max.append(max(fitness))
        pop_avg.append(sum(fitness)/num_of_ind)
    print("Najlepszy po operacjach:", min_ind[1])

    if print_info: show_plot(all_min,pop_max,pop_avg)

    return min_ind[1]

import matplotlib.pyplot as plt
def show_plot(all_min,pop_max,pop_avg):
    ox = range(len(all_min))
    plt.plot(ox, all_min)
    plt.plot(ox, pop_max)
    plt.plot(ox, pop_avg)
    plt.show()

genetic_algorithm(False, print_info=True)

import pandas as pa
import numpy
import matplotlib.pyplot as plt
data = []
test_data = []

for is_succession in [True, False]:
    test_data = []
    for _ in range(3):
        test_data.append(genetic_algorithm(is_succession))
        print()
    data.append(test_data)

print(data)

df = pa.DataFrame(numpy.array(data))
df = df.transpose()

df.plot(kind="box")
plt.show()