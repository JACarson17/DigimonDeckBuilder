from pathlib import Path
from typing import Tuple

root = Path.cwd()
formats = ['BT11-EX3.txt','ST14-BT12-EX4']

def getLists(listPath: Path) -> Tuple[dict[str, dict[str, int]], int]:
    listFile = open(listPath, 'r')
    lines = listFile.readlines()
    lists: dict[str, dict[str, int]] = {}
    deckCount = 0
    for line in lines:
        lineList = line.split(',')
        for i, l in enumerate(lineList):
            num = l.strip('"[]\n')
            if i == 0:
                auth = num
                deckCount += 1
            else:
                if num not in lists.keys():
                    lists.update({num:{auth: 1}})
                elif auth not in lists[num].keys():
                    lists[num].update({auth:1})
                else:
                    lists[num][auth] += 1
    listFile.close()
    return(lists, deckCount)

def weighCards(cards: dict[str, dict[str, int]], decks: int) -> Tuple[dict[str, dict[str, int]], set]:
    weights:set[float] = set()
    for card in cards:
        total = sum(cards[card].values())
        usedIn = len(cards[card].keys())
        weight = total/decks
        weights.add(weight)
        cards[card].update({'weight':weight})
        cards[card].update({'Decks Used':usedIn})
    weightList = [w for w in weights]
    weightList.sort()
    weightList.reverse()
    return(cards, weightList)

def checkEgg(card: str) -> bool:
    info = card.split('-')
    if 'BT' in info[0] and int(info[1]) <=6:
        return True
    else:
        return False

def addEggs(deck:dict[str, int], eggs:dict[str, int]) -> dict[str, int]:
    if eggs['total'] <= 4:
        for card in eggs:
            if card == 'total':
                continue
            else:
                if eggs['total'] >= 5:
                    break
                elif eggs[card] <=4:
                    amt = 4-eggs[card]
                    for i in range(0, amt):
                        eggs[card] +=1
                        eggs['total'] += 1
                        if eggs['total'] >= 5:
                            break

    eggs.pop('total')
    deck.pop('total')
    for egg in eggs:
        deck.update({egg:eggs[egg]})
    return(deck)


def makeDeck(cards: dict[str, dict[str, int]], deckCount: int, weights: list) -> dict[str, int]:
    deck: dict[str, int] = {'total': 0}
    eggs: dict[str, int] = {'total': 0}
    decks = [d+1 for d in range(deckCount)]
    decks.reverse()
    for d in decks:
        for w in weights:
            for card in cards:
                if cards[card]['Decks Used'] == d and cards[card]['weight'] == w:
                    if round(w) == 0:
                        amt = 1
                    else:
                        amt = round(w)
                    if checkEgg(card) == False: #not an egg
                        deck.update({card:amt})
                        deck['total']+= amt
                    elif eggs['total'] <=5: #egg and space in egg deck
                        eggs.update({card:amt})
                        eggs['total'] += amt
                    else:                   #no space in egg deck
                        continue
                if deck['total'] >= 50:
                    break
            if deck['total'] >= 50:
                    break
        if deck['total'] >= 50:
                    break
    
    deck = addEggs(deck,eggs)
    return(deck)
    

def digimonDevExport(deck: dict[str, int], name: str):
    n = name + '.txt'
    path = root/'Exports'/n
    file = open(path, 'w')
    for card in deck:
        tot = deck[card]
        if tot <= 4:
            file.write(f'{tot} {card}\n')
        else:
            for i in range(tot//4):
                if i == tot//4:
                    if tot%4 != 0:
                        file.write(f'{tot%4} {card}\n')
                else:
                    file.write(f'4 {card}\n')
    file.close()

def run(deckName: str, frmt: str):
    for f in formats:
        if frmt in f:
            listPath = root/deckName/f
            break
    
    cards, decks = getLists(listPath)
    cards, weights = weighCards(cards, decks)
    deck = makeDeck(cards, decks, weights)
    digimonDevExport(deck, ' '.join([deckName, frmt]))

if __name__ == '__main__':
    deck = input('Deck Name: ')
    frmt = input('Format: ').upper()
    # deck = 'Machinedramon'
    # frmt = 'BT11'
    run(deck, frmt)