# transform-path-audit

## Français

Vérifier les cycles et âges des transformations rigides 3D.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m transform_path_audit examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Compose les transformations rigides 3D et leurs inverses, puis compare les chemins alternatifs dans la composante de référence. Rejette les observations périmées/futures avant connexion ; produit les chemins témoins des incohérences.

### Limites

Snapshots fournis, quaternion w/x/y/z unitaire, tolérances déclarées. Ne remplace pas tf2, ne traite pas l’interpolation temporelle ni les composantes non connectées ; sans ROS ou robot natif.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Check cycles and ages of rigid 3D transforms.

Synthetic data; no network access or secret required.

```sh
python -m transform_path_audit examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Composes rigid 3D transforms and inverses, comparing alternate paths in the reference component. Rejects stale/future observations before connecting frames and produces path witnesses for inconsistencies.

### Limits

Supplied snapshots, unit w/x/y/z quaternion, declared tolerances. Does not replace tf2, interpolate time or validate disconnected components; no native ROS or robot.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Comprobar ciclos y edades de transformaciones rígidas 3D.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m transform_path_audit examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Compone transformaciones rígidas 3D e inversas y compara caminos alternativos en la componente de referencia. Rechaza observaciones antiguas/futuras antes de conectar y produce caminos testigo de incoherencias.

### Límites

Snapshots dados, cuaternión unitario w/x/y/z y tolerancias declaradas. No sustituye tf2, interpola tiempo ni valida componentes desconectadas; sin ROS ni robot nativo.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://github.com/ros2/geometry2
