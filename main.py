import pandas as pd # Dataframes
from graph_generetor import Graph
from pdf_generetor import PdfReport

def main():
    #lendo o conjunto de dados
    brazil_covid_data = pd.read_csv("assets/dataset/brazil_covid19.csv") #https://www.kaggle.com/unanimad/corona-virus-brazil
    brazil_covid_cities_data = pd.read_csv("assets/dataset/brazil_covid19_cities.csv")
    brazil_cities_coordinates = pd.read_csv("assets/dataset/brazil_cities_coordinates.csv")

    #pegando apenas os dados relevantes dos conjuntos de dados passados
    last_date = brazil_covid_data['date'].iloc[-1] #pegando a ultima data
    df_mask = brazil_covid_data["date"] == last_date #Criando uma mascara para filtrar os relatorios publicados mais atuais apenas do dataset que contem os estados
    filtered_brazil_covid_data = (brazil_covid_data[df_mask]).reset_index(drop=True)

    df_mask = brazil_covid_cities_data["date"] == brazil_covid_cities_data['date'].iloc[-1] #Criando uma mascara para filtrar os relatorios publicados mais atuais do dataset que especifica as cidades
    filtered_brazil_covid_cities_data = (brazil_covid_cities_data[df_mask]).reset_index(drop=True)

    df_filter  = ((filtered_brazil_covid_cities_data['deaths'] > 0) & (filtered_brazil_covid_cities_data['cases'] > 0))
    filtered_brazil_covid_cities_data = filtered_brazil_covid_cities_data[df_filter]

    #gerando graficos
    compare_deaths = Graph.compare_deaths(filtered_brazil_covid_data)
    compare_deaths_pie = Graph.compare_deaths_pie(filtered_brazil_covid_data)
    compare_cases = Graph.compare_cases(filtered_brazil_covid_data)
    deaths_per_date = Graph.deaths_per_date(brazil_covid_data, city="SP")
    covid_deaths_map = Graph.covid_map(filtered_brazil_covid_cities_data, brazil_cities_coordinates, projection ="lcc", dtype="deaths")
    covid_cases_map =  Graph.covid_map(filtered_brazil_covid_cities_data, brazil_cities_coordinates, projection ="ortho", dtype="cases")

    #gerando o pdf
    data = {"date": last_date, "compare_deaths": compare_deaths, "compare_deaths_pie": compare_deaths_pie, "compare_cases": compare_cases, "deaths_per_date": deaths_per_date, "quantity_date": "quantity_date", "covid_map": [covid_deaths_map, covid_cases_map]} #montando o dicionario que e lido pelo gerador de pdfs
    PdfReport.createPDF(data)

if __name__ == "__main__":
    main()  
