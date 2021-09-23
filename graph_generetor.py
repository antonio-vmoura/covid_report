import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from mpl_toolkits.basemap import Basemap

class Graph():

    def coolors(length):
        return [np.random.rand(1, 3)[0] for x in range(length)] #retorna cores aleatorias

    def compare_deaths(df, title="Mortes por estados", xlabel="Estados", ylabel="Mortes"):
        graph_path = "assets/image/compare_deaths.jpg"

        df = df.sort_values(by='deaths', ascending=False) #ordenando o dataset pelas mortes
        ax = df.plot.bar(x='state', y='deaths', color=Graph.coolors(len(df)), legend=None)
        
        # ax.set_title(f"{title}", fontsize=20, loc="center", pad=20)
        ax.set_ylabel(f"{ylabel}")
        ax.set_xlabel(f"{xlabel}")

        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()

        return graph_path

    def compare_deaths_pie(df, title="Mortes por estados"):
        graph_path = "assets/image/compare_deaths_pie.jpg"

        df = df.sort_values(by='deaths', ascending=False) #ordenando o dataset pelas mortes
        ax = df.plot.pie(x='state', y='deaths', shadow=False, startangle=90, colors=Graph.coolors(len(df)), wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': 'dashed', 'antialiased': True}, labels=None, ylabel='')
        
        # ax.set_title(f"{title}", fontsize=20, loc="center", pad=20)
        percents = df["deaths"].to_numpy() * 100 / df["deaths"].to_numpy().sum()
        labels=['%s, %1.1f%%' % (l, s) for l, s in zip(df.state, percents)]

        ax.legend(labels=labels, loc="center", ncol=5, handleheight=1.3, labelspacing=1.5, bbox_to_anchor=(0.5,-0.3))

        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()

        return graph_path

    def compare_cases(df, title="Casos por estados", xlabel="Número de casos", ylabel="Estados"):
        graph_path = "assets/image/compare_cases.jpg"

        df = df.sort_values(by='cases', ascending=True) #ordenando o dataset pelos casos
        ax = df.plot.barh(x='state', y='cases', color=Graph.coolors(len(df)), edgecolor='k', legend=None)
        
        # ax.set_title(f"{title}", fontsize=20, loc="center", pad=20)
        ax.set_xlabel(f"{xlabel}")
        ax.set_ylabel(f"{ylabel}")

        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()

        return graph_path

    def deaths_per_date(df, city="SP", title="Mortes e casos de", xlabel="Data"): 
        graph_path = f"assets/image/deaths_per_date_{city}.jpg"

        df_mask = df["state"] == "SP" #Criando uma mascara para filtrar os relatorios publicados mais atuais
        city_covid_data = (df[df_mask]).set_index("date")

        fig = plt.figure()

        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        city_covid_data.plot(y='cases', ax=ax1, color=Graph.coolors(len(df)), legend=True)
        ax1.set_xlabel("")
        ax1.legend(labels=["Casos"], loc="upper center")
        ax1.ticklabel_format(useOffset=False, style='plain', axis='y')

        city_covid_data.plot(y='deaths', ax=ax2, color=Graph.coolors(len(df)), legend=True)
        ax2.set_xlabel(f"{xlabel}")
        ax2.legend(labels=["Mortes"], loc="upper center")
        ax2.ticklabel_format(useOffset=False, style='plain', axis='y')

        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()

        return graph_path

    def death_range(df, city="DF", title="Mortes e casos de", xlabel="Data"):
        colors = ["#0F9300", "#74E876", "#FCD638", "#FE8F84", "#EE2B34"]; cp_x = 0
        graph_path = f"assets/image/death_range.jpg"

        avg_value = df["deaths"].mean(); max_value = df["deaths"].max(); min_value = df["deaths"].min()
        city_deaths = df.loc[df['state'] == 'DF'].deaths

        fig = plt.figure(figsize=(7,1), dpi=80)

        for color in colors: #pintando o grafico
            plt.axvspan(cp_x,cp_x + (max_value/5), color=color, alpha=1)
            cp_x += max_value/5

        plt.gca().axes.get_yaxis().set_visible(False)

        plt.xticks(np.arange(0, 11, 1))
        plt.xlim([min_value, max_value])
        plt.xlabel(f"Posição do {city} na media de mortes do Brasil")

        plt.yticks(np.arange(0,2, 1))
        plt.ylim([0, 2])            

        plt.plot(54,1, "ko")

        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()

        return graph_path

    def wordclound(df, title="Quantidade de artigos pela data", xlabel="Data", ylabel="Quantidade de artigos"): #data = [{"name": "Example", "content": ["2021-07-26", "2021-07-18"]}, {"x": "Example2", "y": 10}
        paths = []
        stopwords = set(STOPWORDS)
        stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "não", "na", "a", "e", "i", "o", "u", "que", "é", "para"]) #adicionando stopwords em portugues

        unique_string = ' '.join(df['state'])
        wordcloud = WordCloud(width = 3000, height = 2000, background_color="white", max_words=50, colormap='Set2', collocations=False, stopwords = stopwords).generate(unique_string)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

        plt.legend()
        graph_path = f"assets/image/wordclound.jpg"
        plt.savefig(graph_path, bbox_inches='tight')
        plt.close()

        paths.append(graph_path)

        return paths

    def covid_map(df, df_coordinates, projection='lcc', dtype="deaths"):
        select_city = df_coordinates.loc[df_coordinates['city_name'] == 'Brasília']

        lat = float(select_city.lat); lon = float(select_city.long); graph_path = f"assets/image/covid_{dtype}_map.jpg"

        if projection == "lcc":
            map = Basemap(width=12000000,height=9000000,projection='lcc', resolution="c", lat_1=lat, lat_2=lat, lat_0=lat, lon_0=lon)
            map.shadedrelief()
        elif projection == "ortho":
            map = Basemap(projection='ortho', resolution="c", lat_1=lat, lat_2=lat, lat_0=lat, lon_0=lon)
            map.shadedrelief()
        elif projection == "cyl":
            map = Basemap(projection='cyl', llcrnrlat=lat-15, urcrnrlat=lat+15, llcrnrlon=lon-15, urcrnrlon=lon+15, resolution='c') #lat_0=50, lon_0=-100
            map.drawcoastlines(); map.drawmapboundary(fill_color="#7777ff"); map.fillcontinents(color="#ddaa66",lake_color="#7777ff")
            map.drawcoastlines(); map.drawcountries(); map.drawstates() #coloca linhas para facilitar a visualizacao, deixa o mapa mais poluido
        elif projection == "vandg":
            map = Basemap(projection='vandg', lon_0=0, resolution='c')
            map.drawcoastlines(); map.drawmapboundary(fill_color="#7777ff"); map.fillcontinents(color="#ddaa66",lake_color="#7777ff")
            # map.nightshade(datetime.datetime.now(), delta=0.2) #Coloca a sombra dentro do mapa

        avg_value = df["deaths"].mean() if dtype == "deaths" else df["cases"].mean()

        for index, row in df.iterrows():
            city_name = row["name"]
            city_value = row["deaths"] if dtype == "deaths" else row["cases"]

            city_infos = df_coordinates.loc[df_coordinates['city_name'] == city_name]
            lat = city_infos.lat; lon = city_infos.long

            if 1 <= city_value <= avg_value/3: 
                x,y = map(lon,lat)
                map.plot(x,y, 'go', ms="0.6")
            elif avg_value/3 < city_value <= (avg_value/3)*2: 
                x,y = map(lon,lat)
                map.plot(x,y, 'yo', ms="0.8")
            elif (avg_value/3)*2 < city_value <= avg_value: 
                x,y = map(lon,lat)
                map.plot(x,y, 'ro', ms="1.0")
        
        plt.savefig(graph_path, bbox_inches='tight')
        plt.close() 

        return graph_path  

