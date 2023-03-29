from flask import Flask, render_template, request, url_for
import analysis

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    map_list = ['Acropolis', 'Arabia', 'Arena', 'Atacama', 'Fortress', 'Four Lakes', 'Golden Pit', 'Hideout', 'Islands', 'MegaRandom', 'Migration', 'Nomad']
    civ_name_list = ['Aztecs', 'Berbers', 'Britons', 'Bulgarians', 'Burgundians', 'Burmese', 'Byzantines', 'Celts', 'Chinese', 'Cumans', 'Ethiopians', 'Franks', 'Goths', 'Huns', 'Incas', 'Indians', 'Italians', 'Japanese', 'Khmer', 'Koreans', 'Lithuanians', 'Magyars', 'Malay', 'Malians', 'Mayans', 'Mongols', 'Persians', 'Portuguese', 'Saracens', 'Sicilians', 'Slavs', 'Spanish', 'Tatars', 'Teutons', 'Turks', 'Vietnamese', 'Vikings']
    
    return render_template('index.html', map_list=map_list, civ_name_list=civ_name_list)

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        selected_map = request.form.get('aoe2map')
        selected_player_civ = request.form.get('player_civ_name')
        selected_enemy_civ = request.form.get('enemy_civ_name')

        print(selected_map)
        print(selected_player_civ)
        print(selected_enemy_civ)
    
    res = analysis.analyse()
    #print(res)

    return render_template('results.html', res=res)


if __name__ == "__main__":
    app.run(debug=True)