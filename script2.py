import time
from random import randint

playerClass = "none"


# Permets d'avoir un jeu qui se relance à l'infini
def playGame():
    naked = True
    global score
    global playerClass
    global healthPoint
    global base_damage
    print("Alors que vous êtes à un repas offert par un généreux noble étranger, le temps semble s'arrêter et l'obscurité s'abbat. Lorsque vous reprenez conscience, vous êtes alors dans une salle vide, en sous-vêtements. Sur la table se trouve plusieurs tenues :")
    # Le 'playerClass sera utile plus tard pour des évenements aléatoire.

    # Première boucle, choix de faction.
    while naked:
        clothes_choice = input("Des vêtements impériaux (1), des vêtements de Sombrages (2), et des vêtements d'assassin (3). Lesquels voulez vous prendre?")
        # Suivant le choix, attribution d'une classe, stats et scores
        if clothes_choice == "1": #Choix 1 : Impérial
            print("Vous enfilez les vêtements des impériaux et vous voyez les autres disparaître. Vous ne pouvez plus les retirer")
            playerClass = "imperial"
            naked = False
            score = 1
            healthPoint = 20
            base_damage = 5

        elif clothes_choice == "2": # Choix 2 : Sombrages
            print("Vous enfilez les vêtements de Sombrages et vous voyez les autres disparaître. Vous ne pouvez plus les retirer.")
            playerClass = "sombrages"
            naked = False
            score = 1
            healthPoint = 20
            base_damage = 5

        elif clothes_choice == "3": # Choix 3 : Assassin
            print("Vous enfilez les vêtements d'assassin et vous voyez les autres disparaître. Vous ne pouvez plus les retirer mais vous vous sentez plus léger.")
            playerClass = "assassin"
            score = -20
            naked = False
            healthPoint = 20
            base_damage = 10

        else : # En cas de réponse non prévue
            print("Vous n'avez pas d'autres options que 1, 2 ou 3.") 

    print("Maintenant que vous êtes habillé, trois salles s'offrent à vous.")
    showscore()

    while True: 
        while healthPoint > 0: # healthPoint > 0 permets juste de checker un game over
            roomchoice = input("Dans quelle salle voulez vous allez? 1 = Bruyante, 2 = Calme, 3 = Délabrée.")
            if roomchoice == "1": #Choix 1 : Salle Bruyante
                enter_noisy_room()
            elif roomchoice == "2": #Choix 2 : Salle calme
                enter_calm_room()
            elif roomchoice == "3": # Choix 3 : Salle Délabrée
                enter_broken_room()
            else: # En cas de réponse non valable
                print("Vous n'avez pas d'autre options que de choisir un chiffre de 1 à 3.")
        print("Vos pv sont tombés à zéro. Vous vous retrouvez au début, GAME OVER.")
        playGame() # Recommence le jeu depuis 0 en cas de game over
    

    


def showscore():
    global score
    global healthPoint
    print("Votre score est de:", score) 
    time.sleep(1)                       # Affiche simplement les pv et le score du joueur à chaque fin de salle.
    print("Vous avez",healthPoint,"pv")


# Fonction pour les combats contre les soldats dans la salle calme.
def fight_opponent():
    global score
    global base_damage                 ## Les variables sont toujours olbigées d'être en "global" pour éviter que la fonction essaye de la redéfinir 
    global healthPoint                       ## à chaque itération, et pour en garder le compte.
    action = input("Voulez vous fuir ou attaquer?")
    fleeChance = randint(1,3)
                # Test permettant de voir si le joueur peut fuir sans répercussion.
    if action.lower() == "fuir" and playerClass == "assassin" and fleeChance > 1 or action.lower() == "fuir" and fleeChance ==3:
        print("Vous avez réussi à fuir.")
        showscore()
                    # Test permettant de voir si le joueur peut fuir MAIS avec des points négatifs
    elif action.lower() == "fuir" and playerClass == "assassin" and fleeChance == 1 or action.lower() == "fuir":
        print("Vous n'avez pas réussi à fuir. L'ennemi a le temps de vous donner un coup. Vous perdez 2 pv et 3 points.")
        healthPoint = healthPoint - 2
        score = score - 3
        showscore()
        return

    elif action.lower() == "attaquer":
        damage = base_damage + 0.15*abs(score)  # La stat "base_damage" permets d'éviter que le joueur gonfle sa stat de dégat en redémarrant la boucle.
        enemy_healthPoint = 15+0.1*abs(score)      # Les stats sont définies en fonction du score du joueur pour permettre un scaling.
        enemy_damage = 1+0.05*abs(score)     # En valeur absolue pour éviter les dégats négatifs.
        time.sleep(2)
        print("L'ennemi a", enemy_healthPoint, "pv")
        time.sleep(2)

        while enemy_healthPoint > 0 and healthPoint > 0: # Permets de checker la mort du monstre ou joueur
            randomDamageChange = randint(-3,3)
            enemy_healthPoint = enemy_healthPoint - (damage+randomDamageChange)
            print("L'ennemi a maintenant",enemy_healthPoint, "pv après avoir subit", damage+randomDamageChange ,"dégats") # Affiche les pv restant et les dégats subits par l'adversaire

            if enemy_healthPoint < 1: # Mort du monstre.
                time.sleep(2)
                print("L'ennemi n'a plus de pv, vous pouvez passer et vous remportez 5 points.")
                score = score + 5
                showscore()

            else: # Si le monstre ne meurt pas après le coup, joueur prends des dégats.
                healthPoint = healthPoint - (enemy_damage+randomDamageChange)
                time.sleep(2)
                print("Vous avez prit",enemy_damage+randomDamageChange, "dégats et avez maintenant", healthPoint ,"pv") # Affiche les pv restant et les dégats subits par le joueur
        if healthPoint < 1: # Si les pv du joueurs tombent à zéro, game over.
            "GAME OVER."
            playGame()

    else: # En cas de réponse non prévue/érronée
        print("Vous ne pouvez qu'attaquer ou fuir") 
        fight_opponent() #Pourrait être une simple boucle while, relance le combat depuis le début.


# FONCTION POUR SALLES BRUYANTES
def enter_noisy_room():
    # Si la variable "score" n'est pas mise en global, erreur car la fonction essaye de redéfinir "score" à chaque itération.
    global score
    global playerClass
    global healthPoint
    rng = randint(0,100)


    if rng == 100:
        print("Vous avez trouvé un coffre! Dedans, il y a de la nourriture et des pièces!")
        score = score + 10
        healthPoint = healthPoint + 10
        showscore()
        return


    if rng in range (71, 99) and playerClass == "assassin":
        print("Alors que vous entrez dans la salle, des assassins se jettent sur vous et vous volent quelque chose")
        score = score - 1
        showscore()
        return
    
    if rng in range(71,99):
        print("Alors que vous entrez dans la salle, des assassins se jettent sur vous et vous volent quelque chose")
        score = score - 5
        showscore()
        return


    if rng in range(0, 70) and playerClass == "Assassin":
        print("Vous rencontrez des soldats")
        fight_opponent()

    elif rng in range (0, 35) and playerClass =="imperial" or rng in range(35,70) and playerClass =="sombrages": 
        # Evenement "rencontre de soldats alliés"
            print("Vous rencontrez des soldats avec la même tenue que vous. Ils vous saluent et vous donnent un peu à boire")
            healthPoint = healthPoint + 5
            print("Vous récuperez 5 pv.")
            score = score + 1
            showscore()

    else:
            print("Vous rencontrez des soldats ne portant pas le même uniforme que vous.")
            fight_opponent() # Commence la fonction de combat vue plus haut



# FONCTION POUR SALLES CALMES 
def enter_calm_room():
    # Si la variable "score" n'est pas mise en global, erreur car la fonction essaye de redéfinir "score" à chaque itération.
    global score
    global playerClass
    global healthPoint
    rng = randint(0, 100)
    

    if rng in range(0, 40) and playerClass == "assassin": 
            print("Vous remarquez des Assassins tapis dans les ombres. Cependant, ils ne vont ont pas remarqué. Vous en profitez pour subtiliser quelques pièces et une potion de vie.")
            score = score + 5
            time.sleep(1)
            print("Vous récuperez 10 pv.")
            healthPoint = healthPoint + 10
            showscore()
    
    elif rng in range(0, 40):
            print("Alors que mettez pieds dans la salle, une silouhette sombre se faufile derrière vous et vous vole quelques pièces.")
            score = score - 3
            showscore()

    elif rng in range (41, 60) and playerClass == "assassin":
            print("La salle est remplie d'animaux endormi! Cependant, vos pas sont si légers que vous pouvez passez sans être remarqué.")
            time.sleep(1)
            print("Vous trouvez quelques pièces et une pomme, ce qui vous rends 2pv.")
            score = score + 5
            healthPoint = healthPoint + 2
            showscore()

    elif rng in range(41, 60):
            print("Alors que vous entrez dans la salle, les animaux se réveillent et vous attaquent ! Par chance, vous réussissez à vous en sortir, quelques peu épuisé.")
            score = score + 1
            healthPoint = healthPoint - 3
            showscore()

    else: 
        print("La salle est vide. C'était une perte de temps.")
        showscore()


# FONCTION POUR SALLES DELABREE
def enter_broken_room():
     # Si la variable "score" n'est pas mise en global, erreur car la fonction essaye de redéfinir "score" à chaque itération.
    global score
    global playerClass
    global healthPoint
    global base_damage
    rng = randint (0, 100)

    if rng in range (90, 101) and playerClass == "assassin":
        print("Vous arrivez dans la salle délabrée et elle se met soudainement à rajeunir et se ranger. Le noble qui avait organisé la fête apparaît soudainement. Votre tenue n'a pas l'air de lui plaîre. La terre gronde alors qu'il se prépare à vous attaquer.")
        fight_boss() #Lance la fonction du combat de boss.
        return

    if rng in range(0,30):
        print("Vous avez trouvé un coffre contenant de nombreuses pièces d'or et une épée avec de meilleurs stats que la votre!")
        score = score + 20
        base_damage = base_damage + randint(1,5)

    elif rng in range(30,60):
        print("La salle est vide, c'était une perte de temps.")

    elif rng in range (60,90):
        print("Alors que vous avancez avec attention, vous tombez dans un trou! Vous sortez avec peine de ce trou, bien plus léger.")
        score = score - 5
        
    elif rng in range (90, 101) and score < 100:
        print("Une silouhette se dessine au loin, au fond de la salle. Vous n'osez pas l'approcher car vos sens sont en alerte, sans que vous ne sachiez pourquoi.")
        print("Revenez quand vous aurez atteint la barre des 100, aventurier.")
    
    else:
        print("Alors que la salle délabrée se restore, le noble qui avait organisé la fête apparaît au milieu de la salle, tel un fantôme. Après vous avoir regardé pendant quelques instants, il rigole et vous félicite de votre travail dans son domaine")
        print("Il vous dit que vous avez bien travaillé et que vous pouvez maintenant vous reposer.")
            # Permet d'éviter que le joueur dise "non" même s'il écrit mal son "Y".
        while True:
            leave = input("Voulez vous recommencer à zéro? Y/N")

            if leave.lower() == "y":
                playGame() # Appelle la fonction de début de partie, remets tout à zéro.

            elif leave.lower() == "n":# Si le joueur veut continuer sur sa lancée.
                print("Si c'est ce que tu veux, très bien. Continue ton aventure.")
                print("Il vous soigne et vous donne un petit cadeau. Vous gagnez 20hp.")
                healthPoint = healthPoint + 20
                score = score + 40
                showscore()
                return

            else: # Au cas où une réponse invalide est rentrée, permets de relancer le joueur et lui dire quoi répondre.
                print("Le noble vous demande de repeter, n'étant pas sûr d'avoir bien entendu votre réponse.")
                time.sleep(1)
                print("Vous ne pouvez répondre que 'Y' et 'N'.")
            
    showscore()


# Fonction pour le combat de boss (noble vs assassin)
def fight_boss():
    global score
    global base_damage
    global healthPoint
    global playerClass
    action = input("Voulez vous implorer le pardon du noble ou vous battre?")
    
    if action.lower() == "implorer": # Si le joueur choisi d'implorer, relance le jeu depuis le début.
        print("C'est culloté d'implorer mon pardon après avoir fait tant de victimes.")
        time.sleep(1)
        print("Mais soit, tu vas retourner au début de ton aventure. Ne refait pas la même erreur.")
        playGame()

    elif action.lower() == "battre":
        damage = 0.15*abs(score) + base_damage # Permets de scale les dégats du joueur en fonction de son score, comme dans fight_opponent()
        print("Le noble se prépare, il ne sera pas un ennemi comme les autres.")
        enemy_healthPoint = 25 + 0.75*abs(score) # Permets le scale du boss pour qu'il ne soit pas "trop facile" si le joueur le rencontre tard
        enemy_damage = 5 + 0.35*abs(score) # Encore du scale de boss.
        time.sleep(1)
        print("L'ennemi a", enemy_healthPoint, "pv")

        while enemy_healthPoint > 0 and healthPoint > 0:
            randomDamageChange = randint(-3, 3)
            enemy_healthPoint = enemy_healthPoint - (damage + randomDamageChange)
            time.sleep(2)
            print("L'ennemi a maintenant",enemy_healthPoint, "pv après avoir subit", (damage+randomDamageChange) ,"dégats") # Affiche les pv restant et les dégats subits du boss

            if enemy_healthPoint < 1: # Mort du boss
                time.sleep(1)
                print("Le noble tombe à genoux, à bout de force. Il grogne alors quelques mots.")
                time.sleep(1)
                print("- 'Je reviendrai...'")
                time.sleep(1)
                score = score + 50
                healthPoint = healthPoint + 40
                showscore()
                return


            else:
                healthPoint = healthPoint - (enemy_damage+randomDamageChange)
                time.sleep(2)
                print("Vous avez prit",enemy_damage+randomDamageChange, "dégats et avez maintenant", healthPoint ,"pv") # Affiche les pv restant et les dégats subits par le joueur

        if healthPoint < 1: # Si le joueur perds.
            print("Le noble se moque de vous et vous rends votre vie. Bien que le game over soit évité, vous perdez tout vos points.")
            healthPoint = 20
            score = 0
            showscore()
            return

    else: # En cas de réponse non prévue, permets d'aiguiller le joueur sur ce qu'il doit écrire.
        print("Vous ne pouvez que vous 'battre' ou 'implorer' la merci du noble.")
        fight_boss()

while True: # Lance simplement le jeu.
    playGame()





