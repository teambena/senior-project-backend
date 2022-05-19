from flask import Blueprint, render_template
report_blueprint = Blueprint('report', __name__
)
@report_blueprint.route('', methods=['POST'])
def index():
    return render_template('layouts/report_layout.html')
