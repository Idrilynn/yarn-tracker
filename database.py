import sqlite3

connection = sqlite3.connect('yarn.db')
connection.execute('''CREATE TABLE IF NOT EXISTS catalogue (
                        id TEXT PRIMARY KEY,                     -- référence unique du type de pelote
                        picture TEXT,                            -- nom du fichier image
                        brand_name TEXT NOT NULL COLLATE NOCASE, -- marque
                        yarn_name TEXT NOT NULL COLLATE NOCASE,  -- gamme
                        length REAL NOT NULL,                    -- longueur (en mètres)
                        weight REAL NOT NULL,                    -- poids (en grammes)
                        weight_cat TEXT,                         -- catégorie de fil
                        colour_id TEXT NOT NULL COLLATE NOCASE,  -- référence de la couleur
                        colour_type TEXT NOT NULL,               -- unie ou gradient
                        colour TEXT NOT NULL,                    -- couleur
                        fibers TEXT,                             -- matière
                        texture TEXT,                            -- structure du fil    
                        place TEXT,                              -- lieu de rangement
                        where_to_order TEXT,                     -- commander le fil
                        modified_at TEXT,                        -- date de modification
                        UNIQUE (brand_name, yarn_name, colour_id)-- une seule entrée par combinaison marque + gamme + couleur
                     )
                  ''')

connection.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id TEXT PRIMARY KEY,        -- référence unique de la pelote
                        catalogue_id TEXT NOT NULL, -- identifiant du catalogue
                        weight_init REAL NOT NULL,  -- poids (en grammes) à l'achat
                        weight_remain REAL NOT NULL,-- poids (en grammes) restant
                        dye_lot TEXT,               -- bain 
                        added_at TEXT,              -- date d'achat 
                        status TEXT NOT NULL,       -- statut
                        modified_at TEXT,           -- date de modification
    
                        FOREIGN KEY (catalogue_id) REFERENCES catalogue(id)
                     )
                  ''')

connection.execute('''CREATE TABLE IF NOT EXISTS usage (
                        id TEXT PRIMARY KEY,           -- identifiant unique de la sortie
                        inventory_id TEXT NOT NULL,    -- pelote sortie
                        taken_at TEXT NOT NULL,        -- date de sortie
                        returned_at TEXT,              -- date de retour (vide tant que la pelote est utilisée)
                        weight_before REAL NOT NULL,   -- poids (en grammes) à la sortie
                        weight_after REAL,             -- poids (en grammes) au retour (vide tant qu'elle n'est pas revenue)
                        modified_at TEXT,              -- date de modification

                        FOREIGN KEY (inventory_id) REFERENCES inventory(id)
                     )
                  ''')
connection.commit()
connection.close()