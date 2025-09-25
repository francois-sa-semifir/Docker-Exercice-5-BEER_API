from flask import jsonify, render_template
from sqlalchemy import text
from app import db

class BeerController:
    def getBeers(self):
        try:
            sql = text("""
                SELECT nom_article, nom_marque, volume, titrage, prix_achat, nom_couleur, nom_type
                FROM article AS a
                INNER JOIN marque AS m USING (id_marque)
                INNER JOIN couleur AS c USING (id_couleur)
                INNER JOIN type AS t USING (id_type)
            """)
            rows = db.session.execute(sql).fetchall()
            beers = []
            for r in rows:
                beers.append({
                    'nom_article': r[0],
                    'nom_marque':  r[1],
                    'volume':      int(r[2]) if r[2] is not None else None,
                    'titrage':     float(r[3]) if r[3] is not None else None,
                    'prix_ht':     float(r[4]) if r[4] is not None else None,
                    'prix_15':     (float(r[4]) * 1.15) if r[4] is not None else None,
                    'couleur':     r[5],
                    'type':        r[6],
                })
            return jsonify(beers)
        except Exception as e:
            print(e)
            return jsonify({'error': 'getBeers failed'}), 500

    def getCAByFabricant(self):
        try:
            sql = text("""
                SELECT fab.NOM_FABRICANT, SUM(ROUND(a.Prix_achat*v.quantite,2)) AS CA
                FROM beer.ventes AS v
                INNER JOIN beer.article a ON v.ID_ARTICLE=a.ID_ARTICLE
                INNER JOIN beer.marque f ON a.ID_MARQUE=f.ID_MARQUE
                INNER JOIN beer.fabricant fab ON f.ID_FABRICANT=fab.ID_FABRICANT
                GROUP BY fab.NOM_FABRICANT
            """)
            rows = db.session.execute(sql).fetchall()
            return jsonify([
                {'nom': r[0], 'CA': round(float(r[1]) * 1.15, 2) if r[1] is not None else None}
                for r in rows
            ])
        except Exception as e:
            print(e)
            return jsonify({'error': 'getCAByFabricant failed'}), 500

    def getVariation(self):
        try:
            sql = text("""
                SELECT NOM_ARTICLE, qte15, qte16,
                       ((qte16 - qte15) / qte15 * 100) AS variation
                FROM article AS a
                INNER JOIN (
                    SELECT id_article AS id15, SUM(quantite) AS qte15
                    FROM ventes WHERE annee = 2015 GROUP BY id_article
                ) AS r15
                INNER JOIN (
                    SELECT id_article AS id16, SUM(quantite) AS qte16
                    FROM ventes WHERE annee = 2016 GROUP BY id_article
                ) AS r16
                ON  a.id_article = r15.id15
                AND r15.id15 = r16.id16
                AND a.id_article = r16.id16
                HAVING variation BETWEEN -1 AND 1;
            """)
            rows = db.session.execute(sql).fetchall()
            return jsonify([
                {
                    'nom': r[0],
                    'vente_2015': int(r[1]) if r[1] is not None else None,
                    'vente_2016': int(r[2]) if r[2] is not None else None,
                    'variation': float(r[3]) if r[3] is not None else None,
                } for r in rows
            ])
        except Exception as e:
            print(e)
            return jsonify({'error': 'getVariation failed'}), 500

    def doc(self):
        return render_template("doc.html")
