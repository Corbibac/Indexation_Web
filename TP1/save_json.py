import os
import json


def save_results_to_json(data, output_file, overwrite=False):
    """Enregistre les données extraites dans un fichier JSON.

    - Si output_file existe déjà et que `overwrite=False`, lève une erreur.
    - Si output_file existe et que `overwrite=True`, le fichier est écrasé.
    """
    if os.path.exists(output_file) and not overwrite:
        raise FileExistsError(
            f"Le fichier '{output_file}' existe déjà. "
            "Utilisez `overwrite=True` pour l'écraser."
        )

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Résultats sauvegardés dans '{output_file}'.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des résultats : {e}")
