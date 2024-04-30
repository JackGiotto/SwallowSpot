from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/')
def home():
    if "username" in session:
        return render_template("home.html")
    else:
        region_name = "Vene-A"
        hydraulic = "green"
        hydro_geo = "red"
        storms = "orange"
        bulletin_data = f'''<div class="risk-out" id="vene-a">
                                <h2>{region_name}</h2>
                                <div class="risk-in">
                                    <div class="risk">
                                        <span class="circle {hydraulic}"></span>
                                        <p>Rischio idraulico</p>
                                    </div>
                                    <div class="risk">
                                        <span class="circle {hydro_geo}"></span>
                                        <p>Rischio idro-geologico</p>
                                    </div>
                                    <div class="risk">
                                        <span class="circle {storms}"></span>
                                        <p>Rischio idro-geologico per temporale</p>
                                    </div>
                                </div>
                                <p class="basin">Bacino correlato: Alto Piave</p>
                                <p class="last-update" id="update-vene-a">Ultimo aggiornamento: <heregoesthedate /></p>
                             </div>'''
        # query to get user data
        # query to get the last bullettin of an area
        return render_template("home.html", bulletin_data = bulletin_data)
