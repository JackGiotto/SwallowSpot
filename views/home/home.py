from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/')
def home():
    print (session)
    if "username" not in session:
        bulletin_data = '''
                            Per rimanere aggiornato sulla tua zona esegui l'accesso
                            <a href="/auth/login/" class="btn btn-success m-2 btn-lg"> Accedi</a>'''
    else:
        # debug
        region_name = "Vene-A"
        hydraulic = "green"
        hydro_geo = "red"
        storms = "orange"
        update = "13-04-2024"

        # query to get user data
        # query to get the last bullettin of the user area

        print ("ciao ciao")
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
                                <p class="last-update" id="update-vene-a">Ultimo aggiornamento: {update}<heregoesthedate /></p>
                             </div>'''

    return render_template("home.html", bulletin_data = bulletin_data)
