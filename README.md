# TTT4280-Sensorer-og-instrumentering
### Laboppgaver i faget Sensorer og instrumentering 
* Lab1 består av oppkobling av systemet som skal brukes i de andre laboppgavene. Dette inebærer å koble opp 5 ADCer og muliggjøre avlesning på Raspberry pi.

* Lab2 innebærer å bruke tre lydsensorer/mikrofoner for å finne ut av i hvilken rettningen en lydkilde befinner seg. Dette gjøres ved å filterer bort støy og bruke crosscorrelation og trigonometri for å finne i hvilken retning lydkilden ligger. Overføringen av data skjer ved bruk av TCP-sockets som er implementert i C på pien og i python på PC der også all processering av data foregår.