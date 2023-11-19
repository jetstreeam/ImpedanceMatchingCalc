
#%%

from si_prefix import si_format
import decimal

n = [.5, .0000001331, 1332, 123.5]

si_prefixes = {'': '',
               '-18': 'a',
               '-15': 'f',
               '-12': 'p',
               '-09': 'n',
               '-06': 'u',
               '-03': 'm',
               '+03': 'k',
               '+06': 'M',
               '+09': 'G'
               }

def addSiPrefix(number):
    
        #n = format(number,'.0e').split('e')
        n = number.split('E')
        z = si_prefixes[format(i,'.0e').split('e')[1]] if len(n) > 1 else ''
        return(n[0]+z)


for i in n:
    #print(addSiPrefix(decimal.Decimal(i.normalize().to_eng_string()))
    #print(decimal.Decimal(i).normalize().to_eng_string())

    print(addSiPrefix(i))

#%%
import matplotlib as mpl
from matplotlib.ticker import EngFormatter

n = [.5, .0000001331, 1332, 123.5]
for i in n:
    formatter = mpl.ticker.EngFormatter()
    print(EngFormatter.format_eng(i,3))


#%%
from engineering_notation import EngNumber

n = [.5, .0000001331, 1332, 123.5]
for i in n:
    print(EngNumber(i))
    #print(EngNumber(i, precision=0))

#%%
def engineering_notation(number):
    if number == 0:
        print("0.0")
        return

    exponent = 0
    while abs(number) >= 1000:
        number /= 10.0
        exponent += 3

    result = "{:.3e}".format(number)
    result_parts = result.split('e')
    coefficient = float(result_parts[0])
    exponent += int(result_parts[1])

    # Round the coefficient to 3 significant figures
    coefficient = round(coefficient, 3)

    result = "{:.3g}e{}".format(coefficient, exponent)
    print(result)

for i in n:
    engineering_notation(i)