# PRACA INŻYNIERSKA
* PL: Interaktywne narzędzie demonstrujące wykorzystanie różnych bibliotek Pythona do tworzenia wykresów
* ENG: Interactive tool for demonstrating capabilities of various Python libraries in drawing charts and plots

## Wymagania:
W celu odpalenia programu należy zainstalować:
### Interpreter
* `Python 3`
### GUI:
* `PyQt5`
* `PyQtWebEngine`
### PlotLibraries
* `MatPlotLib`
* `PyPlot`
* `PyQtGraph`
* `Bokeh`
### Misc
* `Pandas`
## Docs:
>TBD

## Instalacja
* pip install -r requirements.txt

## Jak odpalić
* **P**ull na repo
  ```
  git pull
  ```
* **U**twórz środowisko wirtualne
    ```
    mkdir env
    python3 -m venv env
    ```
* **A**ktywuj środowisko wirtualne
    ```
    source env/bin/activate
    ```
* **Z**ainstaluj pakiety
    ```
    pip install --upgrade pip
    pip install pyqt5
    pip install pyqtwebengine
    pip install matplotlib
    pip install pyplot
    pip install pyqtgraph
    pip install bokeh
    pip install pandas
    ```
* **E**njoy
    ```
    python3 main_v2.py
    ```
    
## CI
Analiza statyczna kodu na platformie CodeFactor: [Static analysis report](https://www.codefactor.io/repository/github/marynarz/praca_inzynierska)

## Funkcje
### Otwierane pliki
* TXT ```*.txt```
* CSV ```*.csv```
* JSON ```*.json```

### Obsługiwane typy wykresów:
* Liniowy (jedna linia)
* Słupkowy
* Kołowy

### Pzzetwarzanie danych
* Sortowanie po wybranej kolumnie
* Ustawienie wybranej kolumny jako wartość y
* Ustawienie wybranej kolumny jako wartość x

## Author:
### Niedzielski
