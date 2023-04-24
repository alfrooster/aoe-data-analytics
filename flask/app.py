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

@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html', map_list=map_list, civ_name_list=civ_name_list)

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/winrates', methods=['GET', 'POST'])
def winrates():

    return render_template('winrates.html', map_list=map_list)

@app.route('/stratoptimizer', methods=['GET', 'POST'])
def stratoptimizer():
    
    return render_template('stratoptimizer.html', map_list=map_list, civ_name_list=civ_name_list)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST' and request.form.get('data_from_where') == 'stratoptimizer':
        selected_map = request.form.get('aoe2map')
        selected_player_civ = request.form.get('player_civ_name')
        selected_enemy_civ = request.form.get('enemy_civ_name')
        selected_elo = request.form.get('elo')

        print(request.form.get('data_from_where'))
        print(selected_map)
        print(selected_player_civ)
        print(selected_enemy_civ)
        print(selected_elo)
    
        res = analysis.formulate_strat(selected_map, selected_player_civ, selected_enemy_civ, selected_elo)
        #print(res)
        return render_template('stratoptimizer.html', res=res, map_list=map_list, civ_name_list=civ_name_list)

    elif request.method == 'POST' and request.form.get('data_from_where') == 'winrates':
        selected_elo = request.form.get('elo')
        selected_map = request.form.get('aoe2map')
        selected_duration = request.form.get('duration')

        print(request.form.get('data_from_where'))
        print(selected_elo)
        print(selected_map)
        print(selected_duration)

        res = analysis.analyze_winrates(selected_elo, selected_map, selected_duration)

        return render_template('winrates.html', res=res, map_list=map_list, civ_name_list=civ_name_list)


if __name__ == "__main__":
    app.run(debug=True)