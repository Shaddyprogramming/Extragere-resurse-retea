Documentatie:

Codul a fost scris pentru a extrage resursele de retea de pe Wikipedia, folosind selectolax pentru parsare
si urllib pentru a accesa paginile web. Aceasta implementare este optimizata pentru a extrage linkuri
si imagini de pe pagina principala a Wikipedia. Proiectul este setat pentru a extrage un numar maxim de
100 de linkuri si toate imaginile de pe pagina. De asemenea, este configurat pentru a utiliza 10 fire de
executie pentru a accelera procesul de extragere a imaginilor, si aceastea sunt scrise intr-un fisier
text sau ecran. Toate proprietatile sunt setate ca variabile globale pentru a fi usor de modificat dupa
cerinta ultilzatorului.
Codul este structurat pentru a fi usor de inteles si de utilizat, cu functii separate
pentru crawling, parsare si scrierea rezultatelor in fisiere, este folosit executie in paralel pentru a
a accelera procesul de extragere a imaginilor.


Bibliografie:

https://www.reddit.com/r/webscraping/comments/znweub/advice_for_scraping_massive_number_of_items_faster/
https://pypi.org/project/selectolax/
https://www.youtube.com/watch?v=D4xCGnwjMZQ
https://www.youtube.com/watch?v=SAueUTQNup8

Pentru orice intrebari, probleme sau nelamuriri, va rugam sa ma contactati.
