#%%
import pandas as pd
#%%
# A. PRISE EN MAIN
# %%
url = "https://raw.githubusercontent.com/Jrtoby/General-Ledger-Financial-Analysis/main/General-Ledger.xlsx"

gl = pd.read_excel(url, sheet_name="GL", usecols=[
    "GLID", "TxnDate", "Year", "Month", "AccountNumber", "AccountName",
    "Debit", "Credit", "Dept", "CostCenter", "Description", "Currency",
    "NetAmount", "RateToUSD", "Debit_USD", "Credit_USD", "NetAmountUSD", "AccountType"
])
taux_change = pd.read_excel(url, sheet_name="ExchangeRate")
# %%
gl
# %%
print(gl.shape)
print(taux_change)
print(gl.dtypes)
# %%
print(gl['Dept'].unique())
print(gl['AccountName'].unique())
print(gl["AccountType"].unique())
print(gl['Currency'].unique())
# %%
# CONTROL QUALITE - EQUILIBRE DU GRAND LIVRE

# %%
total_debit = gl['Debit'].sum()
total_credit = gl['Credit'].sum()
ecart = total_debit - total_credit

print(total_debit)
print(total_credit)
print(ecart)
# %%
# Décomposition de l'écart de -763041.46 en AccountType
type_group = gl.groupby('AccountType')[['Debit','Credit']].sum()
print(type_group)
# %%
total_d = type_group.loc['COGS','Debit'] + type_group.loc['Expense','Debit']
total_c = type_group.loc['Revenue','Credit']
ecart = total_c - total_d

print(ecart)

# %%
# il s'agit donc du profit 
# %%
# VALIDATION DE LA CONVERSION MULTI-DEVISES
# %%
devises = gl.merge(
    taux_change,
    on = 'Currency',
    how = 'left'
)
devises['Debit2USD'] = devises['Debit'] * devises['Rate2USD']
devises['Credit2USD'] = devises['Credit'] * devises['Rate2USD']

devises['ecart_debit'] = devises['Debit2USD'] - devises['Debit_USD']
devises['ecart_credit'] = devises['Credit2USD'] - devises['Credit_USD']

print(devises['ecart_debit'].unique())
print(devises['ecart_credit'].unique())
# %%
# les valeurs uniques des colonnes devises['ecart_credit'] et devises['ecart_debit'] sont [0.] et [0.] , ce qui confirme que les colonnes Debit_USD et Credit_USD sont bien calculées
# %%
#D. CONSTRUCTION DU COMPTE DE RESULTAT (P&L)
# %%
cr = gl.groupby('AccountName')[['NetAmountUSD']].sum()

ca_total = (
    cr.loc['Online Sales', 'NetAmountUSD'] + 
    cr.loc['Sales Revenue', 'NetAmountUSD']
)* -1
print(f"CHIFFRE D'AFFAIRES TOTAL : {ca_total:,.0f} USD")

cogs = cr.loc['COGS','NetAmountUSD']
print(f"COGS TOTAL : {cogs:,.0f} USD")

marge_brute = ca_total - cogs
print(f"MARGE BRUTE : {marge_brute:,.0f} USD")

taux_marge = marge_brute / ca_total
print(f"TAUX DE MARGE BRUTE : {taux_marge:.1%}")

charges_totales = (
    cr.loc['COGS','NetAmountUSD'] + 
    cr.loc['Payroll Expense','NetAmountUSD'] + 
    cr.loc['Travel Expense','NetAmountUSD']
)
print(f"CHARGES TOTALES : {charges_totales:,.0f} USD")

rai = (
    ca_total - 
    charges_totales
) 
is_impot = rai * 0.30 #j'ai ici supposé 30% comme IS
resultat_net = rai - is_impot
print(f"RESULTAT NET : {resultat_net:,.0f} USD")
# %%
print(devises['TxnDate'].dtype)
# %%
group = devises.groupby(['Year','Month','AccountName'])['NetAmountUSD'].sum().unstack(fill_value = 0)
group
# %%
group['Chiffre_daffaires'] = (group['Online Sales'] + group['Sales Revenue']) * -1
group['Charges_totales'] = group['COGS'] + group['Payroll Expense'] + group['Travel Expense']
group['rai'] = group['Chiffre_daffaires'] - group['Charges_totales'] 
group['is_impot'] = group['rai'] * 0.30  #j'ai maintenu les 30% pour l'IS
group['resultat_net'] = group['rai'] - group['is_impot']
group
# %%
annuel = group.groupby('Year')[['Chiffre_daffaires','resultat_net']].sum()
mensuel = group.groupby('Month')[['Chiffre_daffaires','resultat_net']].sum()
an_mois = group.groupby(['Year','Month'])[['Chiffre_daffaires','resultat_net']].sum()

(annuel)
# %%
(mensuel)
# %%
an_mois
# %%
# E. ANALYSE PAR DEPARTEMENT ET CENTRE DE COUT
# %%
devises
# %%
par_dept = devises.groupby(['Dept'])['Debit'].sum() #j'ai garder Débit et non debit_usd et j'ai combiné ici toutes les charges y compris les COGS, j'espère ne pas m'être trompé sur ça
print(par_dept.sort_values(ascending=False)) 
# le Departement HR génêre le plus de charges soit 227069.82 et Operations le moins de charges pour 176130.68
# %%
croisement = devises.pivot_table(
    index = 'Dept',
    values = 'Debit',
    columns = 'AccountType',
    aggfunc='sum'
)
croisement
# %%
gl
# %%
nb_compte = gl['AccountNumber'].value_counts()
nb_compte

# on retrouve 412 compte de 5010 le plus grand nombre d'enregistrement, compte Travel Expense
# %%
annuel = group.groupby('Year')[['Chiffre_daffaires','resultat_net']].sum()
annuel
# %%
annuel['YoY_CA_%'] = annuel['Chiffre_daffaires'].pct_change() * 100
annuel[['Chiffre_daffaires','YoY_CA_%']]
# %%
##le tableau annuel permet de lire une chute du chiffre d'affaire en 2025 d'environ 500,000 soit une baisse de 55% alors nous nous interresseront sur l'origine de cette baisse soudaine
# %%
#ETANT DONNE QUE LE RESULTAT NET SUIT EGALEMENT LA BAISSE, ON NE S'INTERRESSERA PAS DONC AUX CHARGES MAIS AUX DEPARTEMENTS, MOIS COSTCENTER OU SE LOCALISE LA DIFFERENCE SIGNIFICATIVE AVEC LES AUTRES ANNEES
#ON VA REVENIR A LA TABLE devises OU ON PEUT ENCORE RETROUVER TOUTES NOS COLONNES AVANT TOUTES LES DIVERSES MODIFICATIONS EFFECTUEES

invest = devises[['Year', 'Month', 'Dept', 'CostCenter', 'AccountName', 'AccountType','NetAmount']]
invest
# %%
investigation = invest[
    (invest['Year']!=2023) &
    (invest['AccountType']=='Revenue')
].copy()
investigation['CA'] = investigation['NetAmount'] * -1
investigation = investigation.drop(columns = ['NetAmount'])
investigation
# %%
print(investigation['Year'].unique())
print(investigation['AccountType'].unique())
# %%
par_mois = investigation.pivot_table(
    values = 'CA',
    index = 'Month',
    columns = 'Year',
    aggfunc = 'sum'
)
par_mois
# CE TABLEAU PRESENTE DES DONNEES VIDES EN 2025 DANS LES MOIS DE AOUT DEC JUILLET NOV OCT SEPT
# CALCULONS LE TOTAL DU CA DE 2025 OBSERVE POUR VERIFIER LA CORRESPONDANCE AVEC LE TOTAL OBSERVER DANS LE TABLEAU annuel
ca_2025 = investigation[investigation['Year'] == 2025]['CA'].sum()
ca_2025 
print(384761.3/413398.9648*100)
# on obient 384761.3 pour le ca_2025 soit 93.07263267728433 du chiffre d'affaire total
# ON PEUT DEJÀ CONCLURE QU'IL S'AGIT D'UN EXERCICE ENCORE EN COURS DONT LES DONNEES NOUS ONT ETE ENVOYES EN JUILLET POUR ANALYSE
# DONC IL NE S'AGIT PAS ICI D'UNE CHUTE DE CHIFFRE D'AFFAIRE EN 2025
# TOUTE FOIS NOUS ETUDIERONS LA SAISONNALITE DES ACTIVITES DE CETTE ENTREPRISE DE DEVISES
#%%
group

date2025 = group[group.index.get_level_values('Year') != 2025]

mensuel = date2025.groupby('Month')[['Chiffre_daffaires','resultat_net']].sum()

# %%
month_dic = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}
mensuel.index = mensuel.index.map(month_dic)

mensuel = mensuel.sort_index(ascending = True)
mensuel['variation_CA_%'] = mensuel['Chiffre_daffaires'].pct_change() * 100

print(mensuel['variation_CA_%'])

# je te laisse faire l'analyse avec moi je ne sais pzs ici comment decrire et analyser levolutin mensuelle des ventes de ce type d'entreprise : de devises
# %%
devises
# %%
compte = {
    'Revenue' : 'Chiffre d\'affaire',
    'COGS' : 'Cout des ventes',
    'Expense' : 'Charges opérationnelles'
}
pnl = devises[['AccountType','NetAmountUSD']].copy()

pnl['post_reporting'] = pnl['AccountType'].map(compte)

bon_sens = {
    'Chiffre d\'affaire' : -1 , 
    'Cout des ventes' : 1 ,
    'Charges opérationnelles' : 1
}
pnl['sens'] = pnl['post_reporting'].map(bon_sens)
pnl['Montant'] = pnl['NetAmountUSD'] * pnl['sens']
pnl
# %%
compte_resultat = pnl.groupby('post_reporting')['Montant'].sum()

# %%
compte_resultat
#%%
ca = compte_resultat.loc['Chiffre d\'affaire']
cogss = compte_resultat.loc['Cout des ventes']
opex = compte_resultat.loc['Charges opérationnelles']
#%%
marg_brute = ca - cogss
av_impot = marg_brute - opex
impot = av_impot * 0.30
resultatnet = av_impot - impot

# %%
print('----------- MINI COMPTE DE RESULTAT -----------')
print('')
print(f"Chiffre d\'affaires :          {ca:,.0f} USD")
print(f"Côut des ventes COGS :         {cogss:,.0f} USD")
print(f"--------------------------------------")
print(f"Marge Brute :           {marg_brute} USD")
print(f"Charges operationnelles :          {opex:,.0f} USD")
print(f"--------------------------------------")
print(f"Résultat avant impot :           {av_impot:,.0f} USD")
print(f"Impôt :           {impot:,.0f} USD")
print(f"--------------------------------------")
print(f"Résultat Net : {resultatnet:,.0f} USD")

# %%
