
import glob
import os


from tp1_rapport import (
    section,
    subsection,
    figure,
    table, 
    comparison_grid,
)



def generate_personnal_images_content(basenames, sec1_dir, sec2_dir, sec3_dir, sec4_dir, results):
 
    content = ""
    # =============================================================================
    # SECTION 6.1: Chargement et Compréhension des Données RAW
    # =============================================================================
    sec1_content = ""  

    # Texte d'introduction pour la section 1
    sec1_content += subsection(
        "Introduction",
        '<div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4fc3f7;">'

        '<p>'
        'Les images brutes ont été capturées à l’aide d’un téléphone Samsung S10. '
        'Les caractéristiques de la caméra ont été extraites directement à partir des métadonnées des fichiers RAW. '
        'Le capteur utilise un filtre de Bayer de type GRBG et fournit des données avec une profondeur de 10 bits, correspondant à des valeurs comprises entre 0 et 1023. '
        'Les métadonnées indiquent un niveau de noir égal à 64 et un niveau de saturation à 1023 pour l’ensemble des canaux. '
        'La résolution des images est de 4032 × 3024 pixels'
        '</p>'

        '<p>'
        'Nous avons capturé trois images brutes avec l’application Lightroom en format DNG. Une image correspond à une scène fortement éclairée, où le soleil émet une très grande quantité de lumière vers la caméra. '
        'Une autre capture une scène extérieure avec un éclairage faible (ombre en soirée), et la dernière correspond à une scène intérieure très peu éclairée.'
        'Les resultats sont presentés ci-dessous. '
        '</p>'

        '</div>'
    )
    
    for basename in basenames:
        sec1_img_content = ""
        
        # Figure: Zoom sur la mosaïque Bayer
        zoom_path = os.path.join(sec1_dir, f"{basename}_zoom16x16.png")
        if os.path.exists(zoom_path):
            sec1_img_content += subsection(
                f"Région 16×16 de la mosaïque - {basename}",
                figure(f"img/images_intermediaires_sec1/{basename}_zoom16x16.png",
                       "Zoom sur une région 16×16 montrant les valeurs normalisées et le motif de Bayer coloré.")
            )
        
        if sec1_img_content:
            sec1_content += section(f"Image: {basename}", sec1_img_content)
    
    
    content += section("Section 6.1: Chargement et Compréhension des Données RAW", sec1_content, icon="📷")
    
    # =============================================================================
    # SECTION 2: Dématriçage (Demosaicking)
    # =============================================================================
    sec2_content = ""
    
    
    
    for basename in basenames:
        sec2_img_content = ""
        
        # Figure: Comparaison des méthodes
        comp_path = os.path.join(sec2_dir, f"{basename}_comparison.png")
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
    
    
    
    content += section("Section 6.2: Dématriçage (Demosaicking)", sec2_content, icon="🎨")
    
    # =============================================================================
    # SECTION 3: Balance des Blancs (White Balance)
    # =============================================================================
    sec3_content = ""
    
    
    for basename in basenames:
        sec3_img_content = ""
        
        # Figure: Comparaison des méthodes
        comp_path = os.path.join(sec3_dir, f"{basename}_comparison.png")
        if os.path.exists(comp_path):
            sec3_img_content += subsection(
                f"Comparaison des méthodes - {basename}",
                figure(f"img/images_intermediaires_sec3/{basename}_comparison.png",
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
    
    
    content += section("Section 6.3: Balance des Blancs (White Balance)", sec3_content, icon="⚪")
    
    # =============================================================================
    # SECTION 4: Mappage Tonal et Encodage d'Affichage
    # =============================================================================
    sec4_content = ""
    
    # Figure: Courbes de mappage tonal
    curves_path = os.path.join(sec4_dir, "tonemapping_curves.png")
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
    
    
    
    content += section("Section 6.4: Mappage Tonal et Encodage d'Affichage", sec4_content, icon="🎨")
    
    # =============================================================================
    # GRILLE DE COMPARAISON DES IMAGES FINALES
    # =============================================================================
    # Collecter toutes les images finales JPG de la section 4 et leurs références
    comparisons = []
    jpg_files = sorted(glob.glob(os.path.join(sec4_dir, "*_final.jpg")))
    
    for jpg_path in jpg_files:
        basename = os.path.basename(jpg_path).replace("_final.jpg", "")
        if basename.startswith('LRM'):
            final_src = os.path.basename(jpg_path)
            final_src = os.path.join(sec4_dir, final_src)
            # Chercher l'image de référence correspondante
            reference_src = None
            srgb_path = os.path.join(sec1_dir, f"{basename}_srgb.jpg")
            if os.path.exists(srgb_path):
                reference_src = f"img/images_intermediaires_sec1/{basename}_srgb.jpg"
            #breakpoint()
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
    
    
    final_content = section("Section 6: Images Personnelles", content, icon="📝")
    return final_content