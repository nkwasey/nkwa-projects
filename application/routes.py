__author__ = "Nana Ekow Nkwa Sey"

# Importing necessary requirements

from flask import current_app as app
from flask import render_template, request, jsonify
from application.fireAPI.queries import search_byDate
import datetime
from .firemap.create_df import create_modis_all_df, create_viirs_all_df


# Projects homepage
@app.route('/projects')
def projects_template():
    return render_template('projects/projects.html')


# Routes for Fire API
@app.route('/fire-api')
def fire_api():
    return render_template('projects/api/fire-api.html')


@app.route('/api/fires', methods=['GET'])
def get_fires():
    instr = request.args.get('instr', type=str)
    selected_date = request.args.get('date', type=str)

    if instr is not None and selected_date is not None:

        output = []

        mm, dd, yy = selected_date.split("-")
        acq_date = mm + '/' + dd + '/' + yy
        date_format = "%m/%d/%Y"

        try:
            datetime.datetime.strptime(acq_date, date_format)

            if instr == "modis":
                try:
                    df = create_modis_all_df()
                    search_byDate(acq_date, df, output)
                except KeyError as e:
                    error = {
                        "Error message": 'Check country name "%s"' % str(e)
                    }
                    output.append(error)
                    return jsonify(output), 404

            elif instr == "viirs":
                try:
                    df = create_viirs_all_df()
                    search_byDate(acq_date, df, output)
                except KeyError as e:
                    error = {
                        "Error message": 'Check country name "%s"' % str(e)
                    }
                    output.append(error)
                    return jsonify(output), 404
            else:
                error = {
                    "Available instruments": ['viirs', 'modis'],
                    "Error message": 'Check instrument name "%s"' % str(instr)}
                output.append(error)
                return jsonify(output), 404

            return jsonify(output), 200
        except ValueError as e:
            error = {
                "Error message": '"Incorrect date format. It should be MM-DD-YYYY "%s"' % str(e)
            }
            output.append(error)
            return jsonify(output), 404


# Routes for Nkwa's Project (Python)
@app.route('/')
def home_template():
    return render_template('index.html')


