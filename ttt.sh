#!/bin/bash

PLANSZA=('_' '_' '_' '_' '_' '_' '_' '_' '_')
GRACZ=$((1 + $RANDOM % 2))
WYGRANA=0
liczbaRuchow=1
koniecGry=0
znakGracza=('o' 'x')

function wyswietlNumeryPol() {
  echo Numery pól na planszy:
  echo '0 | 1 | 2'
  echo '3 | 4 | 5'
  echo '6 | 7 | 8'
}

function wyswietl() {
  echo
  echo Plansza:
  echo ${PLANSZA[0]} '|' ${PLANSZA[1]} '|' ${PLANSZA[2]}
  echo ${PLANSZA[3]} '|' ${PLANSZA[4]} '|' ${PLANSZA[5]}
  echo ${PLANSZA[6]} '|' ${PLANSZA[7]} '|' ${PLANSZA[8]}
}

function sprawdzPionowo() {
  for pole in 0 1 2; do
    if [ ${PLANSZA[${pole}]} == '_' ]; then
      continue
    elif [ ${PLANSZA[${pole}]} == ${PLANSZA[${pole} + 3]} ] && [ ${PLANSZA[${pole}]} == ${PLANSZA[${pole} + 6]} ]; then
      echo WYGRYWA GRACZ ${GRACZ}. Koniec gry
      WYGRANA=1
      koniecGry=1
    fi
  done
}

function sprawdzPoziomo() {
  for pole in 0 3 6; do
    if [ ${PLANSZA[${pole}]} == '_' ]; then
      continue
    elif [ ${PLANSZA[${pole}]} == ${PLANSZA[${pole} + 1]} ] && [ ${PLANSZA[${pole}]} == ${PLANSZA[${pole} + 2]} ]; then
      echo WYGRYWA GRACZ ${GRACZ}
      WYGRANA=1
      koniecGry=1
    fi
  done
}

function sprawdzPrzekatne() {
  if [ ${PLANSZA[0]} == ${PLANSZA[4]} ] && [ ${PLANSZA[0]} == ${PLANSZA[8]} ] && [ ${PLANSZA[0]} != '_' ]; then
    echo WYGRYWA GRACZ ${GRACZ}
    WYGRANA=1
    koniecGry=1
  elif [ ${PLANSZA[2]} == ${PLANSZA[4]} ] && [ ${PLANSZA[2]} == ${PLANSZA[6]} ] && [ ${PLANSZA[2]} != '_' ]; then
    echo WYGRYWA GRACZ ${GRACZ}
    WYGRANA=1
    koniecGry=1
  fi
}

function sprawdzWygrana() {
  sprawdzPionowo
  sprawdzPoziomo
  sprawdzPrzekatne
}

function zmienGracza() {
  if [ $GRACZ -eq '1' ]; then
    GRACZ='2'
  else
    GRACZ='1'
  fi
}

echo Gra w kółko i krzyżyk
echo Zaczyna gracz $GRACZ
wyswietlNumeryPol

while [ $koniecGry -eq '0' ]; do
  if [ $liczbaRuchow -le 9 ]; then
    wyswietl
    echo -e '\nKtóre pole zaznaczyć dla zawodnika' ${GRACZ}'?'
    read POLE

    echo Zaznaczam pole: ${POLE}
    if [ ${POLE} -gt 8 ]; then
      echo Złe pole
      echo Podaj pole z przedziału [0-8]
      wyswietlNumeryPol
      continue
    elif [ ${PLANSZA[${POLE}]} != "_" ]; then
      echo Złe pole
      echo Podaj WOLNE pole z przedziału [0-8]
      continue
    fi
    PLANSZA[${POLE}]=${znakGracza[${GRACZ} - 1]}
    sprawdzWygrana
    let liczbaRuchow=$liczbaRuchow+1
    zmienGracza
  else
    let koniecGry=1
    echo REMIS. Koniec gry
  fi
done
