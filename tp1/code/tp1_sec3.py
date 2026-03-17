#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP1 Section 3: Balance des Blancs (White Balance)

Ce script:
1. Charge les images TIFF dématricées depuis ./images_intermediaires_sec2/*_bilinear.tiff
2. Charge les métadonnées depuis ./images_intermediaires_sec1/*.json
3. Applique les algorithmes de balance des blancs:
   A) Manuelle (clic sur région neutre) - À IMPLÉMENTER
   B) Grey World - À IMPLÉMENTER
   C) Proposé par la caméra - IMPLÉMENTÉ
4. Convertit en espace XYZ - IMPLÉMENTÉ
5. Sauvegarde dans ./images_intermediaires_sec3/

Usage:
    python tp1_sec3.py --input-dir images_intermediaires_sec2 --output-dir images_intermediaires_sec3
"""

import numpy as np
import glob
import os

from tp1_io import (
    load_tiff,
    load_metadata,
    save_tiff16,
    save_jpeg,
    linear_to_srgb,
    xyz_to_srgb,
)
from tp1_rapport import (
    html_document,
    section,
    subsection,
    figure,
    table,
    algorithm_box,
    save_report,
    create_wb_comparison_figure,
    create_xyz_comparison_figure,
)


# =============================================================================
# Algorithmes de Balance des Blancs
# =============================================================================


def find_neutral_region(image, region_size=11):
    """
    Trouve automatiquement une région neutre dans l'image.

    L'algorithme cherche des régions qui sont à la fois lumineuses et neutres
    (faible écart-type entre les canaux R, G, B).

    Args:
        image: Image RGB [H, W, 3] normalisée [0, 1]
        region_size: Taille de la région à analyser

    Returns:
        (y, x): Position du centre de la meilleure région neutre

    TODO: Implémenter l'algorithme de sélection automatique de région neutre

    Algorithme:
    1. Parcourir l'image par pas réguliers (ex: max(region_size, 20) pixels)
    2. Pour chaque région, calculer:
       - Luminosité moyenne: 0.299*R + 0.587*G + 0.114*B
       - Neutralité: 1.0 / (1.0 + std(means) * 10)
       - Score combiné: luminosité × neutralité
    3. Garder la région avec le meilleur score (si luminosité > 0.2)
    """
    # =========================================================================
    # TODO: Implémenter la sélection automatique de région neutre
    # =========================================================================

    H, W, _ = image.shape
    step = 20
    half = region_size // 2

    best_score = -np.inf
    best_position = (0, 0)

    for y in range(half, H-half, step):
        for x in range(half, W-half, step):
            region = image[y-half : y + half + 1, x-half : x + half + 1,  :]
            luminosity = 0.299 * region[..., 0] + 0.587 * region[..., 1] + 0.114 * region[..., 2]
            mean_luminosity = np.mean(luminosity)

            neutrality = 1 / (1 + 10 * np.mean(np.std(region, axis=2)))

            score = mean_luminosity * neutrality
            if mean_luminosity > 0.2 and score >= best_score:
                best_score = score
                best_position = (y, x)

    return best_position



def white_balance_auto_neutral(image, region_size=11, target_gray=0.5):
    """
    Balance des blancs par sélection automatique de région neutre.

    Trouve automatiquement une région neutre, puis calcule les multiplicateurs
    de correction basés sur cette région.

    Args:
        image: Image RGB [H, W, 3] normalisée [0, 1]
        region_size: Taille de la région à analyser
        target_gray: Valeur cible pour les neutres (0.5 par défaut)

    Returns:
        corrected: Image corrigée
        multipliers: Tuple (mult_R, mult_G, mult_B)
        neutral_pos: Position (y, x) de la région neutre sélectionnée

    TODO: Implémenter la balance des blancs par région neutre automatique

    Indices:
    1. Utiliser find_neutral_region() pour trouver la région neutre
    2. Extraire la région autour de cette position
    3. Calculer la moyenne de chaque canal R, G, B dans cette région
    4. Calculer les multiplicateurs: mult_X = target_gray / mean_X
    5. Appliquer les multiplicateurs à toute l'image
    6. Clipper à [0, 1]
    """
    # =========================================================================
    # TODO: Implémenter la balance des blancs par région neutre automatique
    # =========================================================================

    y, x = find_neutral_region(image, region_size)
    half = region_size // 2

    neutral_region = image[y - half: y + half + 1, x - half: x + half + 1, :]
    r_mean, g_mean, b_mean = np.mean(neutral_region[..., 0]), np.mean(neutral_region[..., 1]), np.mean(neutral_region[..., 2])

    mul_r, mul_g, mul_b = target_gray/r_mean, target_gray/g_mean, target_gray/b_mean

    corrected_image = image.copy()
    corrected_image[..., 0] *= mul_r
    corrected_image[..., 1] *= mul_g
    corrected_image[..., 2] *= mul_b

    corrected_image = np.clip(corrected_image, 0.0, 1.0)

    return corrected_image, (mul_r, mul_g, mul_b), (y, x)

    

def white_balance_grey_world(image):
    """
    Algorithme Grey World: mettre à l'échelle chaque canal pour que
    toutes les moyennes soient égales (typiquement à la moyenne du vert).

    Hypothèse: la couleur moyenne d'une scène devrait être un gris neutre.

    Args:
        image: Image RGB [H, W, 3] normalisée [0, 1]

    Returns:
        corrected: Image corrigée
        multipliers: Tuple (mult_R, mult_G, mult_B)

    TODO: Implémenter l'algorithme Grey World

    Indices:
    1. Calculer la moyenne de chaque canal sur toute l'image
    2. Utiliser la moyenne du vert comme référence (canal le plus fiable en Bayer)
    3. Calculer les multiplicateurs: mult_X = mean_G / mean_X
    4. Appliquer les multiplicateurs à toute l'image
    5. Clipper à [0, 1]
    """
    # =========================================================================
    # TODO: Implémenter l'algorithme Grey World
    # =========================================================================

    r_mean, g_mean, b_mean = np.mean(image[..., 0]), np.mean(image[..., 1]), np.mean(image[..., 2])
    mult_r, mult_g, mult_b = g_mean / r_mean, g_mean / g_mean, g_mean / b_mean

    corrected_image = image.copy()
    corrected_image[..., 0] *= mult_r
    corrected_image[..., 1] *= mult_g
    corrected_image[..., 2] *= mult_b

    return np.clip(corrected_image, 0.0, 1.0), (mult_r, mult_g, mult_b)

def white_balance_camera(image, camera_wb):
    """
    Appliquer la balance des blancs proposée par la caméra (as-shot).

    Les multiplicateurs sont stockés dans les métadonnées du fichier RAW.

    Args:
        image: Image RGB [H, W, 3] normalisée [0, 1]
        camera_wb: Liste des multiplicateurs [R, G, B, ?] depuis camera_whitebalance

    Returns:
        corrected: Image corrigée
        multipliers: Tuple (mult_R, mult_G, mult_B)
    """
    multipliers = (camera_wb[0], camera_wb[1], camera_wb[2])

    corrected = image.copy()
    for c in range(3):
        corrected[:, :, c] *= multipliers[c]

    return np.clip(corrected, 0, 1), multipliers


# =============================================================================
# Conversion d'Espace Colorimétrique
# =============================================================================


def camera_rgb_to_xyz(image, rgb_xyz_matrix):
    """
    Convertir le RGB caméra en XYZ en utilisant rgb_xyz_matrix.

    La matrice de rawpy (cam_xyz) convertit XYZ → Camera RGB.
    On la normalise et l'inverse pour obtenir Camera RGB → XYZ.

    Args:
        image: Image RGB [H, W, 3] normalisée
        rgb_xyz_matrix: Matrice 3x4 ou 4x3 depuis les métadonnées

    Returns:
        Image XYZ [H, W, 3]
    """
    xyz_mat = np.array(rgb_xyz_matrix, dtype=np.float64)

    if xyz_mat.shape[0] >= 3 and xyz_mat.shape[1] >= 3:
        xyz_to_cam = xyz_mat[:3, :3]

        # Normaliser les lignes
        row_sums = np.sum(xyz_to_cam, axis=1, keepdims=True)
        row_sums = np.where(np.abs(row_sums) < 1e-10, 1.0, row_sums)
        xyz_to_cam_norm = xyz_to_cam / row_sums

        # Inverser
        try:
            cam_to_xyz = np.linalg.inv(xyz_to_cam_norm)
        except np.linalg.LinAlgError:
            cam_to_xyz = np.linalg.pinv(xyz_to_cam_norm)
    else:
        cam_to_xyz = np.eye(3)

    return np.einsum("ij,...j", cam_to_xyz, image)


# =============================================================================
# Génération du Rapport HTML
# =============================================================================


def generate_report(results, output_dir):
    """Générer le rapport HTML pour la section 3."""
    algorithms = algorithm_box(
        "A) Sélection automatique de région neutre",
        "<p>Trouve automatiquement une région lumineuse et neutre. Calcul: <code>mult_X = gris_cible / moyenne_X</code>. <strong>À IMPLÉMENTER</strong></p>",
    )
    algorithms += algorithm_box(
        "B) Algorithme Grey World",
        "<p>Mise à l'échelle pour que toutes les moyennes égalent celle du vert. <strong>À IMPLÉMENTER</strong></p>",
    )
    algorithms += algorithm_box(
        "C) Proposé par la caméra",
        "<p>Multiplicateurs stockés dans les métadonnées RAW. <strong>IMPLÉMENTÉ</strong></p>",
    )
    algorithms += algorithm_box(
        "Conversion XYZ",
        "<p>Camera RGB → XYZ via l'inverse normalisée de <code>rgb_xyz_matrix</code>. <strong>IMPLÉMENTÉ</strong></p>",
    )

    content = section("Algorithmes implémentés", algorithms, icon="📘")

    for result in results:
        basename = result["basename"]
        multipliers = result.get("multipliers", {})

        # Tableau des multiplicateurs
        rows = []
        for name, key in [
            ("A) Auto Neutre", "auto_neutral"),
            ("B) Grey World", "grey_world"),
            ("C) Caméra", "camera"),
        ]:
            m = multipliers.get(key, (0, 0, 0))
            status = "✓" if key == "camera" else "À impl."
            rows.append(
                [f"{name} {status}", f"{m[0]:.4f}", f"{m[1]:.4f}", f"{m[2]:.4f}"]
            )

        section_content = subsection(
            "Image originale",
            figure(
                f"{basename}_original.jpg", "Image dématricée sans balance des blancs"
            ),
        )

        section_content += subsection(
            "Multiplicateurs de correction",
            table(["Méthode", "Mult. R", "Mult. G", "Mult. B"], rows),
        )

        section_content += subsection(
            "A) Balance auto neutre",
            figure(
                f"{basename}_auto.jpg",
                "Résultat avec balance des blancs avec auto neutre",
            ),
        )

        section_content += subsection(
            "B) Balance grey_world",
            figure(
                f"{basename}_grey.jpg",
                "Résultat avec balance des blancs avec grey world",
            ),
        )

        section_content += subsection(
            "C) Balance caméra",
            figure(
                f"{basename}_camera.jpg",
                "Résultat avec balance des blancs de la caméra",
            ),
        )

        section_content += subsection(
            "Comparaison",
            figure(
                f"{basename}_comparison.png",
                "Comparaison des méthodes de balance des blancs",
            ),
        )

        section_content += subsection(
            "Conversion XYZ",
            figure(
                f"{basename}_xyz_comparison.png",
                "Images converties en XYZ puis reconverties en sRGB",
            ),
        )

        content += section(basename, section_content)

    html = html_document(
        "TP1 - Section 3",
        "Balance des Blancs (White Balance)",
        "⚪",
        content,
        accent_color="#e94560",
    )

    save_report(html, os.path.join(output_dir, "rapport_section3.html"))


# =============================================================================
# Traitement Principal
# =============================================================================


def process_white_balance(
    input_dir="images_intermediaires_sec2",
    metadata_dir="images_intermediaires_sec1",
    output_dir="images_intermediaires_sec3",
    input_suffix="_bilinear.tiff",
):
    """Traiter toutes les images dématricées et appliquer la balance des blancs."""
    os.makedirs(output_dir, exist_ok=True)

    tiff_files = sorted(glob.glob(os.path.join(input_dir, f"*{input_suffix}")))

    if not tiff_files:
        print(f"Aucun fichier *{input_suffix} trouvé dans {input_dir}/")
        return

    print(f"\n{'#'*60}")
    print("# Section 3: Balance des Blancs")
    print(f"{'#'*60}")
    print(f"\n{len(tiff_files)} fichier(s) TIFF trouvé(s)")

    results = []

    for tiff_path in tiff_files:
        basename = os.path.basename(tiff_path).replace(input_suffix, "")
        json_path = os.path.join(metadata_dir, f"{basename}.json")

        if not os.path.exists(json_path):
            print(f"  Ignoré {basename}: métadonnées non trouvées")
            continue

        print(f"\n{'='*60}")
        print(f"Traitement: {basename}")
        print("=" * 60)

        try:
            image = load_tiff(tiff_path)
            metadata = load_metadata(json_path)

            rgb_xyz_matrix = metadata.get("rgb_xyz_matrix", np.eye(3).tolist())
            camera_wb = metadata.get("camera_whitebalance", [1.0, 1.0, 1.0, 0.0])

            result = {"basename": basename, "multipliers": {}}

            # Sauvegarder l'original
            save_jpeg(image, os.path.join(output_dir, f"{basename}_original.jpg"))

            # A) Sélection automatique de région neutre (à implémenter par l'étudiant)
            print("  [A] Sélection automatique de région neutre...")
            wb_auto, mult_auto, neutral_pos = white_balance_auto_neutral(
                image, region_size=15
            )
            result["multipliers"]["auto_neutral"] = mult_auto
            result["neutral_pos"] = neutral_pos
            save_tiff16(wb_auto, os.path.join(output_dir, f"{basename}_auto.tiff"))
            save_jpeg(wb_auto, os.path.join(output_dir, f"{basename}_auto.jpg"))

            # B) Grey World (à implémenter par l'étudiant)
            print("  [B] Grey World...")
            wb_grey_world, mult_gw = white_balance_grey_world(image)
            result["multipliers"]["grey_world"] = mult_gw
            save_tiff16(wb_grey_world, os.path.join(output_dir, f"{basename}_grey.tiff"))
            save_jpeg(wb_grey_world, os.path.join(output_dir, f"{basename}_grey.jpg"))

            # C) Caméra (implémenté)
            print("  [C] Balance des blancs caméra...")
            wb_camera, mult_cam = white_balance_camera(image, camera_wb)
            result["multipliers"]["camera"] = mult_cam

            save_tiff16(wb_camera, os.path.join(output_dir, f"{basename}_camera.tiff"))
            save_jpeg(wb_camera, os.path.join(output_dir, f"{basename}_camera.jpg"))

            # Conversion XYZ
            print("  Conversion vers XYZ...")
            xyz_camera = camera_rgb_to_xyz(wb_camera, rgb_xyz_matrix)
            save_tiff16(
                np.clip(xyz_camera, 0, 1),
                os.path.join(output_dir, f"{basename}_camera_xyz.tiff"),
            )

            # Figures de comparaison
            comparison = {
                "Original": {"image": image, "multipliers": (1.0, 1.0, 1.0)},
                "Auto Neutre": {"image": wb_auto, "multipliers": mult_auto},
                "Grey World": {"image": wb_grey_world, "multipliers": mult_gw},
                "Caméra": {"image": wb_camera, "multipliers": mult_cam},
                
            }

            create_wb_comparison_figure(
                comparison,
                os.path.join(output_dir, f"{basename}_comparison.png"),
                linear_to_srgb,
                title=f"Balance des Blancs - {basename}",
            )

            xyz_comparison = {"Caméra": {"rgb": wb_camera, "xyz": xyz_camera}}
            create_xyz_comparison_figure(
                xyz_comparison,
                os.path.join(output_dir, f"{basename}_xyz_comparison.png"),
                linear_to_srgb,
                xyz_to_srgb,
                title=f"Conversion XYZ - {basename}",
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
     # Proposed Images
    parser = argparse.ArgumentParser(description="TP1 Section 3: Balance des Blancs")
    parser.add_argument("--input-dir", "-i", default="img/images_intermediaires_sec2")
    parser.add_argument("--metadata-dir", "-m", default="img/images_intermediaires_sec1")
    parser.add_argument("--output-dir", "-o", default="img/images_intermediaires_sec3")
    parser.add_argument(
        "--suffix",
        "-s",
        default="_malvar.tiff",
        help="Suffixe des fichiers à traiter (défaut: _bilinear.tiff)",
    )

    args = parser.parse_args()
    process_white_balance(
        args.input_dir, args.metadata_dir, args.output_dir, args.suffix
    )

   