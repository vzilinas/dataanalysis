# Duomenų tyrybos praktinė užduotis
## Įžanga
Šiame darbe nagrinėjamas Future-500-17.csv. 
Duomenų aibei nagrinėti naudojamas Python 3.8
**Užduoties tikslas** – išanalizuoti duotų duomenų aibę, atlikti pirminį duomenų apdorojimą: užpildyti praleistus duomenis, išskirti taškus atsiskyrėlius, pritaikyti kelis normavimo metodus, pateikti aprašomąsias duomenų statistikas. Atlikti tiriamos aibės vizualią analizę, naudojant taškines, stačiakampes diagramas, histogramas, dimensijos mažinimo algoritmus.

**Uždaviniai**:
1. Aprašyti užduoties tikslą ir uždavinius.
2. Trumpai aprašyti tiriamą duomenų aibę, kokie požymiai: skaitiniai, ranginiai ir pan.?
3. Pateikti atskirų požymių aprašomąsias statistikas lentelės pavidalu: min, max, 1, 3 kvartilės, vidurkis mediana, dispersija ir pan.
4. Pasirinktais metodais užpildyti praleistas reikšmes, mokėti argumentuoti, kokį metodą taikėte ir kodėl.
5. Nustatyti taškus atsiskyrėlius, pašalinti juos iš duomenų aibės, palyginti, kaip pasikeitė imties statistiniai duomenys.
6. Sunormuoti duomenų aibę naudojant du normavimo metodus: pagal vidurkį ir dispersiją, min - max.
7. Pateikti vizualią duomenų aibės analizę: taškiniai grafikai, dažnio diagramos, histogramos, stačiakampės diagramos. Po kiekvienu grafiku turi būti interpretacija, kokias išvadas gauname analizuojant grafikus. Kaip pajamos priklauso nuo pramonės šakos? Koks pelno pasiskirstymas pagal valstijas? Ir t.t.
8. Apskaičiuoti požymių koreliacijas, pateikti skaitinius įverčius lentelės pavidalu.
9. Duomenų aibę suformuoti paliekant tik skaitinius požymius ir Industry stulpelį. Vizualizuoti daugiamačius duomenis naudojant PCA ir MDS algoritmus.
10. Reikia pateikti atliekamos užduoties kodus.

## Duomenų aibė

**Imties dydis** - Nagrinėjami duomenys susidaro iš 500 įmonių.

**Imties duomenų savybės** - Nagrinėjama duomenų aibė susidaro iš požymių: ID, Name, Industry, Inception, Employees, State, City, Revenue, Expenses, Profit, Growth.

Šios savybės skaidomi į šiuos tipus:

**Nominalieji**: Industry, Inception, State, City,

**Ranginiai**: ID

**Kiekybiniai diskretieji**: Revenue, Expenses, Profit, Employees

**Tolydieji**: Growth

## Duomenų priešanalizė

Neapdorotu duomenis analizuojant su Python priedu Pandas 

```
data = pd.read_csv("Future-500-17.csv")
print(data.describe(include='all'))
``` 

|        | ID         | Name | Industry | Inception   | Employees   | State | City | Revenue | Expenses | Profit       | Growth |
|--------|------------|------|----------|-------------|-------------|-------|------|---------|----------|--------------|--------|
| count  | 500.000000 | 500  | 497      | 499.000000  | 495.000000  | 495   | 500  | 493     | 495      | 4.970000e+02 | 497    |
| unique | NaN        | 500  | 7        | NaN         | NaN         | 42    | 297  | 493     | 495      | NaN          | 32     |
| freq   | NaN        | 1    | 145      | NaN         | NaN         | 57    | 13   | 1       | 1        | NaN          | 39     |
| mean   | 250.500000 | NaN  | NaN      | 2010.174349 | 149.161616  | NaN   | NaN  | NaN     | NaN      | 6.534190e+06 | NaN    |
| std    | 144.481833 | NaN  | NaN      | 3.228211    | 398.474670  | NaN   | NaN  | NaN     | NaN      | 3.872034e+06 | NaN    |
| min    | 1.000000   | NaN  | NaN      | 1999.000000 | 1.000000    | NaN   | NaN  | NaN     | NaN      | 1.243400e+04 | NaN    |
| 25%    | 125.750000 | NaN  | NaN      | 2009.000000 | 27.500000   | NaN   | NaN  | NaN     | NaN      | 3.259485e+06 | NaN    |
| 50%    | 250.500000 | NaN  | NaN      | 2011.000000 | 56.000000   | NaN   | NaN  | NaN     | NaN      | 6.512379e+06 | NaN    |
| 75%    | 375.250000 | NaN  | NaN      | 2012.000000 | 126.000000  | NaN   | NaN  | NaN     | NaN      | 9.314149e+06 | NaN    |
| max    | 500.000000 | NaN  | NaN      | 2014.000000 | 7125.000000 | NaN   | NaN  | NaN     | NaN      | 1.962453e+07 | NaN    |

Gauname tokius rezultatus iš kurių matome, jog trūksta duomenų visur išskyrus Name, Industry. Todėl duomenis turime apvalyti.

## Praleistų reikšmių užpildymas


