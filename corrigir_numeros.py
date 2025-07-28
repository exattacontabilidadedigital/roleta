import pandas as pd

# Lê o arquivo CSV
df = pd.read_csv('contatos.csv')

# Corrige os números que não têm o +
for index, row in df.iterrows():
    numero = str(row['contato']).strip()
    if numero.startswith('55') and not numero.startswith('+55'):
        df.at[index, 'contato'] = '+' + numero
        print(f"Corrigido: {numero} -> +{numero}")

# Salva o arquivo corrigido
df.to_csv('contatos.csv', index=False)
print(f"\n✅ Arquivo corrigido! {len(df)} contatos processados.")
print("Todos os números agora têm o formato +55DDDNUMERO") 