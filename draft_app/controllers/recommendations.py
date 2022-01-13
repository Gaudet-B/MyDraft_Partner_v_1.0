from flask import app
from flask import render_template, request, redirect, session, flash
from werkzeug.utils import redirect
from draft_app import app
from draft_app.models.user import User, Admin
from draft_app.models.player import Player
from draft_app.models.team import Team
from draft_app.models.recommendation import Recommendation
from draft_app.controllers import general