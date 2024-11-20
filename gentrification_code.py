# Instalar librerías necesarias
!pip install folium pandas numpy -q

import folium
import pandas as pd
import numpy as np
from folium.plugins import HeatMap

# Generar dataset de proyectos de construcción
np.random.seed(42)

num_projects = 500
construction_data = {
    "Nombre del Proyecto": [f"Proyecto {i}" for i in range(1, num_projects + 1)],
    "Latitud": np.random.uniform(4.5, 4.8, num_projects),  # Bogotá
    "Longitud": np.random.uniform(-74.2, -74.0, num_projects),
    "Tipo de Proyecto": np.random.choice(
        ["Parque", "Vía", "Centro Educativo", "Cultural", "Hospital", "Comercial"], num_projects
    ),
    "Impacto Estimado (%)": np.random.randint(5, 30, num_projects),
    "Radio de Influencia (m)": np.random.choice([1000, 1500, 2000, 2500, 3000], num_projects),
}
construction_df = pd.DataFrame(construction_data)

# Generar dataset de churn poblacional
num_zones = 100
churn_data = {
    "Zona": [f"Zona {i}" for i in range(1, num_zones + 1)],
    "Latitud": np.random.uniform(4.5, 4.8, num_zones),  # Bogotá
    "Longitud": np.random.uniform(-74.2, -74.0, num_zones),
    "Tasa de Churn (%)": np.random.uniform(-5, 20, num_zones),  # Negativo: aumento poblacional
}
churn_df = pd.DataFrame(churn_data)

# Combinar los datasets
# Asumimos que una oportunidad es donde el impacto estimado es alto y el churn es bajo o negativo.
opportunity_data = []
for _, project in construction_df.iterrows():
    for _, churn in churn_df.iterrows():
        # Calcular distancia (simulada como cercanía por coordenadas)
        distance = np.sqrt(
            (project["Latitud"] - churn["Latitud"])**2 +
            (project["Longitud"] - churn["Longitud"])**2
        )
        if distance < 0.05:  # Zona de influencia
            opportunity_data.append({
                "Latitud": project["Latitud"],
                "Longitud": project["Longitud"],
                "Impacto Estimado (%)": project["Impacto Estimado (%)"],
                "Tasa de Churn (%)": churn["Tasa de Churn (%)"]
            })

opportunity_df = pd.DataFrame(opportunity_data)

# Crear un mapa con las oportunidades
bogota_map = folium.Map(location=[4.7110, -74.0721], zoom_start=11)

# Agregar oportunidades al mapa
for _, row in opportunity_df.iterrows():
    folium.Circle(
        location=[row["Latitud"], row["Longitud"]],
        radius=300,  # Tamaño del círculo
        color="green" if row["Tasa de Churn (%)"] < 0 else "orange",
        fill=True,
        fill_opacity=0.6,
        popup=(
            f"Impacto Estimado: {row['Impacto Estimado (%)']}%<br>"
            f"Tasa de Churn: {row['Tasa de Churn (%)']}%"
        )
    ).add_to(bogota_map)

# Guardar el mapa en HTML
bogota_map.save("bogota_opportunities_map.html")

# Mostrar el mapa en Google Colab
bogota_map
