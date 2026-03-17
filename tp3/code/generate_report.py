#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from report_utils import (
    html_document,
    section,
    subsection,
    figure_row,
    figure_pile,
    save_report,
    table,
    algorithm_box,
)

# =========================================================
# Helpers HTML
# =========================================================

def paragraph(text):
    return f'''
    <p style="line-height:1.75; color:#dddddd; font-size:1.06em; margin: 12px 0;">
        {text}
    </p>
    '''

def quote(text):
    return f'''
    <div style="
        margin:18px 0;
        padding:14px 18px;
        border-left:4px solid #ffb300;
        background-color:rgba(255,255,255,0.05);
        font-style:italic;
        color:#f2f2f2;
        line-height:1.7;">
        {text}
    </div>
    '''


def video(src, caption="", width="80%"):
    caption_html = (
        f'<div style="margin-top:8px; font-style:italic; color:#bbbbbb;">{caption}</div>'
        if caption else ""
    )
    return f"""
    <div style="text-align:center; margin:25px 0;">
        <video controls style="width:{width}; border-radius:10px; box-shadow:0 4px 20px rgba(0,0,0,0.35);">
            <source src="{src}" type="video/mp4">
            Votre navigateur ne supporte pas la lecture vidéo.
        </video>
        {caption_html}
    </div>
    """


def bullet_list(items):
    html = '<ul style="line-height:1.8; color:#dddddd; font-size:1.04em;">'
    for item in items:
        html += f"<li>{item}</li>"
    html += "</ul>"
    return html


# =========================================================
# Main report generation
# =========================================================

def generate_report():
    """
    Génère le rapport HTML du TP3.
    Ce script est supposé être exécuté depuis tp3/code/
    et génère le rapport dans tp3/web/index.html
    """

    output_html = os.path.join("..", "web", "index.html")

    # =====================================================
    # PARAMÈTRES
    # =====================================================

    student_name = "Tadagbé Dhossou"

    # Vidéo principale
    main_video = "../video/morph_second.mp4"

    # # Vidéos supplémentaires
    

    friend_videos = [
    {
        "title": "Morphing entre mon ami Vianney et moi",
        "src": "../resultats/morph_vianney_tadagbe.mp4",

        "img1": "images/vianney.jpg",
        "img2": "images/tadagbe.jpg",

        "tri1": "images/triangulation_vianney.jpg",
        "tri2": "images/triangulation_tadagbe.jpg",

        "caption1": "Photo de Vianney",
        "caption2": "Ma photo",
        "tri_caption1": "Triangulation sur l’image de Vianney",
        "tri_caption2": "Triangulation sur ma photo",

        "discussion": (
            "Cette animation n’est pas parfaite, mais le résultat reste tout de même intéressant. "
            "En observant les triangles obtenus, on remarque qu’une rotation importante est nécessaire "
            "pour passer d’une image à l’autre. Cela se ressent dans la vidéo par un léger effet de "
            "tourbillon lors de la transition. "
            "Un autre facteur qui influence la qualité du rendu est que les deux photos ont été prises "
            "dans la même salle, mais à des endroits différents. Par exemple, un sac apparaît à côté de "
            "moi sur l’une des images alors qu’il n’est pas présent sur l’autre. Cela crée une certaine "
            "incohérence dans la transition. "
            "Enfin, l’arrière-plan n’est pas parfaitement blanc ni uniforme, ce qui affecte également "
            "la qualité visuelle du morphing."
        ),
    },
    {
        "title": "Morphing entre mon ami Jospin et moi",
        "src": "../resultats/morph_lolo_jospin.mp4",

        "img1": "images/jospin.jpg",
        "img2": "images/lolo.jpg",

        "tri1": "images/triangulation_jospin.jpg",
        "tri2": "images/triangulation_lolo.jpg",

        "caption1": "Photo de Jospin",
        "caption2": "Ma photo",
        "tri_caption1": "Triangulation sur l’image de Jospin",
        "tri_caption2": "Triangulation sur ma photo",

        "discussion": (
            "Cette animation correspond à un morphing de visage. La particularité de cet exemple "
            "est que les deux images sources proviennent d’une seule et même image de départ. "
            "L’image originale utilisée est montrée ci-dessous.<br><br>"

            "<div style='text-align:center;'>"
            "<img src='../web/images/lolo_jojo.jpg' style='width:420px; max-width:90%; border-radius:10px;'>"
            "</div><br>"

            "J’ai recadré cette image pour obtenir mes deux images sources. "
            "Les points d’intérêt que j’ai sélectionnés se trouvent uniquement sur les visages. "
            "Le morphing entre les visages fonctionne relativement bien, mais comme je n’ai pas "
            "placé d’autres points dans l’arrière-plan, on observe un léger effet de ghosting. "

            "Ce que je trouve intéressant est que la transformation produit un petit effet de "
            "translation, car les deux visages proviennent d’une même image originale et il faut "
            "donc effectuer un déplacement pour passer d’un visage à l’autre."
        ),
}
]


    object_videos = [
        {
            "title": "Morphing d'objets : mes deux tasses préférées",
            "src": "../resultats/morph_objets.mp4",

            "img1": "images/ia.jpg",
            "img2": "images/noir.jpg",

            "tri1": "images/triangulation_ia.jpg",
            "tri2": "images/triangulation_noir.jpg",

            "caption1": "Tasse 1",
            "caption2": "Tasse 2",
            "tri_caption1": "Triangulation sur la tasse 1",
            "tri_caption2": "Triangulation sur la tasse 2",

            "discussion": (
                "Cette animation illustre l’application de la même méthode à des objets, en l’occurrence deux tasses d’eau. "
                "Le rendu est presque parfait, ce qui s’explique par le fait que les deux images présentent des structures très similaires. "
                "Le principal problème rencontré dans ce cas est la lenteur de l’algorithme : malgré l’utilisation d’environ 38 points "
                "autour de chaque objet, le temps de calcul est resté relativement élevé. "
                "Cela s’explique notamment par la résolution élevée des images, qui ont été prises avec mon téléphone "
                "et mesurent environ 1282 × 1704 pixels."
            ),
        }
    ]


    # Images principales
    image_main_1 = "images/19_Roberge_Alexis.jpg"
    image_main_2 = "images/20_Dhossou_Tadagbé.jpg"

    # Mets True seulement si tu as vraiment généré ces images
    show_debug_figures = False

    points_img1 = "images/points_main_1.png"
    points_img2 = "images/points_main_2.png"
    triangulation_img = "images/triangulation_main.png"

    frame_samples = [
        ("images/frame_00001.png", "Début de la séquence"),
        ("images/frame_00025.png", "Déformation initiale"),
        ("images/frame_00050.png", "Image intermédiaire"),
        ("images/frame_00075.png", "Transition avancée"),
        ("images/frame_00100.png", "Fin de la séquence"),
    ]

    # =====================================================
    # CONTENU
    # =====================================================

    content = ""

    # -----------------------------------------------------
    # 1. Introduction
    # -----------------------------------------------------
    intro_html = ""
    intro_html += paragraph(
        "Ce travail porte sur la métamorphose d’images à l’aide de correspondances de points. "
        "L’objectif principal était de produire une séquence vidéo transformant progressivement "
        "une image vers une autre, puis d’appliquer la même approche à plusieurs "
        "autres paires d’images."
    )
    intro_html += paragraph(
        "L’approche utilisée repose sur trois idées principales : la sélection de points "
        "correspondants, une triangulation de Delaunay calculée sur la moyenne des points, "
        "puis un morphing triangle par triangle à l’aide de transformations affines et d’un "
        "fondu progressif des couleurs."
    )
    intro_html += paragraph(
        "Dans ce rapport, je présente d’abord l’algorithme utilisé, puis la vidéo principale "
        "demandée par l’énoncé, suivie de trois animations supplémentaires et d’une discussion "
        "sur la qualité des résultats."
    )

    content += section("Introduction", intro_html, icon="📝")

    # -----------------------------------------------------
    # 2. Algorithme
    # -----------------------------------------------------
    algo_html = ""

    algo_html += subsection("Vue d’ensemble")
    algo_html += bullet_list([
        "Lecture des deux images et des points correspondants.",
        "Calcul d’une triangulation de Delaunay sur la moyenne des points.",
        "Pour chaque trame, interpolation des points vers une géométrie intermédiaire.",
        "Pour chaque triangle, calcul d’une transformation affine inverse vers les deux images originales.",
        "Échantillonnage des couleurs dans les deux images, puis fondu pondéré pour construire l’image intermédiaire.",
        "Sauvegarde des trames et assemblage en vidéo."
    ])

    algo_html += subsection("1. Définition des correspondances")
    algo_html += paragraph(
        "Les points d’intérêt ont été définis manuellement sur les deux images. "
        "Ils incluent les principales structures du visage, notamment le contour, les yeux, "
        "les sourcils, le nez, la bouche ainsi que des points sur les bordures de l’image afin "
        "de mieux contrôler l’arrière-plan."
    )

    algo_html += subsection("2. Triangulation")
    algo_html += paragraph(
        "Une triangulation de Delaunay a été calculée sur la moyenne des deux ensembles de points. "
        "Cette triangulation est conservée fixe pendant toute la séquence afin d’éviter les changements "
        "abrupts de structure entre les trames."
    )

    algo_html += subsection("3. Morphing")
    algo_html += paragraph(
        "Pour une trame donnée, une forme intermédiaire est obtenue par interpolation linéaire "
        "des points de contrôle. Ensuite, pour chaque triangle, une transformation affine est "
        "calculée entre le triangle intermédiaire et les triangles correspondants dans les deux "
        "images source."
    )
    algo_html += paragraph(
        "Le remplissage de l’image intermédiaire est effectué par transformation inverse : "
        "pour chaque pixel situé dans un triangle de l’image intermédiaire, on remonte vers "
        "sa position dans chaque image source, on interpole sa couleur, puis on combine les "
        "deux couleurs selon un facteur de fondu."
    )


    content += section("Algorithme de métamorphose", algo_html, icon="⚙️")

    # -----------------------------------------------------
    # 3. Résultat principal
    # -----------------------------------------------------
    main_html = ""

    main_html += subsection("Images utilisées")
    main_html += figure_row([
        (image_main_1, "Image source 1"),
        (image_main_2, "Image source 2"),
    ])

    if show_debug_figures:
        main_html += subsection("Points correspondants et triangulation")
        main_html += figure_row([
            (points_img1, "Points sur l’image 1"),
            (points_img2, "Points sur l’image 2"),
        ])
        main_html += figure_pile(
            triangulation_img,
            "Triangulation de Delaunay calculée sur la moyenne des points.",
            style="width: 55%; border-radius: 8px;"
        )

        main_html += subsection("Exemples de trames intermédiaires")
        main_html += figure_row(frame_samples[:3])
        main_html += figure_row(frame_samples[3:])

    main_html += subsection("Vidéo finale")
    main_html += video(
        main_video,
        caption="Vidéo principale : métamorphose du visage précédent vers mon visage.",
        width="320px"
)

    main_html += subsection("Discussion")
    main_html += paragraph(
        "Le résultat obtenu est globalement convaincant, surtout dans les régions où les points "
        "de correspondance étaient bien alignés. La structure générale du visage évolue de manière "
        "progressive et la transition de couleur reste fluide."
    )
    main_html += paragraph(
        "Les artefacts les plus visibles apparaissent surtout autour des cheveux, du contour du visage "
        " . Cela est normal vu que mon collegue a des cheveux longs et moi j'ai des cheveux courts "
        "présentent des différences de pose, d’éclairage ou d’expression."
    )
    main_html += paragraph(
        "L’ajout de points sur les bordures de l’image a permis de mieux contrôler l’arrière-plan "
        "et de limiter certains étirements excessifs à l’extérieur du visage. Pour cette paire "
        "d’images, le rendu est convaincant, puisque les deux images représentent le même type "
        "de contenu, à savoir des visages."
    )

    content += section("Résultat principal : visage précédent vers mon visage", main_html, icon="🎭")

    # -----------------------------------------------------
    # 4. Morphing d’objets
    # -----------------------------------------------------
    objects_html = ""

    for item in object_videos:
        objects_html += subsection(item["title"])

        objects_html += figure_row([
            (item["img1"], item["caption1"]),
            (item["img2"], item["caption2"]),
        ])

        objects_html += figure_row([
            (item["tri1"], item["tri_caption1"]),
            (item["tri2"], item["tri_caption2"]),
        ])

        objects_html += video(
            item["src"],
            caption=item["title"],
            width="300px"
        )

        objects_html += paragraph(item["discussion"])

    content += section("Morphing d’objets", objects_html, icon="☕")

    # -----------------------------------------------------
    # 5. Morphings avec mes amis
    # -----------------------------------------------------
    friends_html = ""
    friends_html += quote(
        "Cette section m’a rappelé Photograph d’Ed Sheeran et l’idée de "
        "“keep this love in a photograph”, qui résonne bien avec ces souvenirs capturés avec mes amis."
    )
    for item in friend_videos:
        friends_html += subsection(item["title"])

        friends_html += figure_row([
            (item["img1"], item["caption1"]),
            (item["img2"], item["caption2"]),
        ])

        friends_html += figure_row([
            (item["tri1"], item["tri_caption1"]),
            (item["tri2"], item["tri_caption2"]),
        ])

        friends_html += video(
            item["src"],
            caption=item["title"],
            width="300px"
        )

        friends_html += paragraph(item["discussion"])

    content += section("Morphings avec mes amis", friends_html, icon="🧑‍🤝‍🧑")

    # -----------------------------------------------------
    # 6. Utilisation de l’IA
    # -----------------------------------------------------
    ai_html = ""

    ai_html += subsection("Déclaration d’utilisation de l’IA")
    ai_html += paragraph(
        "J’ai utilisé un assistant d’IA comme soutien pour la compréhension de l’énoncé, la vérification "
        "de certains choix d’implémentation et l’aide à la rédaction du rapport HTML."
    )

    ai_html += subsection("Prompts utilisés")
    ai_html += """
    <div class="algorithm-box">
        <h4>Prompt</h4>
        <p style="font-family: 'Fira Code', monospace;">
        Aide-moi à structurer un rapport HTML pour un TP de métamorphose de visages.
        Le rapport doit contenir une introduction, une description de l’algorithme,
        la vidéo principale, trois animations supplémentaires, une discussion et une section
        sur l’utilisation de l’IA.
        </p>
    </div>
    """

    ai_html += """
    <div class="algorithm-box">
        <h4>Prompt</h4>
        <p style="font-family: 'Fira Code', monospace;">
        Genere le code du rapport.
        </p>
    </div>
    """

    ai_html += """
    <div class="algorithm-box">
        <h4>Prompt</h4>
        <p style="font-family: 'Fira Code', monospace;">
        Implémente des fonctions de visualisation
        </p>
    </div>
    """

    ai_html += """
    <div class="algorithm-box">
        <h4>Prompt</h4>
        <p style="font-family: 'Fira Code', monospace;">
        Recentre l'image dans le texte
        </p>
    </div>
    """

    

    ai_html += subsection("Résumé de l’approche")
    ai_html += paragraph(
        "L’IA a surtout servi d’assistance pour organiser clairement le rapport et formuler certaines "
        "explications de manière plus structurée. Les contenus finaux ont été revus, corrigés et adaptés "
        "en fonction de mes propres résultats expérimentaux."
    )

    content += section("Utilisation de l’intelligence artificielle", ai_html, icon="🤖")

    # =====================================================
    # HTML final
    # =====================================================

    html = html_document(
        title="TP3 — Métamorphose de visages",
        subtitle=f"GIF-4105/7105 · Rapport de {student_name}",
        icon="🎭",
        content=content,
        accent_color="#ffb300",
    )

    html = html.replace(
        "GIF 4105/7105 &mdash; TP2 | On s'amuse en fréquences",
        "GIF 4105/7105 &mdash; TP3 | Métamorphose de visages"
    )

    save_report(html, output_html)


if __name__ == "__main__":
    generate_report()