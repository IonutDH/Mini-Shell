Dan-Hariton Ioan Marian
1220BF

Pentru inceput, in functia run_simple_commands am facut un array cu comenzile introduse la tastatura pentru a putea construi
functii plecand de la aceasta lista. Intai a trebuit sa testez comenzile cd si exit iar din cauza ca acestea sunt comenzi 
interne, a trebuit sa le implementez, deoarece nu pot fi executate de catre comanda execvp, pe care am folosit-o pentru
restul comenzilor externe cum ar fi ls, echo, cat etc. Dupa verificarea celor doua, am creat un proces cu os.fork() iar in 
interiorul copilului am efectuat testele pentru redirectari. Pentru fiecare redirectare a fost nevoie sa testez daca 
father_command-ul asociat redirectarii este None sau primeste un fisier ca parametru. Fiecare redirectare are functia ei, 
definite dupa run_simple_commands. In continuare am facut functia pentru && si || care sunt aproape la fel, singura 
diferenta fiind testul statusului (st in cod) care permite sau nu executarea celei de-a doua comenzi. Inca o functie ce 
trebuia implementata a fost si executarea comenzilor cu ajutorul operatorul de secvențiere ";". Aceasta si cu cele doua din 
urma, && si ||, sunt facute recursiv astfel incat functioneaza si pentru mai mult de 2 parametrii.