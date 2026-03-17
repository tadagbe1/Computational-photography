#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP1 Section 4: Mappage Tonal et Encodage d'Affichage

Ce script:
1. Charge les images XYZ depuis ./images_intermediaires_sec3/*_camera_xyz.tiff
2. Applique l'ajustement de luminosité (À IMPLÉMENTER)
3. Applique le mappage tonal:
   - Linéaire (implémenté)
   - Reinhard (À IMPLÉMENTER)
4. Convertit XYZ vers sRGB linéaire (implémenté)
5. Applique l'OETF sRGB (implémenté)
6. Sauvegarde le JPEG final (implémenté)
7. Analyse les artefacts JPEG (À IMPLÉMENTER)
8. Sauvegarde dans ./images_intermediaires_sec4/

Usage:
    python tp1_sec4.py --input-dir images_intermediaires_sec3 --output-dir images_intermediaires_sec4
"""

import numpy as np
import glob
import os
from PIL import Image

from tp1_io import (
    load_tiff,
    save_tiff16,
    linear_to_srgb,
    xyz_to_linear_srgb,
    quantize_to_8bit,
)
from tp1_rapport import (
    html_document,
    section,
    subsection,
    figure,
    table,
    algorithm_box,
    formula_box,
    save_report,
    comparison_grid,
    create_tonemapping_curves_figure,
    create_tonemapping_comparison_figure,
    create_oetf_comparison_figure,
    create_dynamic_range_figure,
)

from personnal_sections import generate_personnal_images_content

# =============================================================================
# Ajustement de Luminosité
# =============================================================================


def adjust_brightness(xyz_image, percentile=99):
    """
    Ajuster la luminosité de l'image en normalisant au percentile donné.

    Mesure le percentile spécifié du canal Y (luminance) et divise
    toute l'image par cette valeur pour normaliser la luminosité.

    Args:
        xyz_image: Image XYZ [H, W, 3]
        percentile: Percentile à utiliser pour la normalisation (défaut: 99)

    Returns:
        Image XYZ avec luminosité ajustée

    TODO: Implémenter l'ajustement de luminosité

    Indices:
    1. Extraire le canal Y (luminance): Y = xyz_image[:, :, 1]
    2. Filtrer les valeurs valides (Y > 0)
    3. Calculer le percentile spécifié des valeurs valides
    4. Diviser toute l'image par cette valeur
    5. Retourner l'image ajustée
    """
    # =========================================================================
    # TODO: Implémenter l'ajustement de luminosité par le 99e percentile
    # =========================================================================
    Y = xyz_image[:, :, 1]
    
    # Compute the percentile of luminance (excluding zeros/negatives)
    valid_Y = Y[Y > 0]
    if len(valid_Y) == 0:
        print("    Warning: No valid luminance values, skipping brightness adjustment")
        return xyz_image.copy()
    
    percentile_value = np.percentile(valid_Y, percentile)
    
    if percentile_value <= 0:
        print("    Warning: Percentile value <= 0, skipping brightness adjustment")
        return xyz_image.copy()
    
    # Divide the entire image by the percentile value
    adjusted = xyz_image / percentile_value
    
    print(f"    Brightness adjustment: divided by {percentile_value:.6f} (1st percentile)")
    
    return adjusted



# =============================================================================
# Opérateurs de Mappage Tonal
# =============================================================================


def tonemap_linear(xyz_image):
    """
    Mappage tonal linéaire (identité) - pas de compression.

    Les valeurs > 1 seront clippées lors de la conversion finale.

    Args:
        xyz_image: Image XYZ [H, W, 3]

    Returns:
        Image XYZ (copie)
    """
    return xyz_image.copy()


def tonemap_reinhard(xyz_image):
    """
    Mappage tonal de Reinhard: L_out = L_in / (1 + L_in)

    Appliqué à Y (luminance), X et Z sont mis à l'échelle proportionnellement.

    Référence: "Photographic Tone Reproduction for Digital Images" (2002)

    Args:
        xyz_image: Image XYZ [H, W, 3]

    Returns:
        Image XYZ avec mappage tonal appliqué

    TODO: Implémenter l'opérateur de Reinhard

    Indices:
    1. Extraire le canal Y (luminance): Y = xyz_image[:, :, 1]
    2. Appliquer la formule: Y_mapped = Y / (1 + Y)
    3. Calculer le ratio: scale = Y_mapped / Y (attention aux divisions par zéro!)
    4. Appliquer ce ratio à X et Z également
    5. Retourner l'image résultante
    """
    # =========================================================================
    # TODO: Implémenter le mappage tonal de Reinhard
    # =========================================================================
    Y = xyz_image[:, :, 1]
    Y_mapped = Y / (1 + Y)
    scale = np.zeros_like(Y)
    mask = Y > 0
    scale[mask] = Y_mapped[mask] / Y[mask]

    adjusted = xyz_image.copy()
    adjusted[:, :, 0] *= scale
    adjusted[:, :, 1] = Y_mapped
    adjusted[:, :, 2] *= scale
    
    return adjusted



# =============================================================================
# Sauvegarde d'Images
# =============================================================================


def save_jpeg(img_8bit, filepath, quality=95):
    """
    Sauvegarder une image en JPEG.

    Args:
        img_8bit: Image uint8 [H, W, 3]
        filepath: Chemin de sortie
        quality: Qualité JPEG (1-100, défaut: 95)
    """
    Image.fromarray(img_8bit, mode="RGB").save(filepath, "JPEG", quality=quality)
    print(f"  Saved JPEG: {filepath}")


def save_png(img_8bit, filepath):
    """
    Sauvegarder une image en PNG (sans perte).

    Args:
        img_8bit: Image uint8 [H, W, 3]
        filepath: Chemin de sortie
    """
    Image.fromarray(img_8bit, mode="RGB").save(filepath, "PNG")
    print(f"  Saved PNG: {filepath}")


# =============================================================================
# Analyse de Plage Dynamique
# =============================================================================


def analyze_dynamic_range(image_linear):
    """Analyser l'écrêtage des hautes lumières et l'écrasement des ombres."""
    lum = (
        0.2126 * image_linear[:, :, 0]
        + 0.7152 * image_linear[:, :, 1]
        + 0.0722 * image_linear[:, :, 2]
    )

    highlight_pct = np.sum(lum >= 0.99) / lum.size * 100
    shadow_pct = np.sum(lum <= 0.01) / lum.size * 100

    valid = lum[lum > 0]
    if len(valid) > 0:
        min_lum, max_lum = np.percentile(valid, 1), np.percentile(valid, 99)
        dr_stops = np.log2(max_lum / min_lum) if min_lum > 0 else 0
    else:
        dr_stops = 0

    return {
        "highlight_clipped_percent": highlight_pct,
        "shadow_crushed_percent": shadow_pct,
        "dynamic_range_stops": dr_stops,
        "min_luminance": float(np.min(lum)),
        "max_luminance": float(np.max(lum)),
        "mean_luminance": float(np.mean(lum)),
    }


# =============================================================================
# Génération du Rapport HTML
# =============================================================================


def generate_report(results, output_dir):
    """
    Générer un rapport HTML template pour toutes les sections du TP1.
    
    Crée un rapport complet avec:
    - Section 1: Chargement et compréhension des données RAW
    - Section 2: Dématriçage (Demosaicking)
    - Section 3: Balance des Blancs (White Balance)
    - Section 4: Mappage tonal et encodage d'affichage
    
    Inclut toutes les figures générées et des espaces "À remplir" pour l'étudiant.
    """
    # Définir les répertoires de sortie pour chaque section
    # Si output_dir est "images_intermediaires_sec4", base_dir sera le répertoire parent
    if "images_intermediaires_sec" in os.path.basename(output_dir):
        base_dir = os.path.dirname(output_dir) or "."
    else:
        base_dir = output_dir
    
    sec1_dir = os.path.join(base_dir, "images_intermediaires_sec1")
    sec2_dir = os.path.join(base_dir, "images_intermediaires_sec2")
    sec3_dir = os.path.join(base_dir, "images_intermediaires_sec3")
    sec4_dir = output_dir
    
    # Obtenir la liste des basenames (noms de fichiers sans extension)
    basenames = [result["basename"] for result in results] if results else []
    
    # Si aucun résultat, chercher les fichiers dans les répertoires
    if not basenames:
        # Chercher dans sec1
        tiff_files = glob.glob(os.path.join(sec1_dir, "*.tiff"))
        basenames = [os.path.splitext(os.path.basename(f))[0] for f in tiff_files if "zoom" not in f]
        basenames = list(set(basenames))  # Dédupliquer
    
    # Separate proposed images and personnal images
    personnal_basenames = []
    temp_basenames = []
    for basename in basenames:
        if basename.startswith('LRM'):
            personnal_basenames.append(basename)
        else:
            temp_basenames.append(basename)
        
    basenames = temp_basenames.copy()

    # Limiter à 2 images d'exemple pour rendre le rapport plus court
    basenames = sorted(basenames)[:2]
    content = ""
    
    # =============================================================================
    # SECTION 1: Chargement et Compréhension des Données RAW
    # =============================================================================
    sec1_content = ""
    
    # Texte d'introduction pour la section 1
    sec1_content += subsection(
        "Introduction",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4fc3f7;">'

        '<p>'
        'Le format RAW permet de représenter les données brutes capturées par le capteur d’une caméra. '
        'Il s’agit d’un format brut, qui n’est pas directement affichable, car aucune étape de traitement d’image n’y est encore appliquée. '
        'Chaque pixel du capteur mesure une quantité de lumière, correspondant au nombre de photons reçus pendant le temps d’exposition. '
        '</p>'

        '<p>'
        'Une manière courante de capturer ces données brutes consiste à utiliser un filtre de Bayer, dans lequel chaque pixel mesure l’intensité d’une seule composante de couleur : rouge, vert ou bleu. '
        'Le motif de Bayer est une matrice bidimensionnelle répétitive, où chaque sous-matrice de taille 2×2 contient un pixel rouge, un pixel bleu et deux pixels verts. '
        'Cette répartition privilégie le vert, auquel l’œil humain est plus sensible.'
        '</p>'

        '<p>'
        'Les données brutes capturées par chaque pixel contiennent non seulement l’intensité lumineuse mesurée, mais également un niveau de noir (offset électronique) ainsi que du bruit. '
        'La normalisation des données RAW permet d’extraire les intensités utiles mesurées par le capteur en tenant compte du niveau de noir et du niveau de saturation, qui correspond au niveau de blanc maximal que la caméra peut enregistrer.'
        '</p>'

        '</div>'
    )
    
    for basename in basenames:
        sec1_img_content = ""
        
        # Figure: Zoom sur la mosaïque Bayer
        zoom_path = os.path.join(sec1_dir, f"{basename}_zoom16x16.png")
        #breakpoint()
        if os.path.exists(zoom_path):
            sec1_img_content += subsection(
                f"Région 16×16 de la mosaïque - {basename}",
                figure(f"img/images_intermediaires_sec1/{basename}_zoom16x16.png",
                       "Zoom sur une région 16×16 montrant les valeurs normalisées et le motif de Bayer coloré.")
            )
        
        if sec1_img_content:
            sec1_content += section(f"Image: {basename}", sec1_img_content)
    
    # Analyse et observations
    sec1_content += subsection(
        "Analyse et observations",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4fc3f7;">'
        '<p>'
        'Nous constatons que les métadonnées extraites contiennent des informations liées aux propriétés physiques de la scène, ainsi que des données nécessaires pour transformer les données brutes en une image affichable, notamment la balance des blancs et la matrice de conversion RGB–XYZ. '
        'Elles incluent également des informations relatives aux caractéristiques du capteur, comme le motif de Bayer et la profondeur de bits.'
        '</p>'

        '<p>'
        'Nous remarquons que le motif de Bayer est une matrice de dimension 2 où chaque pixel capte un seul canal de lumière. '
        'Pour des images trop noires, certains pixels du motif de Bayer peuvent être noirs également.'
        '</p>'

        '<p>'
        'La normalisation permet de retirer le niveau de noir et d’obtenir des intensités par pixel cohérentes avec les données de la mosaïque brute. '
        '</p>'

        '</div>'
    )
    
    content += section("Section 1: Chargement et Compréhension des Données RAW", sec1_content, icon="📷")
    
    # =============================================================================
    # SECTION 2: Dématriçage (Demosaicking)
    # =============================================================================
    sec2_content = ""
    
    # Texte d'introduction pour la section 2
    sec2_content += subsection(
        "Introduction",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #778da9;">'
        '<p>'
        'Comme dit précédemment, chaque pixel du filtre de Bayer capte l’intensité pour une seule couleur. '
        'Le dématriçage nous permet d’obtenir les valeurs des couleurs R, G et B pour chaque pixel. '
        '</p>'

        '<p>'
        'Pour le dématriçage bilinéaire, pour chaque pixel, les deux couleurs qui lui manquent sont interpolées en faisant la moyenne avec ses voisins ayant la couleur particulière considérée. '
        'Quant au dématriçage de Malvar–He–Cutler, il corrige la méthode bilinéaire en calculant un gradient local à partir du pixel courant, qui est appliqué à l’interpolation bilinéaire, ce qui permet de mieux préserver les contours et les détails.'
        '</p>'

        '<p>'
        'Avec la méthode de dématriçage bilinéaire, il y a des artefacts comme le flou et les bavures de couleur.'
        ' Ces artefacts sont moins prononcés lorsqu’on utilise le dématriçage de Malvar–He–Cutler.'
        '</p>'
        '</div>'
    )
    
    for basename in basenames:
        sec2_img_content = ""
        
        # Figure: Comparaison des méthodes
        comp_path = os.path.join(sec2_dir, f"{basename}_comparison.png")
        #breakpoint()
        if os.path.exists(comp_path):
            sec2_img_content += subsection(
                f"Comparaison des méthodes - {basename}",
                figure(f"img/images_intermediaires_sec2/{basename}_comparison.png",
                       "Comparaison des méthodes de dématriçage")
            )
        
        # Figure: Zoom sur les artefacts
        zoom_path = os.path.join(sec2_dir, f"{basename}_zoom.png")
        if os.path.exists(zoom_path):
            sec2_img_content += subsection(
                f"Zoom sur les artefacts - {basename}",
                figure(f"img/images_intermediaires_sec2/{basename}_zoom.png",
                       "Recadrages montrant les artefacts de contour")
            )
        
        if sec2_img_content:
            sec2_content += section(f"Image: {basename}", sec2_img_content)
    
    # Analyse et observations
    sec2_content += subsection(
        "Analyse et observations",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #778da9;">'
        '<p >'
        'Les résultats obtenus avec la méthode de Malvar–He–Cutler sont nettement plus réalistes que ceux obtenus avec l’interpolation bilinéaire.' 
        'Cependant, la méthode bilinéaire prend environ trois fois moins de temps que celle de Malvar–He–Cutler.'
        '</p>'

        '<p >'
        'Le SSIM entre les résultats des méthodes bilinéaires et de Malvar–He–Cutler est, dans la plupart des cas, supérieur à 60 %, ce qui suggère que les résultats retournés par les deux méthodes se ressemblent visuellement. '
        'Le PSNR, qui est généralement au-dessus de 20 dB, montre que les images générées avec les deux méthodes sont numériquement acceptables.'
        '</p>'

        '<p >'
        'Les artefacts apparaissent principalement au niveau des contours et des zones à for contraste.'
        '</p>'

        '</div>'
    )
    
    content += section("Section 2: Dématriçage (Demosaicking)", sec2_content, icon="🎨")
    
    # =============================================================================
    # SECTION 3: Balance des Blancs (White Balance)
    # =============================================================================
    sec3_content = ""
    
    # Texte d'introduction pour la section 3
    sec3_content += subsection(
        "Introduction",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #e94560;">'
        
        '<p>'
        'La balance des blancs est une étape du traitement d’image qui permet de corriger les dominantes de couleur causées par l’éclairage et par la réponse du capteur. '
        'L’objectif est que les zones neutres de la scène apparaissent réellement grises ou blanches. '
        'Concrètement, cette correction se fait en appliquant des coefficients multiplicatifs aux canaux rouge, vert et bleu.'
        'Différentes méthodes ont été utilisées.'
        'La balance des blancs par région neutre consiste à détecter automatiquement une zone supposée grise dans l’image, puis à ajuster les canaux afin de rendre cette région neutre. '
        'Cette méthode est souvent efficace, mais elle dépend fortement de la présence d’une région réellement neutre dans la scène.'
        ' La méthode Grey World repose sur l’hypothèse que la couleur moyenne de l’image est neutre ; elle est simple et rapide à mettre en œuvre, mais peut donner de mauvais résultats lorsque la scène est dominée par une couleur particulière. '
        'Enfin, la balance des blancs fournie par la caméra utilise des paramètres calculés lors de la capture et donne en général des résultats cohérents, même si elle reste dépendante du matériel et moins flexible. '
        'Ainsi, chaque méthode présente des avantages et des limites, et leur efficacité dépend principalement du contenu de la scène et des hypothèses sur lesquelles elles reposent. '
        '</div>'
    )
    
    for basename in basenames:
        sec3_img_content = ""
        
        # Figure: Comparaison des méthodes
        comp_path = os.path.join(sec3_dir, f"{basename}_comparison.png")
        if os.path.exists(comp_path):
            sec3_img_content += subsection(
                f"Comparaison des méthodes - {basename}",
                figure(f"img//images_intermediaires_sec3/{basename}_comparison.png",
                       "Comparaison des méthodes de balance des blancs")
            )
        
        # Figure: Conversion XYZ
        xyz_path = os.path.join(sec3_dir, f"{basename}_xyz_comparison.png")
        if os.path.exists(xyz_path):
            sec3_img_content += subsection(
                f"Conversion XYZ - {basename}",
                figure(f"img/images_intermediaires_sec3/{basename}_xyz_comparison.png",
                       "Images converties en XYZ puis reconverties en sRGB")
            )
        
        if sec3_img_content:
            sec3_content += section(f"Image: {basename}", sec3_img_content)
    
    # Analyse et observations
    sec3_content += subsection(
        "Analyse et observations",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #e94560;">'
        '<p>'
        'Nous remarquons que la méthode Grey World donne un résultat plus proche de celui de la caméra. '
        'Cependant, la méthode auto-neutre est plus proche de l’image originale. '
        'De façon générale, le multiplicateur du canal vert pour toutes les méthodes est égal à 1. '
        'Il est supérieur à 1 pour les autres canaux, en particulier pour les canaux R et B. '
        'Lorsque le multiplicateur du canal R est trop grand, l’image apparaît visuellement plus rouge.'
        '</p>'

        '<p>'
        'L’espace XYZ, contrairement à l’espace RGB, est un espace standard indépendant de la nature du capteur. '
        'La conversion de l’espace RGB de la caméra vers l’espace XYZ se fait via une multiplication matricielle.'
        'La matrice utilisée est fournie par les métadonnées de la caméra en question. '
        '</p>'
        '</div>'
    )
    
    content += section("Section 3: Balance des Blancs (White Balance)", sec3_content, icon="⚪")
    
    # =============================================================================
    # SECTION 4: Mappage Tonal et Encodage d'Affichage
    # =============================================================================
    sec4_content = ""
    
    # Texte d'introduction pour la section 4
    sec4_content += subsection(
        "Introduction",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #778da9;">'
        '<p>'
        'Le mappage tonal permet de compresser la plage dynamique des images HDR afin de les rendre affichables sur des écrans à dynamique limitée. '
        'Le mappage linéaire est simple mais peut perdre des détails, tandis que l’opérateur de Reinhard applique une compression non linéaire mieux adaptée aux scènes à forte dynamique. '
        'L’OETF sRGB transforme ensuite les valeurs linéaires en valeurs adaptées à l’affichage. '
        'L’analyse de la plage dynamique justifie ces étapes en montrant l’écart entre les intensités capturées et celles supportées par l’affichage.'
        '</p>'
        '</div>'
    )
    
    # Concepts et algorithmes
    algorithms = algorithm_box(
        "A) Ajustement de luminosité",
        "<p>Division par le 99e percentile. <strong>À IMPLÉMENTER</strong></p>",
    )
    algorithms += algorithm_box(
        "B) Mappage tonal",
        "<p><b>Linéaire:</b> Pas de compression.</p>"
        "<p><b>Reinhard:</b> <code>L_out = L_in / (1 + L_in)</code>. <strong>À IMPLÉMENTER</strong></p>",
    )
    algorithms += algorithm_box(
        "C) Conversion XYZ → sRGB",
        "<p>Matrice standard D65 suivie de l'OETF sRGB. <strong>IMPLÉMENTÉ</strong></p>",
    )
    algorithms += algorithm_box(
        "D) OETF sRGB",
        formula_box("sRGB = 1.055 × linéaire^(1/2.4) − 0.055")
        + "<p><strong>IMPLÉMENTÉ</strong></p>",
    )
    algorithms += algorithm_box(
        "E) Analyse des artefacts JPEG",
        "<p>Sauvegarde en différentes qualités et analyse des artefacts. <strong>À IMPLÉMENTER PAR L'ÉTUDIANT</strong></p>",
    )
    
    sec4_content += subsection("Concepts et algorithmes", algorithms)
    
    # Figure: Courbes de mappage tonal
    curves_path = os.path.join(sec4_dir, "tonemapping_curves.png")
    #breakpoint()
    if os.path.exists(curves_path):
        sec4_content += subsection(
            "Courbes de mappage tonal",
            figure(curves_path, "Comparaison des courbes de réponse")
        )
    
    # Figures pour chaque image
    # Utiliser results si disponible, sinon utiliser basenames
    # Filtrer pour ne garder que les 2 images sélectionnées
    if results:
        images_to_process = [r for r in results if r["basename"] in basenames]
    else:
        images_to_process = [{"basename": bn} for bn in basenames]
    
    for result in images_to_process:
        basename = result["basename"]
        dr = result.get("dynamic_range", {})
        jpeg_info = result.get("jpeg_analysis", None)
        
        sec4_img_content = ""
        
        # Figure: Comparaison des opérateurs
        comp_path = os.path.join(sec4_dir, f"{basename}_tonemapping_comparison.png")
        if os.path.exists(comp_path):
            sec4_img_content += subsection(
                "Comparaison des opérateurs",
                figure(
                    comp_path,
                    "Comparaison: Linéaire, Reinhard",
                ),
            )
        
        # Figure: Avant/Après OETF
        oetf_path = os.path.join(sec4_dir, f"{basename}_oetf_comparison.png")
        if os.path.exists(oetf_path):
            sec4_img_content += subsection(
                "Avant/Après OETF",
                figure(
                    oetf_path,
                    "L'OETF encode les valeurs linéaires pour l'affichage",
                ),
            )
        
        # Figure: Image finale
        final_path = os.path.join(sec4_dir, f"{basename}_final.jpg")
        if os.path.exists(final_path):
            sec4_img_content += subsection(
                "Image finale",
                figure(final_path, "Image JPEG finale (qualité 95)"),
            )
        
        # Figure: Plage dynamique
        dr_path = os.path.join(sec4_dir, f"{basename}_dynamic_range.png")
        if os.path.exists(dr_path):
            dr_table = ""
            if dr:
                dr_table = table(
                    ["Métrique", "Valeur"],
                    [
                        [
                            "Plage dynamique",
                            f"{dr.get('dynamic_range_stops', 0):.1f} stops",
                        ],
                        [
                            "Hautes lumières écrêtées",
                            f"{dr.get('highlight_clipped_percent', 0):.2f}%",
                        ],
                        ["Ombres écrasées", f"{dr.get('shadow_crushed_percent', 0):.2f}%"],
                    ],
                )
            sec4_img_content += subsection(
                "Plage dynamique",
                figure(
                    dr_path, "Analyse des hautes lumières et ombres"
                ) + dr_table,
            )

        # ------------------------------------------------------------------
        # Analyse des artefacts JPEG
        # ------------------------------------------------------------------
        if jpeg_info:
            rows = []

            for q, size in jpeg_info["jpeg_sizes"].items():
                rows.append([f"JPEG qualité {q}", f"{size/1024:.1f} KB"])

            rows.append(["PNG (sans perte)", f"{jpeg_info['png_size']/1024:.1f} KB"])

            jpeg_table = table(
                ["Format", "Taille du fichier"],
                rows
            )

            sec4_img_content += subsection(
                "Analyse des artefacts JPEG",
                jpeg_table
                + figure(
                    f"img/images_intermediaires_sec4/{basename}_jpeg_q95.jpg",
                    "JPEG qualité 95 – quasi sans artefacts",
                )
                + figure(
                    f"img/images_intermediaires_sec4/{basename}_jpeg_q50.jpg",
                    "JPEG qualité 50 – artefacts visibles (blocs, lissage)",
                )
                + figure(
                    f"img/images_intermediaires_sec4/{basename}_png.png",
                    "PNG sans perte – référence",
                )
            )

        
        if sec4_img_content:
            sec4_content += section(basename, sec4_img_content)
    
    # Analyse et observations
    sec4_content += subsection(
        "Analyse et observations", 
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #778da9;">'
        '<p >'
        'Le mappage tonal de Reinhard préserve mieux les détails dans les hautes lumières que le mappage linéaire. L’OETF sRGB améliore le contraste perçu et rend l’image plus adaptée à l’affichage, avec peu de hautes lumières écrêtées et aucune ombre écrasée. '
        'Les artefacts JPEG deviennent visibles à faible qualité, au prix d’une réduction significative de la taille des fichiers.'
        '</p>'
        '</div>'
    )
    
    content += section("Section 4: Mappage Tonal et Encodage d'Affichage", sec4_content, icon="🎨")
    
    # =============================================================================
    # GRILLE DE COMPARAISON DES IMAGES FINALES
    # =============================================================================
    # Collecter toutes les images finales JPG de la section 4 et leurs références
    comparisons = []
    jpg_files = sorted(glob.glob(os.path.join(sec4_dir, "*_final.jpg")))
    
    for jpg_path in jpg_files:
        basename = os.path.basename(jpg_path).replace("_final.jpg", "")
        if not basename.startswith('LRM'):
            final_src = os.path.basename(jpg_path)
            final_src = os.path.join(sec4_dir, final_src)
            
            # Chercher l'image de référence correspondante
            reference_src = None
            srgb_path = os.path.join(sec1_dir, f"{basename}_srgb.jpg")
            if os.path.exists(srgb_path):
                reference_src = f"img/images_intermediaires_sec1/{basename}_srgb.jpg"
            
            if reference_src:
                comparisons.append({
                    "basename": basename,
                    "final_src": final_src,
                    "reference_src": reference_src,
                    "final_alt": f"Image finale - {basename}",
                    "reference_alt": f"Référence sRGB - {basename}"
                })
            else:
                # Si pas de référence, ajouter quand même l'image finale seule
                comparisons.append({
                    "basename": basename,
                    "final_src": final_src,
                    "reference_src": final_src,  # Dupliquer pour l'affichage
                    "final_alt": f"Image finale - {basename}",
                    "reference_alt": f"Image finale - {basename}"
                })
    
    if comparisons:
        grid_content = subsection(
            "Comparaison: Vos résultats vs Références sRGB",
            '<p style="color: #a0a0a0; margin-bottom: 20px;">Comparez vos images finales avec les aperçus sRGB générés par rawpy. Cliquez sur une image pour l\'agrandir.</p>'
        )
        grid_content += comparison_grid(comparisons)
        content += section("Comparaison des Images Finales", grid_content, icon="🖼️")
    
    # =============================================================================
    # IMAGES PERSONNELLES
    # =============================================================================


    content += generate_personnal_images_content(personnal_basenames, sec1_dir, sec2_dir, sec3_dir, sec4_dir, results)

    conclusion_content = subsection(
        "IA générative",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffd54f;">'
        '<p>'
        'Nous avons eu recours à l’intelligence artificielle pour comprendre les étapes de traitement des données brutes de la caméra ainsi que certains aspects du code.'

        'Certaines parties, notamment les sections HTML, ont été générées par ChatGPT.'

        'Dans une démarche de compréhension et de validation, nous avons comparé les informations issues de la littérature avec les résultats et explications fournis par l’IA afin de vérifier leur cohérence et leur exactitude.'
        '</p>'

        '<p>'
        'Prompts: '
        '</p>'

        '<p>'
        'Donne moi le code pour la section des artefacs'
        '</p>'

        '<p>'
        'Corrige les fautes dans mes textes'
        '</p>'

        '<p>'
        'Genère moi le code pour interpolation bilinéaire'
        '</p>'

        '</div>'
    )

    content += section("IA générative", conclusion_content, icon="📝")

    # =============================================================================
    # CONCLUSION GÉNÉRALE
    # =============================================================================
    conclusion_content = subsection(
        "Conclusion",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffd54f;">'
        '<p>'
        'Ce TP1 nous a permis de comprendre toute la pipeline de traitement des données brutes capturées par la caméra. '
        'Les différentes étapes de traitement sont : la capture des données brutes, le dématriçage, la balance des blancs et le mappage tonal. '
        'Nous avons testé nos algorithmes sur les données brutes proposées pour le travail, ainsi que sur trois images brutes capturées par un téléphone Android.'
        'Nous avons appris comment les images sont traitées par la caméra, mais aussi les différentes raisons pour lesquelles ces étapes sont importantes. '
        'Les difficultés rencontrées concernent principalement la capture des images brutes.'
        'Les possibles améliorations pourraient être d’implémenter des méthodes de dématriçage plus avancées.'
        '</p>'
        '</div>'
    )
    
    content += section("Conclusion", conclusion_content, icon="📝")
    
    # Générer le document HTML final
    html = html_document(
        "Rapport TP1 - Tadagbé Dhossou",
        "",
        "📸",
        content,
        accent_color="#778da9",
    )
    
    save_report(html, os.path.join(output_dir, "../../index.html"))


# =============================================================================
# Traitement Principal
# =============================================================================


def process_display_encoding(
    input_dir="img/images_intermediaires_sec3",
    output_dir="img/images_intermediaires_sec4",
    input_suffix="_camera_xyz.tiff",
):
    """Traiter les images XYZ avec mappage tonal et encodage d'affichage."""
    os.makedirs(output_dir, exist_ok=True)

    tiff_files = sorted(glob.glob(os.path.join(input_dir, f"*{input_suffix}")))

    if not tiff_files:
        print(f"Aucun fichier *{input_suffix} trouvé dans {input_dir}/")
        return

    print(f"\n{'#'*60}")
    print("# Section 4: Mappage Tonal et Encodage d'Affichage")
    print(f"{'#'*60}")
    print(f"\n{len(tiff_files)} fichier(s) trouvé(s)")

    # Générer la figure des courbes une seule fois
    create_tonemapping_curves_figure(os.path.join(output_dir, "tonemapping_curves.png"))

    results = []

    for tiff_path in tiff_files:
        basename = os.path.basename(tiff_path).replace(input_suffix, "")

        print(f"\n{'='*60}")
        print(f"Traitement: {basename}")
        print("=" * 60)

        try:
            xyz_image = load_tiff(tiff_path)
            result = {"basename": basename}

            # Ajustement de luminosité (à implémenter par l'étudiant)
            print("  [0] Ajustement de luminosité...")
            xyz_image = adjust_brightness(xyz_image, percentile=99)

            # Comparaison des opérateurs de mappage tonal
            print("  [A] Comparaison du mappage tonal...")
            tonemap_funcs = {
                "Linéaire": tonemap_linear,
                "Reinhard": tonemap_reinhard,
            }
            srgb_results = create_tonemapping_comparison_figure(
                xyz_image,
                os.path.join(output_dir, f"{basename}_tonemapping_comparison.png"),
                tonemap_funcs,
                xyz_to_linear_srgb,
                linear_to_srgb,
                title=f"Mappage tonal - {basename}",
            )

            # Utiliser linéaire pour la suite (ou Reinhard si implémenté)
            xyz_tonemapped = tonemap_linear(xyz_image)
            rgb_linear = xyz_to_linear_srgb(xyz_tonemapped)
            rgb_linear = np.clip(rgb_linear, 0, 1)
            srgb = linear_to_srgb(rgb_linear)

            # Sauvegarder les résultats
            for name, img in srgb_results.items():
                save_tiff16(
                    img, os.path.join(output_dir, f"{basename}_{name.lower()}.tiff")
                )

            # Comparaison OETF
            print("  [B] Comparaison OETF...")
            create_oetf_comparison_figure(
                rgb_linear,
                srgb,
                os.path.join(output_dir, f"{basename}_oetf_comparison.png"),
                title=f"OETF sRGB - {basename}",
            )

            # Sauvegarder l'image finale en JPEG
            print("  [C] Sauvegarde de l'image finale...")
            img_8bit = quantize_to_8bit(srgb)

            final_jpg = os.path.join(output_dir, f"{basename}_final.jpg")
            save_jpeg(img_8bit, final_jpg, quality=95)

            # TODO: L'étudiant doit implémenter l'analyse des artefacts JPEG
            # - Sauvegarder en différentes qualités (95, 75, 50, 25)
            # - Comparer avec PNG (sans perte)
            # - Visualiser les artefacts de compression
            # - Créer un graphique taille vs qualité
            print("  [!] Analyse JPEG à implémenter par l'étudiant")

            jpeg_qualities = [95, 50]
            jpeg_sizes = {}

            for q in jpeg_qualities:
                jpeg_path = os.path.join(output_dir, f"{basename}_jpeg_q{q}.jpg")
                save_jpeg(img_8bit, jpeg_path, quality=q)
                jpeg_sizes[q] = os.path.getsize(jpeg_path)

            # Sauvegarde PNG (sans perte)
            png_path = os.path.join(output_dir, f"{basename}_png.png")
            save_png(img_8bit, png_path)
            png_size = os.path.getsize(png_path)

            result["jpeg_analysis"] = {
                "qualities": jpeg_qualities,
                "jpeg_sizes": jpeg_sizes,
                "png_size": png_size,
            }

            # Analyse de plage dynamique
            print("  [D] Analyse de plage dynamique...")
            dr_analysis = analyze_dynamic_range(rgb_linear)
            result["dynamic_range"] = dr_analysis
            print(
                f"    Plage dynamique: {dr_analysis['dynamic_range_stops']:.1f} stops"
            )

            create_dynamic_range_figure(
                rgb_linear,
                srgb,
                dr_analysis,
                os.path.join(output_dir, f"{basename}_dynamic_range.png"),
                title=f"Plage dynamique - {basename}",
            )

            results.append(result)

        except Exception as e:
            print(f"\nErreur lors du traitement de {tiff_path}: {e}")
            import traceback

            traceback.print_exc()

    if results:
        generate_report(results, output_dir)

    print(f"\n{'='*60}")
    print(f"Terminé! {len(results)} image(s) traitée(s) → {output_dir}/")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="TP1 Section 4: Mappage Tonal et Encodage"
    )
    parser.add_argument("--input-dir", "-i", default="img/images_intermediaires_sec3")
    parser.add_argument("--output-dir", "-o", default="img/images_intermediaires_sec4")
    parser.add_argument("--suffix", "-s", default="_camera_xyz.tiff")

    args = parser.parse_args()
    process_display_encoding(args.input_dir, args.output_dir, args.suffix)

    # '<p>'
    # '</p>'
