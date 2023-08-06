Pyfuso
======
#### Esse pacote realiza conversões de fusohorario de acordo com a região requerida pelo usuário


## Instalação:
    pip install Pyfuso

## Uso:

import Pyfuso as pf


## Retorna as opcões de fusohorario disponíveis
print(pf.get_local()) 

## Retorna a data referente ao local
date = pf.get_data('local_desejado') 

## Retorna a data referente ao local e no formato desejado  ex.: 'D/M/A', 'M/D/A', 'A/M/D' 
date_formatobr = pf.get_data_formato('local_desejado','D/M/A') 

## Retorna a diferença de horarios dos locais desejados
dif_fuso = pf.get_time_diff('local1','local2')


