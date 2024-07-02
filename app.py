# Importar bibliotecas necesarias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
# Configuración de la página de Streamlit
st.set_page_config(page_title='Dashboard residuos municipales', page_icon="🌎", initial_sidebar_state="expanded", layout='wide')
# Estilos en formato HTML para el texto
text_style = """
    <style>
        .title_text {
            font-size: 24px; font-family: "Times New Roman", Georgia, serif;
            font-weight: bold;
        }
        .desc_text {
            font-size: 24px; font-family: "Times New Roman", Georgia, serif;
            text-align: justify;
        }
    </style>
"""
st.markdown(text_style, unsafe_allow_html=True)
# Título principal del Dashboard
st.markdown("<h3 class='title_text'>Residuos municipales (2014-2021)<h3>" , unsafe_allow_html=True)
# Cargar el archivo CSV en un DataFrame
@st.cache_data
def load_data():
    file_path = 'residuos_municipales.csv'
    df = pd.read_csv(file_path, encoding="latin1", delimiter=";", index_col=0)
    df["PERIODO"] = df["PERIODO"].astype(int)
    return df

df = load_data()

@st.cache_data
def process_data(df):
    # Group by DEPARTAMENTO and PERIODO and sum QRESIDUOS_MUN
    df_grouped = df.groupby(['DEPARTAMENTO', 'PERIODO'])['QRESIDUOS_MUN'].sum().reset_index()
    return df_grouped

# Función para generar el primer gráfico
def do_chart1():
    global df
    count_by_periodo = df.groupby("PERIODO")["QRESIDUOS_MUN"].count().reset_index()
    fig = go.Figure()
    # Crear un gráfico de pastel (donut chart) utilizando plotly.express
    fig.add_trace(go.Pie(
        labels=count_by_periodo["PERIODO"],
        values=count_by_periodo["QRESIDUOS_MUN"],
        texttemplate="%{label}<br>%{percent:.2%}",
        hole=0.6,
        showlegend=True,
        hovertemplate="<b>Año</b>: %{label}<br>"
                      "<b>Total</b>: %{value:.0f}<br>"
                      "<b>Porcentaje</b>: %{percent:.2%}<br>"
                      "<extra></extra>",
        textinfo='percent+value',
        pull=[0.1] * len(count_by_periodo),
        marker=dict(colors=px.colors.qualitative.Set3),
    ))
    fig.add_annotation(
        text="RESIDUOS MUNICIPALES",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20)
    )
    fig.update_layout(
        title="Residuos municipales Ton/Año | 2014 - 2021",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Arial", size=12, color="black"),
    )
    st.plotly_chart(fig, use_container=True)
    st.markdown("*Gráfica 1: El gráfico representa la proporción expresada en porcentajes de la cantidad de residuos sólidos domiciliarios por año*")
    st.info('En la gráfica se logra observar la comparación de la cantidad de residuos sólidos domiciliarios que fueron registrados durante el periodo 2019 al 2022 y la proporción que representan respecto al 100% del total de los datos registrados, de los cuales se puede destacar que el año 2019 y 2020 tienen un porcentaje igual de distribución y lo mismo se logra observar para los años 2021 y 2022, pero es importante destacar que los 2 últimos años del periodo fueron los que mayor porcentaje de residuos sólidos domiciliarios registraron. ', icon="😀")
# Función para generar el segundo gráfico
def do_chart2():
    sum_residuos_urbanos = df.groupby("DEPARTAMENTO")["QRESIDUOS_MUN"].sum().reset_index()
    sum_residuos_urbanos.rename(columns={"QRESIDUOS_MUN": "Residuos Municipales"}, inplace=True)
    fig = px.scatter(sum_residuos_urbanos, x="DEPARTAMENTO", y="Residuos Municipales",
                    size="Residuos Municipales", color="DEPARTAMENTO",
                    hover_name="DEPARTAMENTO", title="Residuos Municipales Ton/Año por Departamento",
                    labels={"Residuos Domiciliarios": "Residuos Municipales", "DEPARTAMENTO": "Departamento"},
                    size_max=60,
                    color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_yaxes(title_text="Residuos Municipales 2014 - 2021")
    fig.update_layout(xaxis_tickangle=-45)
    fig.update_layout(
        xaxis=dict(title='Departamento'),
        yaxis=dict(title='Residuos Municipales 2014 - 2021'),
        template="plotly_dark",
        font=dict(family="Arial", size=12, color="white"),
    )
    st.plotly_chart(fig)
    st.markdown("*Gráfica 2: El gráfico representa los residuos Municipales por departamento expresada en millones de toneladas*")
    st.warning('En el gráfico presentado podemos observar que  en  la capital del Perú Lima, es una de las ciudades más urbanizadas , de igual forma la más poblada del país y, por lo tanto, genera una gran cantidad de residuos sólidos domiciliarios.  ', icon="😀")
# Función para generar el tercer gráfico
def do_chart3():
    # Process data
    df_grouped = process_data(df)
    # Create the line chart using Plotly with markers
    fig = px.line(df_grouped, x='DEPARTAMENTO', y='QRESIDUOS_MUN', color='PERIODO', title='QRESIDUOS_MUN by DEPARTAMENTO and PERIODO', markers=True)
    # Update traces to customize markers and lines
    fig.update_traces(marker=dict(size=10, symbol='circle', line=dict(width=2, color='DarkSlateGrey')),
                    line=dict(width=2))

    # Update layout for advanced styling
    fig.update_layout(
        yaxis=dict(
            tickmode='linear',
            dtick=10,  # Increase this value to add more space between ticks
            range=[df_grouped['QRESIDUOS_MUN'].min() - 10, df_grouped['QRESIDUOS_MUN'].max() + 10],
            title='QRESIDUOS_MUN',
            gridcolor='LightGray'
        ),
        xaxis=dict(
            title='DEPARTAMENTO',
            gridcolor='LightGray'
        ),
        title=dict(
            text='QRESIDUOS_MUN by DEPARTAMENTO and PERIODO',
            x=0.5,
            xanchor='center',
            font=dict(size=14)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=50),
        legend=dict(
            title='PERIODO',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    # Display the chart in Streamlit
    st.title("QRESIDUOS_MUN by DEPARTAMENTO and PERIODO")
    st.plotly_chart(fig)
    st.markdown("*Gráfica 3: La gráfica muestra la diferencia de consumos de residuos sólidos domiciliarios por departamento con su respectiva región.*")
    st.info('Tener en cuenta que el territorio  peruano está dividido en 3 regiones naturales: costa, sierra y selva. Esta división se basa en las características topográficas y climáticas de cada región,es por ello, que en la gráfica se puede apreciar que el mismo departamento se encuentra en diferentes regiones. Por ejemplo, el departamento de Piura que se encuentra ubicado en la zona norte del país, está distribuido geográficamente en la costa y sierra, como consecuencia se pueden apreciar playas, ríos y montañas dentro de un mismo territorio.', icon="🔎")
# Función para generar el cuarto gráfico    
def do_chart4():
    # Access the DataFrame from session state
    saved_df = st.session_state['df_guardado']
    # Definir las categorías de residuos
    # categorias_organicos = ["QRESIDUOS_ALIMENTOS", "QRESIDUOS_MALEZA", "QRESIDUOS_OTROS_ORGANICOS"]
    # categorias_inorganicos = ["QRESIDUOS_PAPEL_BLANCO", "QRESIDUOS_PAPEL_PERIODICO", "QRESIDUOS_PAPEL_MIXTO",
    #                         "QRESIDUOS_CARTON_BLANCO", "QRESIDUOS_CARTON_MARRON", "QRESIDUOS_CARTON_MIXTO",
    #                         "QRESIDUOS_VIDRIO_TRANSPARENTE", "QRESIDUOS_VIDRIO_OTROS_COLORES", "QRESIDUOS_VIDRIOS_OTROS",
    #                         "QRESIDUOS_TEREFLATO_POLIETILENO", "QRESIDUOS_POLIETILENO_ALTA_DENSIDAD",
    #                         "QRESIDUOS_POLIETILENO_BAJA_DENSIDAD", "QRESIDUOS_POLIPROPILENO", "QRESIDUOS_POLIESTIRENO",
    #                         "QRESIDUOS_POLICLORURO_VINILO", "QRESIDUOS_TETRABRICK", "QRESIDUOS_LATA", "QRESIDUOS_METALES_FERROSOS",
    #                         "QRESIDUOS_ALUMINIO", "QRESIDUOS_OTROS_METALES"]
    # categorias_no_aprovechables = ["QRESIDUOS_BOLSAS_PLASTICAS", "QRESIDUOS_TECNOPOR", "QRESIDUOS_INERTES",
    #                                 "QRESIDUOS_TEXTILES", "QRESIDUOS_CAUCHO_CUERO", "QRESIDUOS_MEDICAMENTOS",
    #                                 "QRESIDUOS_ENVOLTURAS_SNAKCS_OTROS", "QRESIDUOS_OTROS_NO_CATEGORIZADOS"]
    # categorias_peligrosos = ["QRESIDUOS_SANITARIOS", "QRESIDUOS_PILAS"]
    # # Calcular las sumas consolidadas para cada categoría
    # saved_df["ORGANICOS"] = saved_df[categorias_organicos].sum(axis=1)
    # saved_df["INORGANICOS"] = saved_df[categorias_inorganicos].sum(axis=1)
    # saved_df["NO_APROVECHABLES"] = saved_df[categorias_no_aprovechables].sum(axis=1)
    # saved_df["PELIGROSOS"] = saved_df[categorias_peligrosos].sum(axis=1)
    # # Realizar la sumatoria por categoría y departamento
    # sum_by_department = saved_df.groupby("DEPARTAMENTO")["ORGANICOS", "INORGANICOS", "NO_APROVECHABLES", "PELIGROSOS"].sum()
    # # Mostrar los resultados en una tabla
    # st.write("**Suma de Residuos por Categoría y Departamento:**")
    # st.dataframe(sum_by_department)
    # # Reorganizar los datos para el gráfico de barras
    # sum_by_department_melted = sum_by_department.reset_index().melt(id_vars=["DEPARTAMENTO"],
    #                                                                 value_vars=["ORGANICOS", "INORGANICOS", "NO_APROVECHABLES", "PELIGROSOS"],
    #                                                                 var_name="Categoría", value_name="Suma de Residuos")
    # # Crear el gráfico de barras vertical
    # fig = px.bar(sum_by_department_melted, x="DEPARTAMENTO", y="Suma de Residuos", color="Categoría",
    #             title="Residuos en Ton/Año (Toneladas por años) por clasificación y departamento",
    #             labels={"Suma de Residuos": "Suma de Residuos", "DEPARTAMENTO": "Departamento"},
    #             color_discrete_map={"ORGANICOS": "lime", "INORGANICOS": "black", "NO_APROVECHABLES": "purple", "PELIGROSOS": "red"},
    #             )
    # # Agregar etiquetas de texto con el conteo total abreviado
    # for i, departamento in enumerate(sum_by_department_melted["DEPARTAMENTO"].unique()):
    #     total_count = sum_by_department_melted[sum_by_department_melted["DEPARTAMENTO"] == departamento]["Suma de Residuos"].sum()
    #     total_count_abbr = '{:,.0f}K'.format(total_count / 1000)  # Formato abreviado en K
    #     fig.add_annotation(
    #         go.layout.Annotation(
    #             x=departamento,
    #             y=total_count,
    #             text=total_count_abbr,
    #             showarrow=True,
    #             arrowhead=4,
    #             arrowcolor="teal",
    #             arrowsize=1,
    #             arrowwidth=2,
    #             ax=0,
    #             ay=-40,
    #             bgcolor="rgba(255, 255, 255, 0.6)",
    #         )
    #     )
    # # Estilo adicional
    # fig.update_layout(
    #     xaxis=dict(title='Departamento'),
    #     yaxis=dict(title='Suma de Residuos'),
    #     legend=dict(title="Categoría"),
    # )
    # # Mostrar el gráfico
    # st.plotly_chart(fig)
    st.markdown("*La gráfica muestra la cantidad de consumo de residuos sólidos con su respectiva clasificación.*")
    st.info('''Según el Ministerio del Ambiente los residuos sólidos orgánicos se dividen en 34 tipos, en los cuales se pueden clasificar en cuatro grandes grupos: orgánicos, inorgánicos, no aprovechables y peligrosos. Dicha gráfica tiene la facilidad de identificar qué categoría prevalece más, es decir, que conjunto de residuos es más consumido en cada departamento.

**Orgánicos:** Son aquellos desechos biodegradables de origen vegetal o animal que pueden descomponerse en la naturaleza sin demasiada dificultad y transformarse en otro tipo de materia orgánica , 

**Inorgánicos:** Son aquellos desechos no biodegradables o degradables a muy largo plazo que se derivan de procesos antropogénicos (generados por el ser humano).

**No aprovechables:** Son aquellos desechos que no pueden ser reutilizados, reciclados o transformados en otros productos.

**Peligrosos:** Son aquellos residuos que, debido a sus propiedades corrosivas, explosivas, tóxicas, inflamables o radiactivas, pueden causar daños o efectos indeseados a la salud o al ambiente.
''', icon="🔎")
# Función para generar el quinto gráfico
def do_chart5():
    # Multiplicar las columnas para obtener "RESIDUOS URBANA" y "RESIDUOS RURAL"
    saved_df = st.session_state['df_guardado']
    # saved_df["RESIDUOS URBANA"] = saved_df["POB_URBANA"] * saved_df["GPC_DOM"]
    # saved_df["RESIDUOS RURAL"] = saved_df["POB_RURAL"] * saved_df["GPC_DOM"]
    # # Agrupar por departamento y sumar las columnas
    # count_residuos = saved_df.groupby("DEPARTAMENTO")["RESIDUOS URBANA", "RESIDUOS RURAL"].sum().reset_index()
    # # Reorganizar los datos para el gráfico de barras multivariable
    # count_residuos_melted = count_residuos.melt(id_vars=["DEPARTAMENTO"],
    #                                             value_vars=["RESIDUOS URBANA", "RESIDUOS RURAL"],
    #                                             var_name="Tipo de Residuos", value_name="Cantidad")
    # # Crear el gráfico de barras multivariable con texto personalizado
    # fig = px.bar(count_residuos_melted, x="DEPARTAMENTO", y="Cantidad", color="Tipo de Residuos",
    #             title="Residuos sólidos Urbanos y rurales por departamento en Kg/Hab/día: Kilogramo por habitante día",
    #             labels={"Cantidad": "Cantidad de Residuos", "DEPARTAMENTO": "Departamento"},
    #             color_discrete_map={"RESIDUOS URBANA": "darkslategray", "RESIDUOS RURAL": "lime"},
    #             text="Cantidad",
    #             )
    # # Establecer el formato de texto personalizado con abreviación K
    # fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    # # Estilo adicional
    # fig.update_layout(
    #     xaxis=dict(title='Departamento'),
    #     yaxis=dict(title='Cantidad de Residuos'),
    #     legend=dict(title="Tipo de Residuos"),
    # )

    # # Mostrar el gráfico
    # st.plotly_chart(fig)
    st.markdown("*Gráfica 5:  El gráfico representa  la cantidad de consumo de residuos en la zona urbana y rural en su respectivo departamento.*")
    st.success(
    """
    En la gráfica se logra observar que la mayoría de los residuos sólidos que provienen de las zonas urbanas es en mayor cantidad con respecto a los residuos de las zonas rurales, factores como la densidad de población y estilo de vida son los responsables de dichos resultados. Por ejemplo, en las zonas urbanas las personas tienden a consumir más productos desechables envasados, generando así que la cantidad de residuos sólidos aumente, a diferencia de la población en las zonas rurales quienes tiende a consumir más productos frescos y a granel, permitiendo que la cantidad de residuos sólidos se reduzca.
    """, icon='🔎')
# Función para mostrar información sobre el proyecto
def do_acerca():
    st.image('basura.jpg', caption="Basura en la playa", use_column_width=True)
    st.link_button("Ir a código del proyecto", "https://github.com/summermp/streamlit", type='primary')
    st.markdown("""
<p class='desc_text'> La base de datos de composición de residuos sólidos Municipales corresponde a la información sobre la distribución de los residuos sólidos del ámbito domiciliario generados por tipo (medido en tonelada). Dicha información, fue obtenida desde los años 2014 hasta el 2021, con respecto a todos los departamentos de nuestro país.</br></br>
La información que se toma de insumo para la estimación de esta estadística es obtenida a partir de dos fuentes de información: </br></br>
Sistema de Información para la Gestión de los Residuos Sólidos – SIGERSOL el cual es administrado por el Ministerio del Ambiente (MINAM).</br></br>
Los Estudios de caracterización de residuos sólidos municipales, que se estandarizaron desde el año 2014 en adelante, aprobada mediante Resolución Ministerial N° 457-2018-MINAM.</p>
<h4 class='title_text'>¿Qué buscamos?</h4>
<p class='desc_text'>Buscamos brindar información sobre la distribución de los residuos sólidos en el ámbito domiciliario en todos los departamentos del Perú; facilitando su uso mediante gráficas y tablas para un mejor entendimiento.</p>
<h4 class='title_text'>¿Qué son los residuos sólidos domiciliarios?</h4>
<p class='desc_text'>Residuos sólidos domiciliarios son aquellos provenientes del consumo o uso de un bien o servicio, comprenden específicamente como fuente de generación a las viviendas.</p>
<h4 class='title_text'>¿Cómo influyen los residuos sólidos en los seres vivos?</h4>
<p class='desc_text'>De acuerdo a su clasificación y aprovechamiento estos residuos domiciliarios pueden influir tanto positiva como negativamente, por ejemplo, el uso irresponsable y excesivo de plástico, pilas y/o baterías podría ser muy perjudicial para los seres vivos y al ambiente, ya que estos son residuos que podrían <b>tomarse entre 100 a 1000 años en descomponerse</b>, generando así un rastro tóxico a largo plazo en nuestro ecosistema. Por otra parte, el aprovechamiento responsable y creativo de los residuos domiciliarios, tales como la materia orgánica, el papel y el cartón permiten fomentar el reciclaje y crear nuevos productos que sean en beneficio para los seres vivos y el ambiente, por ejemplo, la descomposición de la materia orgánica podría ser fuente de compostaje para las plantas.</p>
""",  unsafe_allow_html=True)
# Función para mostrar información de nosotros
def do_nosotros():
    # st.markdown("<h4 class='title_text'>¿Quiénes somos?</h4>", unsafe_allow_html=True)
    st.markdown("<p class='desc_text'>Somos estudiantes del quinto semestre de la carrera de ingeniería ambiental de la Universidad Peruana Cayetano Heredia (UPCH). Nos apasiona el procesamiento y visualización de datos para mejorar y comprender la problemática ambiental y brindar información sobre los residuos sólidos generados en el Perú.</p>", unsafe_allow_html=True)
    st.image('equipo.jpg', caption="Equipo Ing. Ambiental", use_column_width=True)
# Definición de estilos para la interfaz gráfica
# Estilo del contenedor principal
styles = {
    "container": {
        "margin": "0px !important",  # Márgenes del contenedor
        "padding": "0 !important",  # Relleno del contenedor
        "align-items": "stretch",  # Alineación de los elementos dentro del contenedor
        "background-color": "#fafafa"  # Color de fondo del contenedor
    },
    # Estilo para los iconos
    "icon": {
        "color": "black",  # Color del icono
        "font-size": "20px"  # Tamaño de fuente del icono
    }, 
    # Estilo para los enlaces de navegación
    "nav-link": {
        "font-size": "20px",  # Tamaño de fuente del enlace
        "text-align": "left",  # Alineación del texto a la izquierda
        "margin": "0px",  # Márgenes del enlace
        "--hover-color": "#fafa"  # Color al pasar el mouse sobre el enlace
    },
    # Estilo para el enlace de navegación seleccionado
    "nav-link-selected": {
        "background-color": "#ff4b4b",  # Color de fondo del enlace seleccionado
        "font-size": "20px",  # Tamaño de fuente del enlace seleccionado
        "font-weight": "normal",  # Grosor de la fuente (normal en este caso)
        "color": "black",  # Color del texto del enlace seleccionado
    },
}
# Estructura del menú
menu = {
    'title': 'Menu principal',  # Título del menú principal
    'items': { 
        'Inicio' : {  # Primer elemento del menú principal
            'action': None,  # Acción a realizar al seleccionar este elemento (None indica ninguna acción)
            'item_icon': 'house',  # Ícono asociado al elemento ('house' en este caso)
            'submenu': {  # Submenú asociado al elemento 'Inicio'
                'title': None,  # Título del submenú (None indica sin título)
                'items': {  # Elementos del submenú
                    'Gráfico 1' : {'action': do_chart1, 'item_icon': 'pie-chart-fill', 'submenu': None},  # Elemento 1 del submenú
                    'Gráfico 2' : {'action': do_chart2, 'item_icon': 'bar-chart-fill', 'submenu': None},  # Elemento 2 del submenú
                    'Gráfico 3' : {'action': do_chart3, 'item_icon': 'bar-chart-line', 'submenu': None},  # Elemento 3 del submenú
                    'Gráfico 4' : {'action': do_chart4, 'item_icon': 'bar-chart-line-fill', 'submenu': None},  # Elemento 4 del submenú
                    'Gráfico 5' : {'action': do_chart5, 'item_icon': 'bar-chart-steps', 'submenu': None},  # Elemento 5 del submenú
                },
                'menu_icon': None,  # Ícono asociado al submenú (None indica sin ícono)
                'default_index': 0,  # Índice predeterminado al cargar el submenú
                'with_view_panel': 'main',  # Indica dónde mostrar el contenido del submenú (en el área principal)
                'orientation': 'horizontal',  # Orientación del submenú (horizontal en este caso)
                'styles': styles  # Estilos del submenú
            }
        },
        'Acerca' : {  # Segundo elemento del menú principal
            'action': do_acerca,  # Acción a realizar al seleccionar este elemento (do_acerca en este caso)
            'item_icon': 'info-square',  # Ícono asociado al elemento ('info-square' en este caso)
             'submenu': {  # Submenú asociado al elemento 'Acerca'
                'title': None,  # Título del submenú (None indica sin título)
                'items': {  # Elementos del submenú
                    'Definición' : {'action': None, 'item_icon': '-', 'submenu': None},  # Elemento 1 del submenú
                },
                'menu_icon': None,  # Ícono asociado al submenú (None indica sin ícono)
                'default_index': 0,  # Índice predeterminado al cargar el submenú
                'with_view_panel': 'main',  # Indica dónde mostrar el contenido del submenú (en el área principal)
                'orientation': 'horizontal',  # Orientación del submenú (horizontal en este caso)
                'styles': styles  # Estilos del submenú
            }
        },
        'Nosotros' : {  # Tercer elemento del menú principal
            'action': None,  # Acción a realizar al seleccionar este elemento (None indica ninguna acción)
            'item_icon': 'people',  # Ícono asociado al elemento ('people' en este caso)
            'submenu': {  # Submenú asociado al elemento 'Nosotros'
                'title': None,  # Título del submenú (None indica sin título)
                'items': {  # Elementos del submenú
                    '¿Quiénes somos?' : {'action': do_nosotros, 'item_icon': '-', 'submenu': None}  # Elemento 1 del submenú
                },
                'menu_icon': None,  # Ícono asociado al submenú (None indica sin ícono)
                'default_index': 0,  # Índice predeterminado al cargar el submenú
                'with_view_panel': 'main',  # Indica dónde mostrar el contenido del submenú (en el área principal)
                'orientation': 'horizontal',  # Orientación del submenú (horizontal en este caso)
                'styles': styles  # Estilos del submenú
            }
        },
    },
    'menu_icon': 'clipboard2-check-fill',  # Ícono asociado al menú principal
    'default_index': 0,  # Índice predeterminado al cargar el menú principal
    'with_view_panel': 'sidebar',  # Indica dónde mostrar el contenido del menú principal (en la barra lateral)
    'orientation': 'vertical',  # Orientación del menú principal (vertical en este caso)
    'styles': styles  # Estilos del menú principal
}
# Definición de una función para mostrar un menú interactivo
def show_menu(menu):
    # Función interna para obtener las opciones del menú
    def _get_options(menu):
        options = list(menu['items'].keys())
        return options
    # Función interna para obtener los iconos asociados a las opciones del menú
    def _get_icons(menu):
        icons = [v['item_icon'] for _k, v in menu['items'].items()]
        return icons
    # Configuración de parámetros para la función de menú
    kwargs = {
        'menu_title': menu['title'],
        'options': _get_options(menu),
        'icons': _get_icons(menu),
        'menu_icon': menu['menu_icon'],
        'default_index': menu['default_index'],
        'orientation': menu['orientation'],
        'styles': menu['styles']
    }
    # Obtener el tipo de panel de vista (sidebar o main)
    with_view_panel = menu['with_view_panel']
    # Mostrar el menú en el panel correspondiente
    if with_view_panel == 'sidebar':
        with st.sidebar:
            menu_selection = option_menu(**kwargs)
    elif with_view_panel == 'main':
        menu_selection = option_menu(**kwargs)
    else:
        # Lanzar una excepción si el tipo de panel de vista no es reconocido
        raise ValueError(f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")
    # Lógica para manejar la selección del menú "Inicio"
    if menu_selection == 'Inicio':
        if menu['items'][menu_selection]['submenu']:
            col1, col2 = st.columns(2)
            selected_year = col1.slider("Seleccione año:", min(df["PERIODO"].unique()), max(df["PERIODO"].unique()))
            st.session_state['anio_seleccionado'] = selected_year
            filtered_year = df[df["PERIODO"] == selected_year]
            reg_nat_values = filtered_year["REG_NAT"].unique()
            reg_nat_values = reg_nat_values[~pd.isna(reg_nat_values)]  # Excluir valores NaN
            selected_reg_nat = col2.radio("Seleccione región natural:", reg_nat_values, horizontal=True)
            st.session_state['df_guardado'] = filtered_year[filtered_year["REG_NAT"] == selected_reg_nat]
            st.toast('Seleccionaste año: '+str(selected_year)+' 📅', icon='❤')
            st.toast('Seleccionaste región: '+selected_reg_nat+' ⛰️', icon='😍')
    # Lógica para mostrar submenú si está presente
    if menu['items'][menu_selection]['submenu']:
        show_menu(menu['items'][menu_selection]['submenu'])
    # Lógica para ejecutar la acción asociada si está presente
    if menu['items'][menu_selection]['action']:
        menu['items'][menu_selection]['action']()
# Mostrar una imagen en la barra lateral usando Streamlit
st.sidebar.image('https://www.precayetanovirtual.pe/moodle/pluginfile.php/1/theme_mb2nl/loadinglogo/1692369360/logo-cayetano.png', use_column_width=True)
# Llamar a la función para mostrar el menú interactivo
show_menu(menu)
# Crear tres columnas en la barra lateral (1:8:1 ratio)
col1, col2, col3 = st.sidebar.columns([2, 4, 2])
# Espacio en blanco en la primera y tercera columna para centrar la imagen
with col1:
    st.write("")
# Mostrar una imagen en la segunda columna, probablemente un avatar o logotipo
with col2:
    st.image('reaccion.png', use_column_width=True)
# Espacio en blanco en la tercera columna para centrar la imagen
with col3:
    st.write("")
# Mostrar un texto en la barra lateral después de las columnas y agregar efecto de nieve
st.sidebar.text("Ing. ambiental - UPCH|2024")
# Inicializar la variable en el estado de la sesión
if 'snow_shown' not in st.session_state:
    st.session_state.snow_shown = False

# Mostrar la animación de nieve una vez
if not st.session_state.snow_shown:
    st.snow()
    st.session_state.snow_shown = True
