from flask import Flask, render_template, request, url_for
from flask_navigation import Navigation
import analysis

app = Flask(__name__)
nav = Navigation(app)

# initializing Navigations
nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Strat', 'stratoptimizer'),
    nav.Item('WinRates', 'winrates'),
])

map_list = ['Acropolis', 'Arabia', 'Arena', 'Atacama', 'Fortress', 'Four Lakes', 'Golden Pit', 'Hideout', 'Islands', 'MegaRandom', 'Migration', 'Nomad']
civ_name_list = ['Aztecs', 'Berbers', 'Britons', 'Bulgarians', 'Burgundians', 'Burmese', 'Byzantines', 'Celts', 'Chinese', 'Cumans', 'Ethiopians', 'Franks', 'Goths', 'Huns', 'Incas', 'Indians', 'Italians', 'Japanese', 'Khmer', 'Koreans', 'Lithuanians', 'Magyars', 'Malay', 'Malians', 'Mayans', 'Mongols', 'Persians', 'Portuguese', 'Saracens', 'Sicilians', 'Slavs', 'Spanish', 'Tatars', 'Teutons', 'Turks', 'Vietnamese', 'Vikings']

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', map_list=map_list, civ_name_list=civ_name_list)

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/winrates', methods=['GET'])
def winrates():

    return render_template('winrates.html', map_list=map_list)

@app.route('/stratoptimizer', methods=['GET'])
def stratoptimizer():
    
    return render_template('stratoptimizer.html', map_list=map_list, civ_name_list=civ_name_list)


@app.route('/results', methods=['POST'])
def results():
    address_path = request.form.get('data_from_where')
    selected_map = request.form.get('aoe2map')

    if address_path == 'stratoptimizer':
        selected_player_civ = request.form.get('player_civ_name')
        selected_enemy_civ = request.form.get('enemy_civ_name')
        selected_elo = request.form.get('elo')

        res = analysis.formulate_strat(selected_map, selected_player_civ, selected_enemy_civ, selected_elo)

    elif address_path == 'winrates':
        selected_elo = request.form.get('elo')
        selected_fromduration = request.form.get('fromDuration')
        selected_toduration = request.form.get('toDuration')

        res = analysis.analyze_winrates(selected_elo, selected_map, selected_fromduration, selected_toduration)
    
    else:
        # returns forbidden http code
        raise NotImplementedError()
    
    
    return render_template(f'{address_path}.html', res=res, map_list=map_list, civ_name_list=civ_name_list, url='/static/images/plot.png')


if __name__ == "__main__":
    app.run(debug=True)