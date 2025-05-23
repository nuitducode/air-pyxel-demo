# on rajoute random
import pyxel, random

class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.vaisseau_x = 60
        self.vaisseau_y = 60

        # vies
        self.vies = 10000

        # initialisation des tirs
        self.tirs_liste = []

        # initialisation des ennemis
        self.ennemis_liste = []

        # initialisation des explosions
        self.explosions_liste = []

        # chargement des images
        pyxel.load("res.pyxres")

        pyxel.run(self.update, self.draw)


    def deplacement(self):
        """déplacement avec les touches de directions"""

        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.vaisseau_x<120:
            self.vaisseau_x += 2
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.vaisseau_x>0:
            self.vaisseau_x += -2
        if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.vaisseau_y<120:
            self.vaisseau_y += 2
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.vaisseau_y>0:
            self.vaisseau_y += -2


    def tirs_creation(self):
        """création d'un tir avec la barre d'espace"""

        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            self.tirs_liste.append([self.vaisseau_x, self.vaisseau_y-8, 'single'])
        if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
            self.tirs_liste.append([self.vaisseau_x, self.vaisseau_y-8, 'multi'])
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_X):
            self.tirs_liste.append([self.vaisseau_x, self.vaisseau_y-8, 'missile'])
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_Y):
            self.tirs_liste.append([self.vaisseau_x, self.vaisseau_y-8, 'love'])
            
    def tirs_deplacement(self):
        """déplacement des tirs vers le haut et suppression quand ils sortent du cadre"""

        for tir in  self.tirs_liste:
            tir[1] -= 1
            if  tir[1]<-8:
                self.tirs_liste.remove(tir)


    def ennemis_creation(self):
        """création aléatoire des ennemis"""

        # un ennemi par seconde
        if (pyxel.frame_count % 30 == 0):
            self.ennemis_liste.append([random.randint(0, 120), 0])


    def ennemis_deplacement(self):
        """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""              

        for ennemi in self.ennemis_liste:
            ennemi[1] += 1
            if  ennemi[1]>128:
                self.ennemis_liste.remove(ennemi)


    def vaisseau_suppression(self):
        """disparition du vaisseau et d'un ennemi si contact"""

        for ennemi in self.ennemis_liste:
            if ennemi[0] <= self.vaisseau_x+8 and ennemi[1] <= self.vaisseau_y+8 and ennemi[0]+8 >= self.vaisseau_x and ennemi[1]+8 >= self.vaisseau_y:
                self.ennemis_liste.remove(ennemi)
                self.vies -= 1
                # on ajoute l'explosion
                self.explosions_creation(self.vaisseau_x, self.vaisseau_y)


    def ennemis_suppression(self):
        """disparition d'un ennemi et d'un tir si contact"""

        for ennemi in self.ennemis_liste:
            for tir in self.tirs_liste:
                if ennemi[0] <= tir[0]+8 and ennemi[0]+8 >= tir[0] and ennemi[1]+8 >= tir[1]:
                    self.ennemis_liste.remove(ennemi)
                    self.tirs_liste.remove(tir)
                    # on ajoute l'explosion
                    self.explosions_creation(ennemi[0], ennemi[1])


    def explosions_creation(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])


    def explosions_animation(self):
        """animation des explosions"""
        for explosion in self.explosions_liste:
            explosion[2] +=1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)


    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.deplacement()

        # creation des tirs en fonction de la position du vaisseau
        self.tirs_creation()

        # mise a jour des positions des tirs
        self.tirs_deplacement()

        # creation des ennemis
        self.ennemis_creation()

        # mise a jour des positions des ennemis
        self.ennemis_deplacement()

        # suppression des ennemis et tirs si contact
        self.ennemis_suppression()

        # suppression du vaisseau et ennemi si contact
        self.vaisseau_suppression()

        # evolution de l'animation des explosions
        self.explosions_animation()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)


        # si le vaisseau possede des vies le jeu continue
        if self.vies > 0:

            # affichage des vies            
            pyxel.text(5,5, 'VIES:'+ str(self.vies), 7)

            # vaisseau (carre 8x8)
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 0, 0, 8, 8)

            # tirs
            for tir in self.tirs_liste:
                if (tir[2] == 'single'):
                    pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)
                if (tir[2] == 'multi'):
                    pyxel.blt(tir[0], tir[1], 0, 8, 8, 8, 8)
                if (tir[2] == 'missile'):
                    pyxel.blt(tir[0], tir[1], 0, 8, 16, 8, 8)  
                if (tir[2] == 'love'):
                    pyxel.blt(tir[0], tir[1], 0, 0, 16, 8, 8) 
                    
            # ennemis
            for ennemi in self.ennemis_liste:
                pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8, 8, 8)

            # explosions (cercles de plus en plus grands)
            for explosion in self.explosions_liste:
                pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)


        # sinon: GAME OVER
        else:

            pyxel.text(50,64, 'GAME OVER', 7)

Jeu()