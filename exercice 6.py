import random
import sys
import time
import sqlite3

# function create player table (pas fini)
def create_player_table(): 
  try: 
    connection = sqlite3.connect('Projet-rpg-python/Rpg.db')
    cursor = connection.cursor()
    cursor.execute("""
      create table if not exists player_data(
                  player_id integer primary key autoincrement unique not null,
                  player_name text not null,
                  player_class text null,
                  player_hpmax integer null,
                  player_hp integer null,
                  player_atk integer null,
                  player_magie integer null,
                  player_lvl integer null,
                  player_xp integer null,
                  player_gold integer null
      )
  """)
    connection.commit()
  finally:
    connection.close()

# function affiche liste joueur
def display_player_data():
    try:
        connection = sqlite3.connect('Projet-rpg-python/Rpg.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM player_data")
        players = cursor.fetchall()
        print("Liste des joueurs :")
        for player in players:
            print(player)
    finally:
        connection.close()

# function ajouter un joueur dans la base de données(pas fini)
def insert_player_data(player_name,player_class,hp_du_perso_max,hp_du_perso,atk,magie,lvl,xp,gold):
   connection = sqlite3.connect('Projet-rpg-python/Rpg.db')
   cursor = connection.cursor()
   cursor.execute("""
        insert into player_data (player_name, player_class, player_hpmax, player_hp, player_atk, player_magie, player_lvl, player_xp, player_gold)
                  values (?,?,?,?,?,?,?,?,?)
""", (player_name, player_class,hp_du_perso_max,hp_du_perso,atk,magie,lvl,xp,gold))
   connection.commit()
   connection.close()

# fonction update player
def update_player_data_by_name(player_name, hp_du_perso_max, hp_du_perso, atk, magie, lvl, xp, gold):
    connection = sqlite3.connect('Projet-rpg-python/Rpg.db')
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE player_data
        SET player_hpmax = ?,
            player_hp = ?,
            player_atk = ?,
            player_magie = ?,
            player_lvl = ?,
            player_xp = ?,
            player_gold = ?
        WHERE player_name = ?
""", (hp_du_perso_max, hp_du_perso, atk, magie, lvl, xp, gold, player_name))
    connection.commit()
    connection.close()

player_name = 'Jean Cule'
player_class = 'Merde Ultime'
hp_du_perso_max = 1000
hp_du_perso = 1000
atk = 100
magie = 100
lvl = 0
xp = 0
perdu = 0
message = 0
messages = 0
augmenter = 0
gold = 20
fuite_unlock = 0
fuite = 0
choix = 0
choice = ""
skip_turn = 0
choix_shop = 0
potion_de_soin = 3
invalides = 0

menuchoix = 0
verif = 0

def level():
  global lvl
  global xp
  global message
  global augmenter
  global messages
  if xp >= 3000:
      lvl = 5
      message = 5
  elif xp >= 2250:
      lvl = 4
      message = 4
  elif xp >= 1500:
      lvl = 3
      message = 3
  elif xp >= 200:
      lvl = 2
      message = 2
  elif xp >= 100:
      lvl = 1
      message = 1
  if message != messages:
    print("Vous avez gagné un niveau !")
    print("Vous êtes maintenant niveau ", lvl)
    augmenter = 1
  messages = message
  augmenter_les_stats()
  return lvl, augmenter

def augmenter_les_stats():
  global augmenter
  global lvl
  global atk
  global hp_du_perso_max
  global magie
  if augmenter == 1:
    if lvl == 1:
      atk = atk + 5
      magie = magie + 5
      hp_du_perso_max = hp_du_perso_max + 100
    if lvl == 2:
      atk = atk + 7.5
      magie = magie + 8
      hp_du_perso_max = hp_du_perso_max + 150
    if lvl == 3:
      atk = atk + 10
      magie = magie + 10
      hp_du_perso_max = hp_du_perso_max + 200
    if lvl == 4:
      atk = atk + 12.5
      magie = magie + 12.5
      hp_du_perso_max = hp_du_perso_max + 250
    if lvl == 5:
      atk = atk + 15
      magie = magie + 15
      hp_du_perso_max = hp_du_perso_max + 300
    print ("\nvous avez maintenant :" , hp_du_perso_max, " de vie", atk, " d'attaque\n")
    print (magie, " de magie" , " et ", hp_du_perso_max, " de vie")
  augmenter = 0
  return hp_du_perso_max, atk, magie, augmenter

def reset_stats():
    return [
        {"nom": "Acheron", "hp": 1600, "atk": 75, "xp": 100, "gold": 10},
        {"nom": "Bloodlust", "hp": 800, "atk": 60, "xp": 80, "gold": 8},
        {"nom": "Kenos", "hp": 1300, "atk": 50, "xp": 85, "gold": 8.5},
        {"nom": "Arcturus", "hp": 1690, "atk": 69, "xp": 90, "gold": 9},
        {"nom": "Zodiac", "hp": 2500, "atk": 25, "xp": 75, "gold": 7.5},
        {"nom": "Void Wave", "hp": 2000, "atk": 25, "xp": 70, "gold": 7.0},
        {"nom": "Abyss Of Darkness", "hp": 3000, "atk": 60, "xp": 9.5, "gold": 9.5},
        {"noms": "Slaughterhouse", "hp": 3500, "atk": 50, "xp": 9.5, "gold": 9.5},
        {"nom": "Bloodbath", "hp": 1000, "atk": 80, "xp": 9.5, "gold": 9.5},
        {"nom": "Kyouki", "hp": 4000, "atk": 50, "xp": 9.5, "gold": 12}
    ]

def shop():
  global gold
  global choix_shop
  global potion_de_soin
  print("vous avez", gold, "d'or, voulez vous acheter quelque chose?\n")
  print("0: rien je m'en vais")
  print("1: acheter une potion de soin (10 d'or)")
  choix_shop = input("choix: ")
  if choix_shop == "0":
      print("\nvous êtes parti\n")
  elif choix_shop == "1":
      if gold >= 10:
          gold = gold - 10
          potion_de_soin += 1
          print("vous avez maintenant", potion_de_soin, "potions de soin\n")
          shop()
      else:
          print("\nvous n'avez pas assez d'argent\n")
          shop()
  else:
      print("\ndonnée incorrecte, veuillez recommencer\n")
      shop()
  
def faire_combat():
  global hp_du_perso
  global atk
  global lvl
  global magie
  global xp
  global perdu
  global gold
  global fuite
  global fuite_unlock
  global skip_turn
  global potion_de_soin
  global invalides
  monstre_actuel = None 
  fuite = 0
  while hp_du_perso > 0:
      if monstre_actuel is None: 
          monstre_actuel = random.choice(reset_stats())
          print("Vous tombez sur un", monstre_actuel["nom"], "sauvage.")
          print("\nQue voulez-vous faire?")

      print("Vos points de vie:", hp_du_perso, "/", hp_du_perso_max)
      print("Ses points de vie:", monstre_actuel["hp"], "pv")
      print("\n1: Attaquer - Votre attaque =", atk, "d'attaque")
      print("2: Magie - Votre magie =", magie, "de magie")
      print("3: Potion de soin - (restaure 20% de santé totale), vous en avez", potion_de_soin , "en votre possession")
      if fuite_unlock == 1:
        print("4: Fuir - Vous fuyez")

      skip_turn = 0
      choix = input("Choix: ")
      if choix == "1":
          print("\nVous attaquez", monstre_actuel["nom"])
          monstre_actuel["hp"] -= atk
          print(monstre_actuel["nom"], "a", monstre_actuel["hp"], "pv")
      elif choix == "2":
          print("\nVous lancez un sort de magie")
      elif choix == "3":
        if potion_de_soin > 0:
          hp_du_perso += hp_du_perso_max * 0.2
          if hp_du_perso > hp_du_perso_max:
              hp_du_perso = hp_du_perso_max
          print("\nVous avez restauré 10% de votre vie, il vous reste", hp_du_perso)
          print("/", hp_du_perso_max, "pv")
          potion_de_soin -= 1
        else:
          print("\nVous n'avez plus de potions de soin.\n")
          skip_turn = 1
      elif fuite_unlock == 1:
          if choix == "4":
            print("\nVous fuyez")
            fuite = 1
            break
      else:
          print("\nChoix invalide")
          continue
      if fuite == 1:
        break
      if monstre_actuel["hp"] <= 0:
          if hp_du_perso<= 0:
              print("\nMais vous êtes mort aussi.")
              sys.exit()
          else:
              print("\nVous avez gagné")
              xp += monstre_actuel["xp"]
              print("\nVous avez gagné", monstre_actuel["xp"], "points d'expérience")
              gold += monstre_actuel["gold"]
              print("Vous avez", gold, "pièces d'or")
              print("Vous êtes à", xp, "d'expérience")
              monstre_actuel = None
          break
      if skip_turn == 0:
        print("\nTour de", monstre_actuel["nom"])
        hp_du_perso -= monstre_actuel["atk"]
        print("Il vous a infligé", monstre_actuel["atk"], "de dégâts")

      if hp_du_perso <= 0:
          print("\nVous avez perdu, adieu")
          sys.exit()
  level()
  if perdu == 0:
    hp_du_perso = hp_du_perso + (hp_du_perso_max / 2)
    if hp_du_perso > hp_du_perso_max:
      hp_du_perso = hp_du_perso_max
    print("vous avez ", hp_du_perso , "pv")
    invalides = 0
    while invalides == 0:
      print("\nVoulez vous aller dans le shop?")
      print("1: Oui\n2: Non")
      shop_choice = input("Choix: ")
      if shop_choice == "1":
        invalides = 1
        shop()
      elif shop_choice == "2":
        print("Vous n'êtes pas venu au shop")
        invalides = 1
      else:
        print ("donée invalide")
        invalides = 0
        continue
    
  return hp_du_perso, atk, magie, xp, hp_du_perso_max, gold

def afficher_texte_progressif(texte):
  for caractere in texte:
      sys.stdout.write(caractere)
      sys.stdout.flush()
      time.sleep(0.0250)
  print()

def histoire():
  global fuite_unlock
  global choix
  global choice
  afficher_texte_progressif("\nVotre quête débute dans les paisibles Terres de l'Aube, où la lumière règne en maître. Votre objectif est clair : retrouver le Livre des Anciens, une relique sacrée qui détient le secret de la purification du Dragon Primordial.")
  time.sleep(1)
  afficher_texte_progressif("\nAlors que vous vous aventurez paisiblement dans les Terres de l'Aube, la brise légère caresse vos joues, et le soleil projette une lumière apaisante sur le paysage. L'atmosphère s'imprègne de sérénité, mais soudain, le ciel lui-même semble s'assombrir. Une ombre massive plane au-dessus de vous, et un grondement guttural brise le calme. Une énergie maléfique émane des ténèbres, annonçant la présence imminente des gardiens corrompus du Dragon Primordial.")
  time.sleep(1)
  afficher_texte_progressif("\nVotre adversaire fonce sur vous, une silhouette sombre et menaçante qui se détache nettement contre la lumière déclinante des Terres de l'Aube. Ses yeux rougeoyants reflètent la corruption du Dragon Primordial, et son rugissement résonne dans toute la région, provoquant une réaction instinctive de votre part.\n")
  time.sleep(1)
  afficher_texte_progressif("Le combat est inévitable. Vous serrez fermement la poignée de votre arme, prêt à affronter ce gardien corrompu. Les ténèbres et la lumière se mélangent dans une danse chaotique, créant une toile de fond spectaculaire pour votre affrontement imminent.\n")
  time.sleep(1)
  faire_combat()
  time.sleep(1)
  afficher_texte_progressif("\nAprès un combat acharné, vous parvenez à repousser l'assaut de l'ombre. Votre adversaire corrompu gît désormais inerte, laissant derrière lui une atmosphère chargée de tension dissipée.")
  time.sleep(1)
  afficher_texte_progressif("Les ténèbres reculent temporairement, laissant place à la clarté retrouvée des Terres de l'Aube. Vous prenez un moment pour reprendre votre souffle, contemplant la victoire remportée.")
  time.sleep(1)
  afficher_texte_progressif("Les sommets enneigés des montagnes vous appellent, et le chemin s'annonce périlleux. Vous faites face à des épreuves divines pour mériter la bénédiction des anciens dieux, nécessaire pour renforcer vos pouvoirs en vue du combat imminent.")
  time.sleep(1)
  faire_combat()
  afficher_texte_progressif("vous venez a bout de ce monstre quand soudain un autre vous tombe dessus")
  faire_combat()
  afficher_texte_progressif("Escaladant des sommets vertigineux, surmontant des tempêtes glaciales, vous atteignez enfin le Sanctuaire des Cieux. Des divinités bienveillantes vous accordent leur bénédiction, amplifiant vos pouvoirs et vous conférant la capacité de résister aux attaques magiques.")
  time.sleep(1)
  afficher_texte_progressif("Fortifié par la puissance des anciens dieux, vous redescendez des montagnes, prêt à affronter de nouveaux défis. Les créatures gardiennes des Montagnes de l'Éternité saluent votre progression et vous accordent des regards respectueux.")
  time.sleep(1)
  afficher_texte_progressif("Avec la bénédiction des dieux, vous vous sentez prêt à affronter l'obscurité qui persiste. Vous mettez le cap vers le Marais des Ombres, où se dissimule le Portail des Ténèbres menant au repaire du Dragon Primordial.")
  afficher_texte_progressif("\nVous vous aventurez dans le Marais des Ombres, une terre lugubre où des créatures cauchemardesques rôdent dans l'obscurité. Votre objectif : trouver le mystérieux Guide des Ombres, détenteur de l'emplacement du Portail des Ténèbres.")
  time.sleep(1)
  afficher_texte_progressif("Le marais est un labyrinthe complexe, mais votre détermination guide chacun de vos pas. Vous devez éviter les pièges sournois disséminés sur votre chemin et combattre les gardiens qui protègent le portail maudit. Préparer vous à vous battre")
  faire_combat()
  faire_combat()
  faire_combat()
  time.sleep(1)
  afficher_texte_progressif("Vous découvrez enfin le Guide des Ombres, une figure énigmatique enveloppée de mystère. Il vous confie une arme ancienne capable de blesser le Dragon Primordial et vous enseigne des compétences d'infiltration essentielles.")
  time.sleep(1)
  afficher_texte_progressif("Guidé par les conseils du mystérieux guide, vous approchez du Portail des Ténèbres. L'énergie sinistre qui émane de l'entrée annonce l'ampleur de votre prochaine confrontation.")
  time.sleep(1)
  afficher_texte_progressif("Vous traversez le portail, plongeant dans l'antre du Dragon Primordial. Le Repaire du Dragon Primordial se dresse devant vous, une citadelle sombre perchée au sommet d'une montagne.")
  afficher_texte_progressif("\nVous atteignez enfin le Repaire du Dragon Primordial, une citadelle sombre perchée au sommet d'une montagne. Votre tâche est redoutable : pénétrer les défenses, affronter les sbires du dragon et finalement libérer la créature de son maléfice.")
  time.sleep(1)
  afficher_texte_progressif("La citadelle est un labyrinthe de corridors obscurs et de salles mystérieuses. Des gardiens corrompus patrouillent, protégeant les lieux des intrus. Vous devez combattre ces serviteurs du mal et déjouer les enchantements maléfiques qui tentent de vous égarer.")
  faire_combat()
  time.sleep(1)
  afficher_texte_progressif("Au fur et à mesure que vous progressez, des illusions et des épreuves mentales testent votre détermination. Chaque détour est une épreuve, mais votre volonté inébranlable vous guide à travers les épreuves.")
  faire_combat()
  faire_combat()
  time.sleep(1)
  afficher_texte_progressif("\nEnfin, vous atteignez le sommet de la citadelle, où le Dragon Primordial corrompu vous attend. Le combat est féroce, mais armé de l'arme ancienne confiée par le Guide des Ombres et des pouvoirs acquis au fil de votre quête, vous parvenez à briser le maléfice qui le consume.")
  time.sleep(1)
  afficher_texte_progressif("Le dragon, libéré de la corruption, retrouve sa bienveillance originelle. Les ténèbres reculent, laissant place à la lumière dans le royaume d'Élémentia.")
  time.sleep(1)
  afficher_texte_progressif("\nÉpuisé mais victorieux, vous contemplez le dragon désormais apaisé. Le royaume respire à nouveau dans la lumière, sauvé par votre bravoure. Acclamé comme le héros qui a restauré l'équilibre, vous recevez la gratitude du Dragon Primordial.")
  time.sleep(1)
  afficher_texte_progressif("Reconnaissant, le dragon vous accorde une bénédiction spéciale, vous érigeant ainsi parmi les légendes du royaume. Vous repartez, porteur d'une gloire éternelle et d'une paix rétablie dans le monde, vous pouvez maintenant fuir et faire des combats à volonté.")
  fuite_unlock = 1
  while choix == 0:
    print("\nvoulez vous faire des combats pour trouver des monstres rares? Y or N: ")
    choice = input()
    if choice == 'Y':
      faire_combat()
    elif choice == 'N':
      choix = 1

def menu():
    global menuchoix
    global verif
    print("Voulez-vous :\n1- Continuer une partie\n2- Créer un nouveau joueur\n3- Quitter")
    while verif == 0:
        try:
            menuchoix = int(input("Entrer votre choix : "))
            if menuchoix == 1:
                verif = 1
                histoire()
            elif menuchoix == 2:
                verif = 1
                print("Bienvenue aventurier")
            elif menuchoix == 3:
                verif = 1
                sys.exit()
            else:
                print("Donnée saisie incorrecte")
                verif = 0
        except ValueError:
            print("Donnée saise incorrecte")
            verif = 0
# menu()
            
display_player_data()