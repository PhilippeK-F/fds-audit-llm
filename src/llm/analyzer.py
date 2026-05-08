import os
import time

ANALYSES_SIMULEES = {
    "Degraissant solvant chlore HD": '''1. RESUME EXECUTIF
Ce produit presente des non-conformites majeures au regard de la reglementation REACH et de la directive COV 1999/13/CE. Avec un taux de COV de 118.5 g/L pour un seuil maximal de 30 g/L, et une biodegradabilite de seulement 28%, ce produit represente un risque environnemental et sanitaire significatif.

2. POINTS DE NON-CONFORMITE
- COV : 118.5 g/L soit un depassement de 295% du seuil reglementaire (30 g/L)
- Biodegradabilite : 28% soit 32 points sous le seuil minimum Ecolabel EU (60%)
- Non-conformite REACH : substances prioritaires non declarees
- Ecotoxicite aquatique critique : LC50 = 8.5 mg/L sous le seuil de 10 mg/L
- Absence de certification Ecolabel EU

3. RISQUES IDENTIFIES
- Environnement : contamination des eaux de surface par ruissellement
- Sante : exposition aux vapeurs de dichloromethane, substance CMR suspectee
- Reglementaire : risque de sanction REACH, amende jusqu a 150 000 euros

4. RECOMMANDATIONS
- Remplacer en priorite par un degraissant biosource (ex : CitraClean)
- Mettre en place une ventilation forcee jusqu au remplacement
- Declarer les substances aupres de l ECHA sous 3 mois
- Former les operateurs aux risques specifiques CMR

5. CONCLUSION
Remplacement urgent recommande. Ce produit ne peut etre maintenu dans le referentiel au-dela de 6 mois sous peine de non-conformite reglementaire.''',

    "Degraissant biosorce CitraClean": '''1. RESUME EXECUTIF
Ce produit presente un excellent profil environnemental et reglementaire. Conforme REACH, certifie Ecolabel EU, avec une biodegradabilite de 94% et des COV inferieurs a 1 g/L, il constitue la reference a privilegier dans le referentiel produits.

2. POINTS DE NON-CONFORMITE
Aucune non-conformite identifiee. Tous les indicateurs sont dans les seuils reglementaires.

3. RISQUES IDENTIFIES
- Risque incendie mineur : mention H226 (liquide inflammable) - gestion standard suffisante
- Aucun risque environnemental ou sanitaire significatif identifie

4. RECOMMANDATIONS
- Maintenir ce produit comme reference degraissant dans le referentiel
- Communiquer la certification Ecolabel EU aupres des clients
- Envisager d etendre son usage aux applications haute pression

5. CONCLUSION
Produit recommande. Peut remplacer avantageusement le degraissant solvant chlore sur la majorite des applications industrielles.''',

    "Desinfectant quaternaire QAC-50": '''1. RESUME EXECUTIF
Ce produit est partiellement conforme. Bien qu enregistre sous REACH, il presente des indicateurs environnementaux preoccupants, notamment une ecotoxicite aquatique elevee et une biodegradabilite insuffisante pour l obtention de l Ecolabel EU.

2. POINTS DE NON-CONFORMITE
- Biodegradabilite : 45% sous le seuil Ecolabel EU (60%)
- Ecotoxicite : LC50 = 22 mg/L - classification Aquatic Chronic 2 selon CLP
- Absence de certification Ecolabel EU

3. RISQUES IDENTIFIES
- Environnement : persistance dans les milieux aquatiques, bioaccumulation possible
- Sante : risque de sensibilisation cutanee a forte concentration
- Reglementaire : non eligible aux marches publics exigeant Ecolabel EU

4. RECOMMANDATIONS
- Etudier le remplacement par un desinfectant peroxyde certifie
- Revoir les doses d utilisation pour minimiser l impact environnemental
- Mettre en place un suivi des rejets dans les eaux usees

5. CONCLUSION
Maintien possible a court terme avec mesures correctives. Remplacement recommande a 12 mois.''',

    "Nettoyant HP vert dilution forte": '''1. RESUME EXECUTIF
Produit exemplaire sur tous les criteres reglementaires et environnementaux. Double certification Ecolabel EU et conformite REACH totale. Avec 97% de biodegradabilite et une ecotoxicite quasi nulle (LC50 = 580 mg/L), ce produit represente le standard de reference pour les achats responsables.

2. POINTS DE NON-CONFORMITE
Aucune non-conformite. Produit conforme a 100% des criteres analyses.

3. RISQUES IDENTIFIES
Aucun risque significatif identifie. Produit sur sans equipement de protection specifique.

4. RECOMMANDATIONS
- Etendre l usage de ce produit a toutes les applications compatibles
- Valoriser la double certification dans les reponses aux appels d offres
- Utiliser comme argument commercial aupres des clients sensibles RSE

5. CONCLUSION
Produit hautement recommande. Reference ideale pour une politique d achats eco-responsables.''',

    "Decapant sol industriel": '''1. RESUME EXECUTIF
Ce produit presente les non-conformites les plus critiques du referentiel. Avec 145 g/L de COV, une biodegradabilite de 22% et trois substances SVHC (naphta, xylene, ethylbenzene), il constitue le risque reglementaire et sanitaire le plus eleve de la flotte produits.

2. POINTS DE NON-CONFORMITE
- COV : 145 g/L soit un depassement de 383% du seuil (30 g/L)
- Biodegradabilite : 22% soit 38 points sous le seuil minimum
- Non-conformite REACH : 3 substances SVHC non declarees
- Ecotoxicite critique : LC50 = 6.2 mg/L - classification Aquatic Acute 1
- Mention H304 : danger mortel par ingestion

3. RISQUES IDENTIFIES
- Environnement : impact aquatique severe, persistance elevee
- Sante : exposition aux hydrocarbures aromatiques, risque neurotoxique
- Reglementaire : infraction REACH caracterisee, risque de mise en demeure DREAL

4. RECOMMANDATIONS
- Arreter les commandes immediatement
- Inventorier et securiser les stocks existants
- Declarer les substances SVHC aupres de l ECHA sous 30 jours
- Identifier un produit de substitution enzymatique en urgence

5. CONCLUSION
Retrait immediat du referentiel obligatoire. Ce produit ne peut rester en usage sans exposer l entreprise a des sanctions reglementaires graves.'''
}

def analyser_produit(produit):
    nom = produit["produit"]
    time.sleep(0.5)
    if nom in ANALYSES_SIMULEES:
        return ANALYSES_SIMULEES[nom]
    return "Analyse non disponible pour ce produit."

def analyser_tous(df, fds_simulees):
    print("[analyzer] Analyse simulee de " + str(len(df)) + " produits...")
    resultats = []
    for i, row in df.iterrows():
        print("[analyzer] Analyse : " + row["produit"] + "...")
        fds_data = fds_simulees[i].copy()
        fds_data["score_conformite"] = row["score_conformite"]
        fds_data["niveau_risque"] = row["niveau_risque"]
        fds_data["nb_alertes"] = row["nb_alertes"]
        analyse = analyser_produit(fds_data)
        resultats.append({
            "produit": row["produit"],
            "score_conformite": row["score_conformite"],
            "niveau_risque": row["niveau_risque"],
            "analyse_llm": analyse
        })
        print("[analyzer] OK - score : " + str(row["score_conformite"]) + "/100")
    return resultats
