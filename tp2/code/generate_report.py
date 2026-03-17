#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from report_utils import (
    html_document,
    section,
    subsection,
    figure,
    formula_box,
    save_report,
    figure_row,
    figure_pile
)

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

OUTPUT_HTML = "../web/index.html"
IMAGES_PATH = "images"   # chemin relatif depuis index.html

# ------------------------------------------------------------------
# Section : Partie 0 - Accentuation
# ------------------------------------------------------------------

def build_part0_section():
    
    content = ""

    # Description théorique
    content += subsection(
        "Méthode utilisée",
        """
        <p>
        Nous avons appliqué la technique d'accentuation par <b>Sharpening</b>.
        L'image est d'abord filtrée par un filtre gaussien (passe-bas),
        puis les hautes fréquences sont extraites par soustraction.
        </p>
        """
    )

    

    # Résultats côte à côte
    content += subsection("Résultats")

    # Ganvié
    content += figure_row([
        (f"{IMAGES_PATH}/ganvie2.jpg", "Image originale - Ganvié"),
        (f"{IMAGES_PATH}/ganvie1_sharpened.jpg", "Image accentuée - Ganvié"),
    ])

    # Quebec
    content += figure_row([
        (f"{IMAGES_PATH}/quebec1.jpeg", "Image originale - Quebec1"),
        (f"{IMAGES_PATH}/quebec1_sharpened.jpg", "Image accentuée - Quebec1"),
    ])

    content += subsection(
        "Analyse",
        """
        <p>
        L'accentuation améliore la perception des contours et des détails
        fins. Toutefois, un α trop élevé peut générer des halos visibles
        autour des transitions abruptes.
        </p>
        """
    )

    return section("Partie 0 – Réchauffement : Accentuation", content, icon="🔥")


# ------------------------------------------------------------------
# Section : Partie 1 - Images hybrides
# ------------------------------------------------------------------

def build_part1_section():
    
    content = ""

    # --------------------------------------------------------------
    # Introduction
    # --------------------------------------------------------------

    
    # --------------------------------------------------------------
    # Méthodologie
    # --------------------------------------------------------------

    # --------------------------------------------------------------
    # Résultat Einstein - Marilyn
    # --------------------------------------------------------------

    content += subsection("Résultat : Einstein & Marilyn")

    content += figure_row([
        (f"{IMAGES_PATH}/Marilyn_Monroe.png", "Image originale – Marilyn"),
        (f"{IMAGES_PATH}/combined_marylin_einstein.jpg", "Image hybride"),
        (f"{IMAGES_PATH}/Albert_Einstein.png", "Image originale – Einstein"),
    ])

    # --------------------------------------------------------------
    # Résultat Jeune - Vieux
    # --------------------------------------------------------------

    content += subsection("Résultat : Jeune & Vieux")

    content += figure_row([
        (f"{IMAGES_PATH}/jeune1_gray.png", "Image originale – Jeune"),
        (f"{IMAGES_PATH}/combined_jeune_vieux.jpg", "Image hybride"),
        (f"{IMAGES_PATH}/vieux_gray.png", "Image originale – Vieux"),
    ])
    content += subsection(
        "Description et analyse des résultats",
        """
        <p>
        À courte distance, les détails fins (rides, moustache) d’Einstein,
        correspondant aux hautes fréquences, dominent la perception.
        À grande distance, ces détails disparaissent et la structure
        globale du visage de Marilyn, issue des basses fréquences,
        devient prédominante.

        L'image de notre choix correspond à celle d’un jeune et d’un vieux,
        tous les deux barbus.
        À faible distance, on voit le vieux et, à distance éloignée,
        on voit le jeune.
        </p>

        <p>
        Les résultats que nous obtenons semblent satisfaisants pour nos
        deux paires d’images.
        Ces résultats sont obtenus en faisant un choix des fréquences de
        coupure proportionnel à la taille des images.
        </p>
        """
)


    # --------------------------------------------------------------
    # Analyse fréquentielle
    # --------------------------------------------------------------

    content += subsection("Analyse fréquentielle")

    # FFT originales
    content += figure_row([
        (f"{IMAGES_PATH}/fft_jeune.png", "FFT – Jeune"),
        (f"{IMAGES_PATH}/fft_vieux.png", "FFT – Vieux"),
    ])

    # FFT filtrées
    content += figure_row([
        (f"{IMAGES_PATH}/fft_low.png", "FFT – Passe-bas"),
        (f"{IMAGES_PATH}/fft_high.png", "FFT – Passe-haut"),
    ])

    # FFT hybride
    content += figure_row([
        (f"{IMAGES_PATH}/fft_hybrid.png", "FFT – Image hybride"),
    ])

    

    content += subsection(
        "Interprétation fréquentielle",
        """
        <p>
        L'image sur laquelle on applique le filtre passe-bas est très lumineuse au centre,
        tandis que celle sur laquelle on applique le filtre passe-haut présente une énergie
        lumineuse plutôt bien répartie sur l’ensemble de l’image.

        Lorsque l’on applique le filtre passe-bas à l’image, on obtient un spectre
        presque noir sauf au centre, ce qui indique que seules les basses fréquences
        sont conservées.

        En revanche, le filtre passe-haut supprime cette énergie centrale et conserve
        les composantes périphériques correspondant aux hautes fréquences.

        Le filtre passe-bas concentre donc l’énergie autour du centre du spectre,
        indiquant la conservation des basses fréquences, tandis que le filtre
        passe-haut met en évidence les détails fins.

        L’image hybride présente une superposition des deux structures spectrales,
        confirmant ainsi une séparation fréquentielle efficace.
        </p>
        """
)

    

    # --------------------------------------------------------------
    # Credit sup
    # --------------------------------------------------------------

    content += subsection(
        "Crédit supplémentaire",
        """
        <p> 

        J'ai fait la composition d'image hybride sur une photo de moi et de mon amie.
        La composition hybride fonctionne sur ces images

        </p>
        """
    )

    content += figure_row([
        (f"{IMAGES_PATH}/julci_gray.png", "Image de mon amie"),
        (f"{IMAGES_PATH}/combined_julci_tadagbe.jpg", "Image hybride"),
        (f"{IMAGES_PATH}/tadagbe_gray.png", "Image de moi"),
    ])

    return section("Partie 1 – Images hybrides", content, icon="🌀")


# ------------------------------------------------------------------
# Section : Partie 2 - Piles gaussiennes et laplaciennes
# ------------------------------------------------------------------

def build_part2_section():
    
    content = ""

    # --------------------------------------------------------------
    # Application : Dali
    # --------------------------------------------------------------

    content += subsection("Application : Lincoln et Gala – Salvador Dali")

    content += "<p>Pile gaussienne :</p>"

    content += figure_pile(
    f"{IMAGES_PATH}/pile_gauss_lincoln.jpg",
    "Pile Gaussienne",
    style="width: 80%;"
    )

    content += "<p>Pile laplacienne :</p>"

    content += figure_pile(
    f"{IMAGES_PATH}/pile_laplace_lincoln.jpg",
    "Pile Laplacienne",
    style="width: 80%;"
)


    # --------------------------------------------------------------
    # Analyse de l'image hybride
    # --------------------------------------------------------------

    content += subsection("Analyse des piles sur l'image hybride")

    content += figure_pile(
    f"{IMAGES_PATH}/pile_gauss_combined_jeune_vieux.jpg",
    "Pile gaussienne – hybride",
    style="width: 85%;")

    content += figure_pile(
    f"{IMAGES_PATH}/pile_laplace_combined_jeune_vieux.jpg",
    "Pile laplacienne – hybride",
    style="width: 85%;")

    content += subsection(
        "Description et commentaire des résultats",
        """
        <p>
        Dans les piles gaussiennes obtenues, on voit que on perd les hautes frequeences
        a mesure que on augment en profonfeur de notre pile et nos images deviennent de plus en plus floue.
        Plus en augmente dnas notre pile gausinne, plus on aplique un bruit plus large. Ce qui explique ces observations.

        </p>
        <p>
        La pile laplacienne permet une décomposition multi-échelle de l’image.
        Pour les petites valeurs de σ, les niveaux mettent en évidence les détails fins et les hautes fréquences.
        Pour des valeurs intermédiaires, les contours principaux et les structures du visage deviennent prédominants.
        Enfin, pour les grandes valeurs de σ, seules les structures globales subsistent, correspondant aux basses fréquences.
        </p>

        <p>
        Pour ce qui est de la pile laplacienne de l'image hybride, elle est quasi uniforme au début.
        Cela s'explique par le fait que les tout premiers niveaux de la décomposition
        contiennent uniquement les très hautes fréquences, dont l’énergie est relativement faible.
        Ces composantes fines produisent donc un contraste peu marqué, ce qui donne
        une apparence presque uniforme.
        </p>
        """
    )

    return section("Partie 2 – Piles gaussiennes et laplaciennes", content, icon="📚")

# ------------------------------------------------------------------
# Section : Partie 3 - Mélange multi-résolution (piles gauss/laplace)
# ------------------------------------------------------------------

def build_part3_section():
    content = ""

    # --------------------------------------------------------------
    # Intro + méthode
    # --------------------------------------------------------------
    content += subsection(
        "Principe du mélange multi-résolution",
        """
        <p>
        Nous réalisons un mélange d’images à l’aide de <b>piles gaussiennes</b> et
        <b>laplaciennes</b>. L’idée est de décomposer chaque image
        en bandes de fréquences (pile laplacienne), puis de combiner ces bandes selon une
        version floutée du masque (pile gaussienne du masque).
        </p>
        <p>
        Cette approche évite les discontinuités de couleur/texture qu’on obtient avec un collage
        direct et produit une transition plus naturelle à la frontière du masque.
        </p>
        """
    )

    content += """
        <p>
        Dans nos expériences, la pile gaussienne est obtenue en appliquant des flous gaussiens
        de plus en plus larges (σ croissant) à partir de l’image originale (résolution constante).
        </p>
    """

    # --------------------------------------------------------------
    # (5%) Pommage : Apple / Orange
    # --------------------------------------------------------------
    content += subsection("Résultat 1 – « Pommage »")
    content += """
        <p>
        Nous reproduisons l’exemple classique « apple/orange » : le masque est une
        séparation verticale (moitié gauche / moitié droite). Le mélange multi-résolution
        permet une transition douce au lieu d’une bordure nette.
        </p>
    """
    
    content += figure_pile(
        f"{IMAGES_PATH}/pommange.jpg",
        "Résultat – Pommage",
        style="width: 70%;"
    )

    # --------------------------------------------------------------
    # (10%) Masque irrégulier (comme fig.8 de l’article)
    # --------------------------------------------------------------
    content += subsection("Résultat 2 – Mélange avec masque irrégulier")
    content += """
        <p>
        Nous utilisons un masque irrégulier afin d’illustrer l’intérêt du blending
        multi-résolution sur des frontières complexes. Il s’agit d’une photo de
        Montréal dans laquelle nous insérons un œil au centre de l’image.
        Le lissage gaussien appliqué au masque permet d’éviter les transitions
        brusques et d’assurer une intégration visuellement réaliste.
        </p>
    """
    
    content += figure_pile(
        f"{IMAGES_PATH}/oeil_montreal.jpg",
        "Résultat – Masque irrégulier",
        style="width: 70%;"
    )
    content += subsection(
        "Commentaire (masque irrégulier)",
        """
        <p>
        Le mélange par bandes réduit les artefacts au contour du masque : les détails fins
        (hautes fréquences) restent localisés près de leur source, tandis que les structures
        larges (basses fréquences) assurent une transition globale plus douce.
        </p>
        """
    )

    # --------------------------------------------------------------
    # (5%) Vos propres photos
    # --------------------------------------------------------------
    content += subsection("Résultat 3 – Mélange sur nos propres photos")
    content += """
    <p>
    Ce résultat utilise nos propres photos. 
    On voit une image du village lacustre de Ganvié au Bénin ainsi qu’une
    photo de moi prise au Canada. J’ai essayé de m’insérer dans l’image
    du village lacustre comme si je restais en équilibre sur l’eau.
    Le rendu n’est pas parfait, mais les objectifs sont globalement atteints.
    </p>
    """
    
    content += figure_pile(
        f"{IMAGES_PATH}/tadagbe_ganvie.jpg",
        "Résultat – Vos propres photos",
        style="width: 70%;"
    )

    # --------------------------------------------------------------
    # (10%) Illustration détaillée du procédé (Fig.10)
    # -> pour TON résultat préféré
    # --------------------------------------------------------------
    content += subsection("Illustration détaillée du procédé – Résultat préféré")
    content += """
        <p>
        La figure suivante illustre le procédé en détail, à la manière de la figure 10
        de Burt & Adelson (1983) : contributions par bandes (piles laplaciennes), combinaison
        par masque flouté à chaque niveau, puis somme progressive menant à l’image finale.
        </p>
    """
    content += figure_pile(
        f"{IMAGES_PATH}/detail_compose.jpg",
        "Illustration détaillée (type Fig.10) – résultat préféré",
        style="width: 92%;"
    )

    # # --------------------------------------------------------------
    # # Conclusion / synthèse
    # # --------------------------------------------------------------
    # content += subsection(
    #     "Synthèse",
    #     """
    #     <p>
    #     Les résultats montrent que le blending multi-résolution est particulièrement utile
    #     lorsque le masque comporte des contours complexes : la transition devient plus naturelle
    #     qu’un collage direct. Les limites restantes proviennent surtout des différences
    #     d’illumination et de perspective entre les images sources (ex. ombres).
    #     </p>
    #     """
    # )

    return section("Partie 3 – Mélange multi-résolution", content, icon="🧩")



# ------------------------------------------------------------------
# Construction complète du rapport
# ------------------------------------------------------------------

def build_full_report():
    
    content = ""
    content += build_part0_section()
    content += build_part1_section()
    content += build_part2_section()
    content += build_part3_section()

    content += section(
        "Sources des images",
        """
        <p>
        <a href="https://commons.wikimedia.org/wiki/File:Ganvie2.jpg">LIEN_1</a><br>
        <a href="https://www.istockphoto.com/fr/search/2/image-film?phrase=oeil&tracked_gsrp_landing=https%3A%2F%2Fwww.istockphoto.com%2Ffr%2Fphotos%2Foeil">LIEN_2</a><br>
        <a href="https://fr.freepik.com/photos/jeune-barbu#uuid=e64d3f64-b8a9-43ee-ab4a-d404aa1a6616">LIEN_3</a><br>
        <a href="https://fr.freepik.com/photos-vecteurs-libre/vieil-homme-moustache-barbe">LIEN_4</a>
        </p>
        """
    )

    content += section(
        "Utilisation de LLM",
        """
        <p>
        Un modèle de langage (LLM) a été utilisé comme outil d’assistance
        pour clarifier certains aspects théoriques et méthodologiques du projet.
        Les requêtes pertinentes incluent notamment :
        </p>

        <ul>
            <li>« Comment obtenir automatiquement un masque binaire pour délimiter
            la tête à partir d’une image ? »</li>

            <li>« Normalement, on construit la pyramide laplacienne et on additionne, non ? »</li>

            <li>« Nous utilisons des piles (et non des pyramides) : est-ce correct
            d’additionner directement les niveaux ? »</li>

            <li>« Comment produire une illustration détaillée du procédé,
            comme la figure 10 de l’article de Burt & Adelson (1983) ? »</li>

            <li>« Génère-moi le code pour afficher les images intermédiaires
            de la composition d’images. »</li>

            <li>« Donne-moi le code pour générer le masque. »</li>

            <li>« Aide-moi à structurer la partie 3 du rapport
            (pommage, masque irrégulier, photos personnelles, illustration détaillée). »</li>
        </ul>

        <p>
        Le modèle a servi uniquement d’assistance conceptuelle et rédactionnelle.
        L’implémentation, les expérimentations, le choix des paramètres
        et l’analyse des résultats ont été réalisés de manière autonome.
        </p>
        """
)



    html = html_document(
        title="TP2 – On s'amuse en fréquences",
        subtitle="Accentuation & Images hybrides",
        icon="📸",
        content=content,
        accent_color="#ff9800"
    )

    return html


if __name__ == "__main__":
    html = build_full_report()
    save_report(html, OUTPUT_HTML)
