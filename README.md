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

```python
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

Rankomis užpildomi State duomenys, kadangi juos galima gauti pagal City stulpelį. 

### Duomenų išvalymas:

#### Kategoriniams duomenims uždedami tipai:
```python
data['Industry'] = data['Industry'].astype('category')
data['Name'] = data['Name'].astype('category')
data['Inception'] = data['Inception'].astype('category')
data['State'] = data['State'].astype('category')
data['City'] = data['City'].astype('category')
```
#### Like duomenys užpildomi Python pagalba:

Expenses stulpeliui šalinami "Dollars" ir kableliai:
```python
data['Expenses'] = data['Expenses'].str.replace("Dollars", "")
data['Expenses'] = data['Expenses'].str.replace(",", "")
data['Expenses'] = pd.to_numeric(data['Expenses'], errors='coerce', downcast='float')
```

Expenses stulpeliui šalinami "Dollars" ir kableliai:
```python
data['Expenses'] = data['Expenses'].str.replace("Dollars", "")
data['Expenses'] = data['Expenses'].str.replace(",", "")
data['Expenses'] = pd.to_numeric(data['Expenses'], errors='coerce', downcast='float')
```

Revenue stulpeliui šalinami "$" ir kableliai:
```python
data['Revenue'] = data['Revenue'].str.replace("$", "")
data['Revenue'] = data['Revenue'].str.replace(",", "")
data['Revenue'] = pd.to_numeric(data['Revenue'], errors='coerce', downcast='float')
```

Growth šalinamas procentų ženklas ir dalinama iš 100:
```python
data['Growth'] = data['Growth'].str.replace("%", "")
data['Growth'] = pd.to_numeric(data['Growth'], errors='coerce', downcast='float') / 100
```

Profit ir Employees nustatomas skaitinis tipas:
```python
data['Profit'] = pd.to_numeric(data['Profit'], errors='coerce', downcast='float')
data['Employees'] = pd.to_numeric(data['Employees'], errors='coerce', downcast='float')
```

Revenue ir Employees užpildomi pagal Industry stulpelio medianą:
```python
data['Revenue'].fillna(data.groupby('Industry')['Revenue'].transform('median'), inplace=True)
data['Employees'].fillna(data.groupby('Industry')['Employees'].transform('median'), inplace=True)
```
Bandoma užpildyti Expenses ir Profit naudojant formulę (Expenses = Revenue - Profit):
```python
data['Expenses'] = data['Expenses'].fillna(data['Revenue'] - data['Profit'])
data['Profit'] = data['Profit'].fillna(data['Revenue'] - data['Expenses'])
```

Nežinomiems Growth nustatomas 0:
```python
data['Growth'] = data['Growth'].fillna(value=0)
```

Tas eilutes kurių Revenue, Expenses, Profit, Industry nepavyko išskaičiuoti yra šalinamos:
```python
data = data[data['Revenue'].notna() & data['Expenses'].notna()
            & data['Profit'].notna() & data['Industry'].notna()]
```

Sutvarkius duomenys gaunami tokie rezultatai:

|       | Employees   | Revenue    | Expenses   | Profit      | Growth     |
|-------|-------------|------------|------------|-------------|------------|
| count | 495.000000  | 495.0      | 495.00     | 495.00      | 495.000000 |
| mean  | 148.870712  | 10831591.0 | 4297555.50 | 6532033.00  | 0.143232   |
| std   | 398.469299  | 3190166.5  | 2125169.75 | 3871154.25  | 0.069440   |
| min   | 1.000000    | 1614585.0  | -41678.00  | 12434.00    | -0.030000  |
| 25%   | 28.000000   | 8696234.5  | 2755930.00 | 3284662.50  | 0.080000   |
| 50%   | 56.000000   | 10651148.0 | 4316632.00 | 6512379.00  | 0.150000   |
| 75%   | 125.500000  | 13096431.0 | 5814274.00 | 9293752.50  | 0.200000   |
| max   | 7125.000000 | 21810052.0 | 9860686.00 | 19624534.00 | 0.300000   |